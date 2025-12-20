"""ASCII thread report generator for RAG runs."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import re
from typing import Any

from eval_fw.rag.scoring import RAGTestResult


@dataclass
class RagThreadEvent:
    """A single parsed event from the RAG log."""

    kind: str
    payload: dict[str, Any]


@dataclass
class RagThread:
    """Thread view of a single RAG test."""

    test_id: str
    description: str
    events: list[RagThreadEvent]


class RAGAsciiReporter:
    """Generate ASCII chat-style reports for RAG runs."""

    _TEST_START_RE = re.compile(r"RAG test start id=(?P<id>\S+)")
    _TEST_DESC_RE = re.compile(r"RAG test description=(?P<desc>.+)")
    _ITER_RE = re.compile(r"RAG iteration (?P<iter>\d+)/")
    _ITER_PROMPT_RE = re.compile(r"RAG iteration prompt=(?P<prompt>.+)")
    _ITER_RESPONSE_RE = re.compile(r"RAG iteration response=(?P<response>.+)")
    _ITER_SCORE_RE = re.compile(r"RAG iteration score=(?P<score>[-\d.]+)")
    _MUTATOR_REQ_RE = re.compile(r"RAG mutator request=(?P<request>.+)")
    _MUTATOR_REPLY_RE = re.compile(r"RAG mutator reply=(?P<reply>.+)")
    _GUARD_RE = re.compile(
        r"RAG guard verdict id=(?P<id>\S+) verdict=(?P<verdict>\S+) "
        r"severity=(?P<severity>[-\d.]+) notes=(?P<notes>.+)"
    )
    _HTTP_RE = re.compile(r"HTTP Request: (?P<method>\S+) (?P<url>\S+)")

    def generate(
        self,
        results: list[RAGTestResult],
        summary: dict[str, Any],
        output_path: Path,
        log_path: Path,
        metadata: dict[str, Any] | None = None,
        sidecar_path: Path | None = None,
    ) -> Path:
        """Generate an ASCII report file."""
        output_path = output_path.with_suffix(".txt")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        allowed_ids = {r.test_case.id for r in results}
        threads = self._load_threads(sidecar_path, log_path, allowed_ids)

        result_map = {r.test_case.id: r for r in results}
        lines: list[str] = []
        lines.extend(self._render_header(summary, metadata))
        lines.append("")

        for test_id, thread in threads.items():
            result = result_map.get(test_id)
            lines.extend(self._render_thread(thread, result))
            lines.append("")

        output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        return output_path

    def _render_header(
        self,
        summary: dict[str, Any],
        metadata: dict[str, Any] | None,
    ) -> list[str]:
        meta = metadata or {}
        generated = datetime.now().isoformat(timespec="seconds")
        header = [
            "RAG ASCII THREAD REPORT",
            "=" * 72,
            f"Generated: {generated}",
        ]
        if meta:
            for key, value in meta.items():
                header.append(f"{key}: {value}")
        header.append(
            f"Summary: total={summary.get('total', 0)} "
            f"passed={summary.get('passed', 0)} "
            f"failed={summary.get('failed', 0)} "
            f"avg_severity={summary.get('avg_severity', 0):.1f} "
            f"max_severity={summary.get('max_severity', 0):.1f}"
        )
        header.append("=" * 72)
        return header

    def _render_thread(
        self,
        thread: RagThread,
        result: RAGTestResult | None,
    ) -> list[str]:
        status = "UNKNOWN"
        severity = "n/a"
        if result:
            status = "PASS" if result.passed else "FAIL"
            severity = f"{result.severity_score:.1f}"
        lines = [
            f"TEST {thread.test_id} | {thread.description} | {status} | severity={severity}",
            "-" * 72,
        ]

        last_iter = None
        for event in thread.events:
            kind = event.kind
            payload = event.payload
            if kind in {"iteration", "exchange"}:
                iter_no = payload.get("iteration") or payload.get("role", "exchange")
                prompt = payload.get("prompt", "")
                response = payload.get("response", "")
                score = payload.get("score", "")
                if iter_no != last_iter:
                    if kind == "exchange":
                        lines.append(f"[{iter_no}]")
                    else:
                        lines.append(f"[iter {iter_no} | score {score}]")
                    last_iter = iter_no
                lines.append(f"USER> {prompt}")
                lines.append(f"RAG > {response}")
            elif kind == "mutator_request":
                lines.append(f"  mutator> request: {payload.get('request')}")
            elif kind == "mutator_reply":
                lines.append(f"  mutator< reply: {payload.get('reply')}")
            elif kind == "guard":
                lines.append(
                    "  guard> verdict={verdict} severity={severity} notes={notes}".format(
                        verdict=payload.get("verdict"),
                        severity=payload.get("severity"),
                        notes=payload.get("notes"),
                    )
                )
            elif kind == "call":
                lines.append(
                    f"  call> {payload.get('target')} {payload.get('detail', '')}".rstrip()
                )
            elif kind == "http":
                lines.append(
                    f"  call> {payload.get('method')} {payload.get('url')}"
                )
        return lines

    def _load_threads(
        self,
        sidecar_path: Path | None,
        log_path: Path,
        allowed_ids: set[str],
    ) -> dict[str, RagThread]:
        if sidecar_path and sidecar_path.exists():
            return self._parse_sidecar(sidecar_path, allowed_ids)
        return self._parse_threads(log_path, allowed_ids)

    def _parse_sidecar(
        self,
        sidecar_path: Path,
        allowed_ids: set[str],
    ) -> dict[str, RagThread]:
        data = json.loads(sidecar_path.read_text(encoding="utf-8"))
        threads: dict[str, RagThread] = {}
        for thread in data.get("threads", []):
            test_id = thread.get("test_id")
            if test_id not in allowed_ids:
                continue
            events = [
                RagThreadEvent(kind=e.get("kind", ""), payload=e.get("data", {}))
                for e in thread.get("events", [])
            ]
            threads[test_id] = RagThread(
                test_id=test_id,
                description=thread.get("description", ""),
                events=events,
            )
        return threads

    def _parse_threads(
        self,
        log_path: Path,
        allowed_ids: set[str],
    ) -> dict[str, RagThread]:
        threads: dict[str, RagThread] = {}
        current_test_id: str | None = None
        current_desc: str = ""
        current_iter: int | None = None
        iter_prompt: dict[int, str] = {}
        iter_response: dict[int, str] = {}
        iter_score: dict[int, str] = {}

        lines = log_path.read_text(encoding="utf-8").splitlines()
        start_idx = 0
        for idx, line in enumerate(lines):
            if "Initialized logging at" in line:
                start_idx = idx + 1

        def add_event(test_id: str, kind: str, payload: dict[str, Any]) -> None:
            if test_id not in allowed_ids:
                return
            thread = threads.setdefault(
                test_id,
                RagThread(test_id=test_id, description=current_desc, events=[]),
            )
            thread.events.append(RagThreadEvent(kind=kind, payload=payload))

        for line in lines[start_idx:]:
            start_match = self._TEST_START_RE.search(line)
            if start_match:
                current_test_id = start_match.group("id")
                current_desc = ""
                current_iter = None
                continue

            if current_test_id:
                desc_match = self._TEST_DESC_RE.search(line)
                if desc_match:
                    current_desc = desc_match.group("desc")
                    thread = threads.setdefault(
                        current_test_id,
                        RagThread(
                            test_id=current_test_id,
                            description=current_desc,
                            events=[],
                        ),
                    )
                    thread.description = current_desc

            guard_match = self._GUARD_RE.search(line)
            if guard_match:
                test_id = guard_match.group("id")
                add_event(
                    test_id,
                    "guard",
                    {
                        "verdict": guard_match.group("verdict"),
                        "severity": guard_match.group("severity"),
                        "notes": guard_match.group("notes"),
                    },
                )

            if not current_test_id:
                continue

            iter_match = self._ITER_RE.search(line)
            if iter_match:
                current_iter = int(iter_match.group("iter"))
                continue

            prompt_match = self._ITER_PROMPT_RE.search(line)
            if prompt_match and current_iter is not None:
                iter_prompt[current_iter] = prompt_match.group("prompt")
                continue

            response_match = self._ITER_RESPONSE_RE.search(line)
            if response_match and current_iter is not None:
                iter_response[current_iter] = response_match.group("response")
                continue

            score_match = self._ITER_SCORE_RE.search(line)
            if score_match and current_iter is not None:
                iter_score[current_iter] = score_match.group("score")
                payload = {
                    "iteration": current_iter,
                    "prompt": iter_prompt.get(current_iter, ""),
                    "response": iter_response.get(current_iter, ""),
                    "score": iter_score.get(current_iter, ""),
                }
                add_event(current_test_id, "iteration", payload)
                continue

            mutator_req_match = self._MUTATOR_REQ_RE.search(line)
            if mutator_req_match:
                add_event(
                    current_test_id,
                    "mutator_request",
                    {"request": mutator_req_match.group("request")},
                )
                continue

            mutator_reply_match = self._MUTATOR_REPLY_RE.search(line)
            if mutator_reply_match:
                add_event(
                    current_test_id,
                    "mutator_reply",
                    {"reply": mutator_reply_match.group("reply")},
                )
                continue

            http_match = self._HTTP_RE.search(line)
            if http_match and current_test_id:
                add_event(
                    current_test_id,
                    "http",
                    {"method": http_match.group("method"), "url": http_match.group("url")},
                )

        return threads
