## Why
RAG (Retrieval-Augmented Generation) systems introduce unique attack vectors through the retrieval pipeline. Malicious content in retrieved documents can override instructions, leak metadata, or poison responses. This is the largest blind spot in production RAG deployments.

## What Changes
- Context injection attack tests (JSON-based test cases)
- Retrieval override attempt detection
- Prompt template inversion tests
- Metadata leakage detection
- Multi-hop RAG attack simulation
- Vector store integration for realistic testing (optional dependency)

## Reused Components
- `HallucinatedRuleDetector` from `src/eval_fw/guard/meta_evaluator.py` (already implemented)

## Implementation Notes
- Test cases in `use_cases/rag_tests.json` (consistent with bypass_tests.json pattern)
- Module location: `src/eval_fw/rag/` (not suites/)
- Vector store deps (ChromaDB, Pinecone) as optional extras

## Impact
- Affected specs: core (depends on), prompt-security (shares patterns)
- Affected code: `src/eval_fw/rag/` (new module)
