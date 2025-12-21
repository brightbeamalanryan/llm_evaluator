## Why
Some RAG endpoints return non-JSON streaming responses (e.g., SSE `text/event-stream`), so the client needs a configurable response parser to extract the answer text.

## What Changes
- Add a response profile under `rag.request_profile` to select a response parser.
- Provide an initial SSE parser that concatenates `data:` fields for `agent_response` events into the final answer, while retaining raw payloads.

## Impact
- Affected specs: rag-response (new)
- Affected code: src/eval_fw/config/settings.py, src/eval_fw/rag/client.py, config.example.yaml, tests
