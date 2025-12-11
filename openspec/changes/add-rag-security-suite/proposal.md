## Why
RAG (Retrieval-Augmented Generation) systems introduce unique attack vectors through the retrieval pipeline. Malicious content in retrieved documents can override instructions, leak metadata, or poison responses. This is the largest blind spot in production RAG deployments.

## What Changes
- Context injection attack tests
- Retrieval override attempt detection
- Prompt template inversion tests
- Metadata leakage detection
- Multi-hop RAG attack simulation
- Hallucinated rule detection
- Vector store integration for realistic testing

## Impact
- Affected specs: core (depends on), prompt-security (shares patterns)
- Affected code: `src/eval_fw/suites/rag_security/`
