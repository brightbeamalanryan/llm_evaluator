## 1. Attack Test Cases (JSON-based)
- [x] 1.1 Create context injection test cases in `use_cases/rag_tests.json`
- [x] 1.2 Create retrieval override test cases
- [x] 1.3 Create prompt template inversion test cases
- [x] 1.4 Create multi-hop attack chain test cases
- [x] 1.5 Create metadata extraction test cases

## 2. RAG Infrastructure
- [x] 2.1 Create `src/eval_fw/rag/` module structure
- [x] 2.2 Create mock RAG pipeline for testing (no external deps)
- [x] 2.3 Create RAG test loader (extends base TestLoader)
- [x] 2.4 Create RAG client for localhost:8091 service
- [x] 2.5 Implement context injection detector

## 3. Detection & Scoring
- [x] 3.1 Hallucinated rule detector (reuse from guard module)
- [x] 3.2 Implement source attribution validator
- [x] 3.3 Implement metadata leakage detector
- [x] 3.4 Create RAG-specific severity scoring

## 4. Testing
- [x] 4.1 Unit tests for RAG module
- [x] 4.2 Integration tests with mock RAG pipeline
