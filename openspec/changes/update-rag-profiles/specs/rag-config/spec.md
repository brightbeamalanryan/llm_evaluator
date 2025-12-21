## ADDED Requirements
### Requirement: RAG profiles list
The system SHALL accept RAG configuration as a list of profiles under `rag.profiles`, each with a unique `name` and optional `active` flag.

#### Scenario: Profile list parsed
- **WHEN** the configuration provides `rag.profiles` with two named profiles
- **THEN** the system loads both profiles and preserves each profile name

### Requirement: Profile-specific endpoints and request profile
Each RAG profile SHALL define its own endpoint settings (`query_endpoint`, `retrieve_endpoint`, `ingest_endpoint`, `endpoint_mode`) and MAY define a `request_profile` for query requests.

#### Scenario: Host-specific schema
- **WHEN** a profile defines a `request_profile` and custom `query_endpoint`
- **THEN** the system uses those values for that profile's queries

### Requirement: Active profile execution and selection
The system SHALL run RAG tests against profiles marked `active: true` by default, and SHALL allow CLI selection of one or more profiles by name to override the active set.

#### Scenario: Active profiles drive execution
- **WHEN** two profiles are marked active and no CLI selection is provided
- **THEN** the system executes tests for both profiles

#### Scenario: CLI selection overrides active flags
- **WHEN** the CLI specifies a profile name
- **THEN** the system executes tests only for the selected profile(s)

### Requirement: Profile naming for logging and reporting
The system SHALL include the profile name in log and report labeling for RAG test runs.

#### Scenario: Logs include profile name
- **WHEN** a RAG test run starts for a profile
- **THEN** the log entries include that profile name

### Requirement: Legacy service URL removal
The system SHALL reject `rag.service_url` and legacy endpoint fields when `rag.profiles` is used, and SHALL provide a validation error that points to the new profile schema.

#### Scenario: Legacy config rejected
- **WHEN** the configuration includes `rag.service_url`
- **THEN** the system raises a validation error describing the `rag.profiles` replacement
