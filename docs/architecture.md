# Architecture

Conversational Memory RAG follows a layered architecture that separates domain concepts, application responsibilities, and infrastructure-specific implementations.

The main goal of this separation is to make the conversational pipeline explicit and allow individual components to evolve or be replaced independently.

## High-Level Flow

```text
Conversation
     │
     ▼
MemoryManager
     │
     ▼
ConversationContext
     │
     ▼
QuestionRewriter
     │
     ▼
Retriever
     │
     ▼
RetrievalResult
     │
     ▼
PromptBuilder
     │
     ▼
Prompt
     │
     ▼
Generator
     │
     ▼
Assistant Response
```

`ConversationEngine` orchestrates this flow but delegates each responsibility to a specialized component.

---

## Domain Layer

The domain layer models information that flows through the system without depending on OpenAI, ChromaDB, or other infrastructure.

Main domain objects include:

- `Conversation` — owns the conversation history.
- `Message` — represents one conversational turn.
- `Role` — identifies the message role.
- `ConversationContext` — contains the context selected for the current request, including recent messages, optional summary, and rewritten question.
- `Summary` — represents compressed conversational memory.
- `Prompt` — represents the final prompt sent to the generator.
- `RetrievedChunk` — represents one retrieved piece of document context.
- `RetrievalResult` — groups retrieved chunks.

---

## Application Layer

The application layer defines the responsibilities required by the conversational pipeline.

Important abstractions include:

### MemoryManager

Selects the conversational information that should be available for the current request.

The current implementation keeps the last five messages and, once the conversation exceeds that window, generates a summary of the conversation.

### QuestionRewriter

Transforms a context-dependent conversational question into a standalone retrieval query.

Example:

```text
How do they work?
```

may become:

```text
How do Knowledge Bases for Amazon Bedrock work?
```

### Retriever

Retrieves document knowledge relevant to the current question.

It returns a `RetrievalResult` rather than exposing vector-database-specific structures to the rest of the application.

### PromptBuilder

Combines conversational context and retrieved knowledge into the prompt used for generation.

### Generator

Generates the assistant response from the constructed prompt.

### ConversationEngine

Acts as the application orchestrator.

It coordinates the components but does not implement retrieval, memory, rewriting, or generation itself.

---

## Infrastructure Layer

The infrastructure layer provides concrete implementations of application abstractions.

Current implementations include:

- `OpenAIGenerator`
- `OpenAIQuestionRewriter`
- `OpenAIConversationSummarizer`
- `EmbeddingService`
- `ChromaRetriever`
- `ChromaVectorStore`
- `LastMessagesMemoryManager`

No-op and mock implementations are also used for demos and controlled evaluation experiments.

This separation allows experiments such as Question Rewriter ON/OFF or Summary ON/OFF without modifying `ConversationEngine`.

---

## Conversational Memory

The memory strategy combines a recent-message window with a generated conversation summary.

```text
Full Conversation
       │
       ├──────────────► Summarizer ──► Summary
       │
       └── Last 5 Messages
                    │
                    ▼
             ConversationContext
```

The summary provides compressed historical information while recent messages preserve local conversational detail.

In the current v1.0 implementation, once the conversation exceeds the recent-message window, the summarizer receives the full conversation.

A possible future optimization is to summarize only the information outside the recent-message window and maintain an incremental summary.

---

## Retrieval

Documents are ingested separately from the conversational pipeline.

```text
PDF
 │
 ▼
DocumentLoader
 │
 ▼
Chunker
 │
 ▼
EmbeddingService
 │
 ▼
ChromaVectorStore
```

At query time, the rewritten question is embedded and used to retrieve the top-k semantically similar chunks.

The number of retrieved chunks is configurable through `ConversationEngine`.

---

## Evaluation Architecture

Evaluation is implemented separately from the production pipeline.

```text
EvaluationCase
      │
      ▼
EvaluationRunner
      │
      ├──► ConversationEngine
      │
      ▼
EvaluationResult
      │
      ▼
Evaluator
      │
      ▼
EvaluationScore
```

`LLMJudgeEvaluator` provides the current semantic evaluator.

The same evaluation infrastructure is reused for:

- conversational-memory cases,
- retrieval top-k experiments,
- Question Rewriter ON/OFF,
- Summary ON/OFF.

This allows architectural choices to be evaluated without embedding evaluation logic inside the conversational pipeline.