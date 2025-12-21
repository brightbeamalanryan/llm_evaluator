## ADDED Requirements
### Requirement: RAG response profile selection
The system SHALL allow a request profile to specify a response profile that defines how to parse the HTTP response body.

#### Scenario: Response profile selects SSE parser
- **WHEN** the request profile defines a response profile with type `sse`
- **THEN** the client uses the SSE parser instead of JSON parsing

### Requirement: SSE response parsing for agent responses
The system SHALL parse `text/event-stream` responses by concatenating `data:` fields from `agent_response` events into the final answer.

#### Scenario: SSE agent_response stream
- **WHEN** the response body contains `event: agent_response` entries with `data:` payloads
- **THEN** the client returns an answer string created by joining the `data:` payloads in order and preserves the raw response
