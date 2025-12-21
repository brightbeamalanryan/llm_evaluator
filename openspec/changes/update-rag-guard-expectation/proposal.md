## Why
Guard scoring is allowing responses that include simulated or indirect leakage language. We want the guard to make a clear pass/fail decision based on a single combined expectation that always includes a baseline leakage policy plus the test-specific expectation.

## What Changes
- Add a default guard expectation that covers all leakage categories and safe behavior.
- Combine the default expectation with each test case expectation when building the guard prompt.
- Simplify the guard prompt to ask the LLM whether the response passed or failed against the combined expectations.

## Impact
- Affected specs: rag-guard
- Affected code: RAG guard scoring prompt and expectation assembly in RAG scoring
