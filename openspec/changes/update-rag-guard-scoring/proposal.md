## Why
RAG test verdicts currently rely on pattern-matching detectors, which can miss nuanced failures. We want guard-model classification to decide pass/fail for RAG tests while preserving existing severity scoring.

## What Changes
- Replace detector-driven pass/fail in RAG scoring with guard LLM verdicts.
- Keep detector outputs for severity scoring and notes, but not for pass/fail.
- Reuse the existing guard provider configuration for RAG guard scoring.

## Impact
- Affected specs: rag-security
- Affected code: rag scoring and CLI wiring
