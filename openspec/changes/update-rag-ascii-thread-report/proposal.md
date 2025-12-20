## Why
The current RAG logs are too verbose and hard to follow. We need a readable, visually pleasing transcript view that shows the back-and-forth evolution of queries and responses while keeping call information accessible.

## What Changes
- Add a new ASCII report format that renders a WhatsApp/SMS-style thread for each RAG test.
- Include key call events (mutator requests, guard scoring, HTTP calls if configured) in the thread view.
- Integrate the ASCII report into the existing reporting module and enable it via config for RAG runs.

## Impact
- Affected specs: reporting
- Affected code: reporting module, rag CLI/report generation, log parsing or event capture
