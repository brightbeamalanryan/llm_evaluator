## ADDED Requirements
### Requirement: RAG HTTP request profile
The system SHALL allow RAG configuration to define a single HTTP request profile with a URL, HTTP method, headers, and JSON body template for the request payload.

#### Scenario: Stream agent POST request
- **WHEN** the configuration defines a request profile with a full URL, `POST` method, `Content-Type: application/json` header, and body template fields `query`, `account_id`, and `prompt`
- **THEN** the system sends the request to that URL with the configured headers and JSON body

### Requirement: Legacy RAG endpoint fields compatibility
The system SHALL continue to support `rag.service_url` with `rag.query_endpoint`, `rag.retrieve_endpoint`, and `rag.ingest_endpoint` when no request profile is provided.

#### Scenario: Legacy config without request profile
- **WHEN** the configuration only specifies `service_url` and `query_endpoint`
- **THEN** the system sends a query request to the concatenated URL as before
