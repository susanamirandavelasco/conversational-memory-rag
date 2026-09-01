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

## ADR-004

### Decision

Introduce a MemoryManager abstraction responsible for selecting the conversational context provided to the LLM.

### Rationale

Different memory strategies may be required depending on conversation length or token limits. Encapsulating this decision allows new strategies to be introduced without modifying the ConversationEngine.

## ADR-005

### Decision

Question rewriting is implemented as an independent application abstraction.

### Rationale

Conversational questions may depend on previous turns and therefore be poor retrieval queries on their own.

Separating question rewriting from retrieval allows the system to transform the query without coupling this behavior to the vector store or retriever implementation. It also makes the component independently replaceable and testable.

## ADR-006

### Decision

Conversation summaries are represented explicitly in the domain through `Summary` and `ConversationContext`.

### Rationale

Conversational memory is part of the information available to the application, not an implementation detail of the LLM provider.

Representing it explicitly makes the flow of memory through the pipeline visible and avoids hiding conversational state inside prompts or infrastructure components.

## ADR-007

### Decision

`ConversationEngine` acts as an orchestrator rather than implementing component behavior directly.

### Rationale

Memory management, question rewriting, retrieval, prompt construction, and generation represent different decisions and responsibilities.

Keeping these responsibilities outside the engine reduces coupling and allows individual components to be replaced without changing the orchestration flow.

## ADR-008

### Decision

Evaluation is implemented outside the conversational pipeline.

### Rationale

Evaluation should observe system behavior rather than become part of production behavior.

Separating `EvaluationRunner`, `Evaluator`, and `EvaluationScore` from `ConversationEngine` also allows the same application pipeline to be evaluated under different configurations.

## ADR-009

### Decision

Use controlled A/B experiments to evaluate configurable architectural components.

### Rationale

Changing one variable at a time makes it easier to attribute behavioral differences to a specific architectural decision.

This approach was used to compare:

- different retrieval top-k values,
- Question Rewriter ON vs OFF,
- Summary ON vs OFF.

The experiments are intentionally small and are intended for architectural validation rather than production benchmarking.