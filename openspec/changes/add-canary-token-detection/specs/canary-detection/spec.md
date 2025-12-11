## ADDED Requirements

### Requirement: Canary Token Generation
The system SHALL generate unique canary tokens for injection into prompts.

#### Scenario: Generate unicode canary
- **WHEN** user requests a unicode canary
- **THEN** the system generates a unique zero-width character sequence

#### Scenario: Generate semantic canary
- **WHEN** user requests a semantic canary
- **THEN** the system generates a unique but natural-looking phrase

### Requirement: Canary Injection
The system SHALL inject canaries into system prompts at specified locations.

#### Scenario: Inject canary into prompt
- **WHEN** user provides a system prompt
- **THEN** the system injects canary tokens at configurable positions
- **AND** returns the modified prompt and canary registry

### Requirement: Canary Detection
The system SHALL detect canary tokens in LLM outputs.

#### Scenario: Unicode canary detected
- **WHEN** LLM output contains zero-width canary characters
- **THEN** detection result is LEAKED with exact match location

#### Scenario: Semantic canary detected
- **WHEN** LLM output contains semantic canary phrase
- **THEN** detection result is LEAKED with similarity score

#### Scenario: No canary detected
- **WHEN** LLM output contains no canary tokens
- **THEN** detection result is CLEAN

### Requirement: Catastrophic Leak Alert
The system SHALL alert on canary detection with highest severity.

#### Scenario: Alert on leak
- **WHEN** any canary is detected in output
- **THEN** the system raises a CRITICAL alert
- **AND** logs full context for investigation
