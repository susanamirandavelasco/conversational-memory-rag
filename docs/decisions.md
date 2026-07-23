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

## ADR-003

### Decision

The Retriever returns a RetrievalResult instead of a list of strings.

### Rationale

A retrieval operation may evolve to include additional information such as relevance score, metadata, execution time, or retrieval strategy. Returning a domain object keeps the API stable while allowing future evolution.