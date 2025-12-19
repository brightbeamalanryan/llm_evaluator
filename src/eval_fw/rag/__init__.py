"""RAG security testing module."""

from eval_fw.rag.loader import RAGTestCase, RAGTestLoader, InjectedDocument
from eval_fw.rag.client import RAGClient, RAGResponse, MockRAGClient, RetrievedDocument
from eval_fw.rag.detectors import (
    MetadataLeakageDetector,
    ContextInjectionDetector,
    RetrievalOverrideDetector,
    MultiHopContextDetector,
    HallucinatedRuleDetector,
    DetectionResult,
)
from eval_fw.rag.scoring import RAGSeverityScorer, RAGAttackType, RAGTestResult
from eval_fw.rag.runner import RAGSessionRunner, RAGSession

__all__ = [
    "RAGTestCase",
    "RAGTestLoader",
    "InjectedDocument",
    "RAGClient",
    "RAGResponse",
    "MockRAGClient",
    "RetrievedDocument",
    "MetadataLeakageDetector",
    "ContextInjectionDetector",
    "RetrievalOverrideDetector",
    "MultiHopContextDetector",
    "HallucinatedRuleDetector",
    "DetectionResult",
    "RAGSeverityScorer",
    "RAGAttackType",
    "RAGTestResult",
    "RAGSessionRunner",
    "RAGSession",
]
