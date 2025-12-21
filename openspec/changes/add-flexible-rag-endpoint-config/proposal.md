## Why
RAG configuration currently assumes a base URL with fixed endpoints, which cannot express full URLs, custom headers, and request bodies required by stream-agent style endpoints.

## What Changes
- Add a single RAG HTTP request profile with URL, method, headers, and JSON body template.
- Use the request profile for query requests, with legacy `rag.service_url` and endpoint fields as fallback.

## Impact
- Affected specs: rag-config (new)
- Affected code: src/eval_fw/config/settings.py, src/eval_fw/cli/main.py, src/eval_fw/rag/client.py, config.example.yaml, src/eval_fw/rag/README.md, tests
