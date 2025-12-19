## 1. Attack Test Cases (JSON-based)
- [x] 1.1 Create context injection test cases in `use_cases/rag_tests.json`
- [x] 1.2 Create retrieval override test cases (include override types)
- [x] 1.3 Create metadata leakage test cases (filenames, chunk IDs)
- [x] 1.4 Create hallucinated rule test cases
- [x] 1.5 Create multi-hop attack simulation test cases (sequential prompts)

## 2. RAG Infrastructure
- [x] 2.1 Create `src/eval_fw/rag/` module structure
- [x] 2.2 Create mock RAG pipeline for testing (no external deps)
- [x] 2.3 Create RAG test loader (extends base TestLoader)
- [x] 2.4 Create RAG client for localhost:8091 service
- [x] 2.5 Support multi-hop execution sessions in the RAG runner

## 3. Detection & Scoring
- [x] 3.1 Implement context injection detector
- [x] 3.2 Implement retrieval override detector with override type logging
- [x] 3.3 Implement metadata leakage detector with severity mapping
- [x] 3.4 Hallucinated rule detector (reuse from guard module)
- [x] 3.5 Implement multi-hop context accumulation detector
- [x] 3.6 Create RAG-specific severity scoring

## 4. Testing
- [x] 4.1 Unit tests for RAG detectors and scoring
- [x] 4.2 Integration tests with mock RAG pipeline (including multi-hop)
