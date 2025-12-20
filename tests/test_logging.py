"""Tests for logging configuration and RAG logging."""

from __future__ import annotations

import logging
from pathlib import Path

from eval_fw.log_config import setup_logging
from eval_fw.rag.client import MockRAGClient
from eval_fw.rag.loader import RAGTestCase
from eval_fw.rag.runner import RAGSessionRunner


def _flush_handlers() -> None:
    for handler in logging.getLogger().handlers:
        handler.flush()


def _remove_log_handler(log_path: Path) -> None:
    root_logger = logging.getLogger()
    resolved = log_path.resolve()
    for handler in list(root_logger.handlers):
        base_filename = getattr(handler, "baseFilename", None)
        if base_filename and Path(base_filename).resolve() == resolved:
            root_logger.removeHandler(handler)
            handler.close()


def test_setup_logging_creates_file(tmp_path):
    log_path = setup_logging(tmp_path)
    logger = logging.getLogger("eval_fw.test")
    logger.info("hello log")
    _flush_handlers()

    assert log_path.exists()
    assert "hello log" in log_path.read_text(encoding="utf-8")

    _remove_log_handler(log_path)


def test_rag_runner_emits_log(tmp_path):
    log_path = setup_logging(tmp_path)
    client = MockRAGClient()
    runner = RAGSessionRunner(client)

    test_case = RAGTestCase(
        id="rag-test-logging",
        description="log check",
        attack_type="injection",
        query="hello",
        expectation="none",
        multi_hop_queries=["step-one"],
    )
    runner.run(test_case, endpoint_mode="query")
    _flush_handlers()

    content = log_path.read_text(encoding="utf-8")
    assert "RAG test start id=rag-test-logging" in content
    assert "RAG prompt session_id=None query=step-one" in content
    assert "RAG response session_id=None answer=Mock response for: step-one" in content
    assert "RAG prompt session_id=None query=hello" in content
    assert "RAG response session_id=None answer=Mock response for: hello" in content
    assert "RAG test complete id=rag-test-logging" in content

    _remove_log_handler(log_path)
