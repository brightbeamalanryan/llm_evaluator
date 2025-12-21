## Why
The RAG configuration needs to support multiple host profiles and parallel evaluation while removing the legacy single `service_url` path.

## What Changes
- Replace single `rag.service_url`/endpoint fields with a list of named RAG profiles, each with its own endpoints and request profile.
- Add an `active` flag and CLI selection to control which profiles run during RAG tests.
- Use profile names in logging and reporting to distinguish parallel runs.
- **BREAKING**: remove support for `rag.service_url` and related legacy endpoint fields.

## Impact
- Affected specs: rag-config
- Affected code: config parsing, CLI flags, RAG runner orchestration, logging/report labeling
