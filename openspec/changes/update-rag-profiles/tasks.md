## 1. Implementation
- [ ] 1.1 Define new RAG profile schema in settings parsing (list, validation, active selection rules).
- [ ] 1.2 Update CLI flags to select profiles and wire selection into the RAG runner.
- [ ] 1.3 Update RAG runner/client orchestration to iterate active/selected profiles and label logs/reports with profile names.
- [ ] 1.4 Remove legacy `service_url`/endpoint fields and add validation errors pointing to the new schema.
- [ ] 1.5 Update example config and docs to show `rag.profiles` usage.
- [ ] 1.6 Add/adjust tests for profile selection, validation, and labeling.

## 2. Validation
- [ ] 2.1 Run targeted test suite for RAG config/client behavior.
