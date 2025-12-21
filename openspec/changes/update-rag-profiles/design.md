## Context
The RAG client currently supports a single request profile with a legacy service URL fallback. The configuration must scale to multiple RAG hosts, each with its own schema (request profile and endpoints), and optionally run evaluations against multiple hosts in the same run.

## Goals / Non-Goals
- Goals:
  - Support a list of named RAG profiles, each with endpoints and request profile settings.
  - Allow selecting profiles via `active` flags and CLI overrides.
  - Label logs and reports with the profile name to distinguish parallel runs.
  - Remove legacy `rag.service_url` and endpoint fields.
- Non-Goals:
  - No changes to the RAG HTTP request/response format beyond using profile-specific settings.
  - No automatic migration tooling beyond validation errors and guidance.

## Decisions
- Decision: Introduce `rag.profiles: [ { name, active, request_profile, query_endpoint, retrieve_endpoint, ingest_endpoint, endpoint_mode } ]` as the only supported configuration shape.
  - Rationale: Profiles align configuration with multiple hosts and avoid split legacy vs profile logic.
- Decision: Active selection rules
  - Default: run all profiles where `active: true`.
  - CLI override: `--rag-profile` selects one or more profiles and bypasses `active` flags.
  - Validation: error if no active profiles and no CLI selection.
- Decision: Logging and reporting
  - Include `profile.name` in log fields/labels and report identifiers to differentiate runs.

## Risks / Trade-offs
- Breaking removal of `service_url` may require users to update configs; mitigate with clear validation errors and updated example docs.
- Running multiple profiles increases runtime; ensure logs and output clearly attribute results to a profile.

## Migration Plan
- Update docs and example config to use `rag.profiles`.
- Validate and error on any legacy `rag.service_url` usage with a message that points to the new schema.

## Open Questions
- None (requirements confirmed by requester).
