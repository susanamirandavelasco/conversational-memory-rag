# Architecture Decisions

## ADR-001

### Decision

Messages are immutable.

### Rationale

A message represents a historical event in a conversation. Once created, it should never change.