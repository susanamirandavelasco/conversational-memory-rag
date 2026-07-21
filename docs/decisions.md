# Architecture Decisions

## ADR-001

### Decision

Messages are immutable.

### Rationale

A message represents a historical event in a conversation. Once created, it should never change.

## ADR-002

### Decision
Conversation exposes read-only access to messages.

### Rationale
External components can inspect the conversation history, but only the Conversation entity can modify it through add_message().