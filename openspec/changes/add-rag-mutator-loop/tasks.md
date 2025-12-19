## 1. Implementation
- [x] 1.1 Add RAG mutator settings to config and example config
- [x] 1.2 Implement mutator prompt generation using `prompt-mutator` and prompt/response history
- [x] 1.3 Integrate mutator loop into `RAGSessionRunner` with plateau-based stopping
- [x] 1.4 Refactor `rag/scoring.py` for incremental scoring reuse in the mutator loop
- [x] 1.5 Update CLI wiring to pass mutator settings into RAG runner

## 2. Tests
- [x] 2.1 Add unit tests for mutator iteration and history usage
- [x] 2.2 Add unit test for plateau-based stopping

## 3. Validation
- [ ] 3.1 Run targeted pytest coverage for RAG suite
