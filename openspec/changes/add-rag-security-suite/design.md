## Context
RAG security testing requires simulating realistic retrieval pipelines and injecting malicious content at various stages. The framework must support different vector stores and chunking strategies.

## Goals / Non-Goals
- Goals:
  - Test RAG systems against document injection
  - Detect metadata and schema leakage
  - Validate source attribution
- Non-Goals:
  - Production vector store management
  - Embedding model security (separate concern)

## Decisions
- **Mock RAG:** Include lightweight mock for testing without real vector store
- **Adapters:** Support ChromaDB (local) and Pinecone (cloud) initially
- **Attack Library:** Pre-built injection payloads for common vulnerabilities

## RAG Attack Categories
1. **Context Injection:** Malicious instructions in retrieved docs
2. **Retrieval Override:** "Ignore previous documents..."
3. **Template Inversion:** Reconstruct RAG prompt template from outputs
4. **Metadata Leakage:** Extract filenames, chunk IDs, scores
5. **Multi-hop Attacks:** Chain queries to build context
6. **Hallucinated Rules:** Model invents policies from retrieved content
