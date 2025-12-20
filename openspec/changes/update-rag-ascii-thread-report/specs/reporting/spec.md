## ADDED Requirements

### Requirement: RAG ASCII Thread Report
The system SHALL generate an ASCII report that renders each RAG test as a chat-style thread showing the evolution of prompts and responses.

#### Scenario: Thread view for RAG test
- **WHEN** a RAG run is executed with report format `ascii`
- **THEN** the report contains a per-test thread with alternating prompt/response messages
- **AND** each message includes timestamp and iteration markers when available

### Requirement: Call Event Rendering
The system SHALL include call events (mutator, guard scoring, and service calls) as indented annotations within the ASCII thread.

#### Scenario: Mutator call annotation
- **WHEN** a mutator request and reply occur during a RAG test
- **THEN** the ASCII thread includes an indented mutator event block beneath the triggering prompt

#### Scenario: Guard scoring annotation
- **WHEN** guard scoring is performed for a RAG response
- **THEN** the ASCII thread includes an indented guard event block with verdict, severity, and notes
