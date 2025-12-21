## ADDED Requirements
### Requirement: Default guard expectation
The system SHALL apply a default guard expectation that defines baseline leakage and refusal behavior for all RAG tests.

#### Scenario: Default expectation applied
- **WHEN** a RAG test case is scored
- **THEN** the guard prompt includes the default expectation alongside the test-specific expectation

### Requirement: Combined expectation prompt
The system SHALL combine the default guard expectation with the test case expectation when asking the guard LLM to decide pass or fail.

#### Scenario: Test-specific expectation appended
- **WHEN** a test case defines an expectation
- **THEN** the guard evaluates the response against the combined expectations

### Requirement: Guard pass/fail decision
The guard LLM SHALL return a verdict and severity that reflect whether the response passes the combined expectation.

#### Scenario: Response violates combined expectation
- **WHEN** a response includes content that violates the default expectation or the test expectation
- **THEN** the guard returns a BLOCK verdict with a non-zero severity score
