## ADDED Requirements

### Requirement: RAG Thread Sidecar
The system SHALL generate a JSON sidecar file containing full RAG thread events for each RAG run.

#### Scenario: Sidecar generation
- **WHEN** a RAG run completes with reporting enabled
- **THEN** a sidecar JSON file is written containing all prompts, responses, and call events

### Requirement: ASCII Report from Sidecar
The system SHALL generate the ASCII thread report from the sidecar data when available.

#### Scenario: Full-fidelity thread rendering
- **WHEN** a sidecar JSON file exists for a run
- **THEN** the ASCII report uses the sidecar data and includes full prompt/response content
