## ADDED Requirements

### Requirement: CLI Interface
The system SHALL provide a command-line interface for running security evaluations.

#### Scenario: Run evaluation suite
- **WHEN** user executes `eval-fw run --suite prompt-security`
- **THEN** the system executes all tests in the specified suite
- **AND** displays progress to stdout
- **AND** generates a report on completion

#### Scenario: List available suites
- **WHEN** user executes `eval-fw list`
- **THEN** the system displays all available test suites

### Requirement: LLM Provider Abstraction
The system SHALL support multiple LLM providers through a unified interface.

#### Scenario: Configure OpenAI provider
- **WHEN** user configures OpenAI in `config.yaml`
- **THEN** the system uses OpenAI API for evaluations

#### Scenario: Configure local Ollama provider
- **WHEN** user configures Ollama in `config.yaml`
- **THEN** the system uses local Ollama instance for evaluations

#### Scenario: Provider failover
- **WHEN** a provider returns an error
- **THEN** the system logs the error and continues with remaining tests

### Requirement: Test Definition Schema
The system SHALL load test definitions from JSON files.

#### Scenario: Load test suite
- **WHEN** a valid JSON test file is provided
- **THEN** the system parses and validates the test definitions

#### Scenario: Invalid test file
- **WHEN** an invalid JSON test file is provided
- **THEN** the system reports validation errors with line numbers

### Requirement: Report Generation
The system SHALL generate evaluation reports in multiple formats.

#### Scenario: Generate JSON report
- **WHEN** evaluation completes with `--format json`
- **THEN** the system outputs machine-readable JSON results

#### Scenario: Generate HTML report
- **WHEN** evaluation completes with `--format html`
- **THEN** the system generates a styled HTML report with charts

#### Scenario: Generate PDF report
- **WHEN** evaluation completes with `--format pdf`
- **THEN** the system generates a printable PDF report
