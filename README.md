# Conversational Memory RAG

A Retrieval-Augmented Generation (RAG) system built from first principles to explore how conversational memory, question rewriting, retrieval, and summarization interact in a multi-turn AI assistant.

The project goes beyond a basic "retrieve → prompt → generate" pipeline by introducing **conversation-aware retrieval**, **long-term memory through summarization**, and a small **evaluation framework for controlled experiments**.

> **Development note:** This project was built by me step by step as a hands-on learning project, with ChatGPT (OpenAI) acting as a technical tutor throughout the process. I implemented the code and made the design decisions while using the tutor to discuss concepts, challenge architectural choices, debug issues, and design evaluation experiments. The goal was not to generate a finished solution, but to understand how each component of a conversational RAG system works by building it incrementally.

## Why I Built This

A basic RAG system can retrieve relevant information for isolated questions, but conversational assistants introduce additional problems:

- What happens when the user refers to something mentioned several turns ago?
- How should a follow-up question be transformed before retrieval?
- How much conversation history should be sent to the model?
- What happens when important information falls outside the recent-message window?
- Does retrieving more chunks actually improve answer quality?
- How can architectural decisions like summarization be evaluated instead of simply assumed to work?

I built this project to understand those problems by implementing the components myself rather than relying on a high-level RAG framework.

The goal was not to build a production chatbot. The goal was to understand and evaluate the architecture behind one.

---

## Architecture

The system separates domain logic, application orchestration, and infrastructure implementations.

```text
User Question
     │
     ▼
Conversation
     │
     ▼
Memory Manager
     │
     ├── Recent Messages
     │
     └── Conversation Summary
              │
              ▼
       Conversation Context
              │
              ▼
       Question Rewriter
              │
              ▼
       Standalone Question
              │
              ▼
           Retriever
              │
              ├── Embedding
              │
              └── Chroma Vector Store
              │
              ▼
        Retrieved Chunks
              │
              ▼
         Prompt Builder
              │
              ├── Conversation Summary
              ├── Recent Messages
              ├── Retrieved Context
              └── User Question
              │
              ▼
           Generator
              │
              ▼
       Assistant Response
```

`ConversationEngine` acts as the main orchestrator.

At a high level, each request follows this flow:

1. The `MemoryManager` builds the conversational context.
2. Older conversation information can be compressed into a summary.
3. The `QuestionRewriter` converts conversational follow-ups into standalone retrieval queries.
4. The `Retriever` performs semantic search over the indexed document corpus.
5. The `PromptBuilder` combines conversational memory and retrieved knowledge.
6. The `Generator` produces the final response.
7. The response is added back to the conversation.

---

## Project Structure

```text
src/conversational_memory_rag/
├── application/
│   ├── conversation_engine.py
│   ├── generator.py
│   ├── ingestion_service.py
│   ├── memory_manager.py
│   ├── prompt_builder.py
│   ├── question_rewriter.py
│   ├── retriever.py
│   └── vector_store.py
│
├── domain/
│   ├── conversation.py
│   ├── conversation_context.py
│   ├── message.py
│   ├── prompt.py
│   ├── retrieval_result.py
│   ├── retrieved_chunk.py
│   ├── role.py
│   └── summary.py
│
├── infrastructure/
│   ├── chroma_retriever.py
│   ├── chroma_vector_store.py
│   ├── embedding_service.py
│   ├── last_messages_memory_manager.py
│   ├── openai_conversation_summarizer.py
│   ├── openai_generator.py
│   └── openai_question_rewriter.py
│
├── ingestion/
│   ├── chunker.py
│   ├── document_loader.py
│   └── ingest.py
│
├── evaluation/
│   ├── evaluation_case.py
│   ├── evaluation_result.py
│   ├── evaluation_runner.py
│   ├── evaluation_score.py
│   ├── llm_judge_evaluator.py
│   ├── memory_cases.py
│   ├── question_rewriter_cases.py
│   ├── retrieval_cases.py
│   └── run_*_experiment.py
│
└── demo/
```

The architecture intentionally uses abstractions such as `Generator`, `Retriever`, `MemoryManager`, and `QuestionRewriter` so infrastructure implementations can be replaced without changing the orchestration logic.

---

## Conversational Memory

One of the main goals of the project was to explore memory beyond simply sending the complete chat history to the LLM.

The implemented strategy keeps a limited window of recent messages while maintaining a compressed summary of the conversation once the recent-message window is exceeded.

Conceptually:

```text
ull Conversation
       │
       ├──────────────► Summarizer ──► Summary
       │
       └── Last 5 Messages
                    │
                    ▼
            ConversationContext
```

This allows the prompt to contain:

- compact long-term conversational information,
- recent conversational turns,
- retrieved document knowledge,
- and the current user question.

For example, an early conversation may contain:

```text
User: My favorite AWS service is Amazon Bedrock.
```

After enough additional turns, that message falls outside the recent-message window.

Without summarization, the system no longer has access to that fact.

With summarization enabled, the information remains available through conversational memory.

This behavior was later tested explicitly through an A/B experiment.

---

## Question Rewriting

Conversational questions are often poor retrieval queries.

For example:

```text
User: Tell me about Amazon Bedrock.
Assistant: ...
User: How much does it cost?
```

Searching the vector database for:

```text
How much does it cost?
```

loses the subject of the conversation.

The `QuestionRewriter` uses the conversation context to produce a standalone query such as:

```text
What is the cost of using Amazon Bedrock?
```

Retrieval is then performed using the rewritten question rather than the raw conversational message.

Question rewriting is implemented as a separate application abstraction so it can be enabled, disabled, or replaced independently.

---

## Retrieval Pipeline

The knowledge corpus is processed through an ingestion pipeline:

```text
PDF
 │
 ▼
Document Loader
 │
 ▼
Chunker
 │
 ▼
Embedding Service
 │
 ▼
Chroma Vector Store
```

At query time:

```text
Question
 │
 ▼
Embedding
 │
 ▼
Vector Search
 │
 ▼
Top-k Retrieved Chunks
```

The current project uses an AWS Bedrock documentation PDF as its experimental corpus.

The document itself and the persisted Chroma database are intentionally excluded from version control.

---

# Evaluation

A major goal of the final development phase was to move from:

> "The architecture seems to work."

to:

> "Can I create experiments that demonstrate how it behaves?"

A lightweight evaluation layer was built around:

- `EvaluationCase`
- `EvaluationResult`
- `EvaluationScore`
- `EvaluationRunner`
- `Evaluator`
- `LLMJudgeEvaluator`

The evaluator compares the expected answer with the actual system response and produces:

```text
passed
score
reason
```

The evaluation uses an LLM-as-a-judge approach for semantic comparison.

The experiments are intentionally small and synthetic. Their purpose is architectural validation and learning, not production benchmarking.

---

## Experiment 1 — Conversational Memory

Five cases were created to test different memory behaviors:

- long-term fact memory,
- recent memory,
- semantic conversational memory,
- resilience to irrelevant conversational noise,
- and absence of information.

### Results

| Metric | Result |
|---|---:|
| Cases | 5 |
| Passed | 5 / 5 |
| Average score | 1.00 |

Examples included remembering that:

```text
My favorite AWS service is Amazon Bedrock.
```

after the original message had moved outside the recent-message window.

Another case verified that the system could correctly answer that no database had been specified rather than inventing one.

### Interpretation

The five synthetic cases passed successfully.

This should **not** be interpreted as 100% system accuracy. The dataset is deliberately small and the evaluator itself is LLM-based.

The result instead provides evidence that the implemented memory architecture behaves as intended for the tested scenarios.

---

## Experiment 2 — Retrieval Top-k

The retrieval pipeline was evaluated using different values for the number of retrieved chunks:

```text
k = 3
k = 5
k = 10
k = 20
```

Three retrieval questions were executed for every configuration.

### Results

| Top-k | Passed |
|---:|---:|
| 3 | 3 / 3 |
| 5 | 3 / 3 |
| 10 | 3 / 3 |
| 20 | 3 / 3 |

### Interpretation

For this small evaluation set, increasing the amount of retrieved context from 3 to 20 chunks produced **no observable improvement in final answer correctness**.

This does not mean that `k=3` is universally optimal.

It means that, for these questions and this corpus, retrieving substantially more context did not improve the evaluated answers.

A more detailed evaluation of chunk relevance, retrieval precision, and context noise is left as future work.

---

## Experiment 3 — Question Rewriter ON vs OFF

The `QuestionRewriter` was evaluated by comparing conversational retrieval with rewriting enabled and disabled.

Example:

```text
Original:
How do they work?

Rewritten:
How do Knowledge Bases for Amazon Bedrock work?
```

### Result

The rewritten queries were clearly more explicit and self-contained.

However, the small evaluation suite did not show a meaningful improvement in final answer correctness: the tested questions could be answered successfully in both configurations.

### Interpretation

Question rewriting improved the **quality of the retrieval query**, but its impact on final answer correctness was inconclusive in this evaluation set.

This is an important distinction: an architectural component can behave as designed without necessarily producing a measurable downstream improvement in every dataset.

More ambiguous conversational references would be useful for evaluating this component further.

---

## Experiment 4 — Summary ON vs OFF

The strongest controlled experiment evaluated the same long-term-memory questions with conversation summarization enabled and disabled.

The relevant facts had already moved outside the five-message recent-memory window.

### Results

| Configuration | Passed |
|---|---:|
| Summary OFF | 0 / 2 |
| Summary ON | 2 / 2 |

With summarization disabled, the system explicitly reported that the required conversational information was unavailable.

For example:

```text
The provided context doesn't mention your favorite AWS service.
```

With summarization enabled:

```text
Your favorite AWS service is Amazon Bedrock.
```

### Interpretation

This experiment demonstrated a direct behavioral effect from conversational summarization.

When the relevant information was outside the recent-message window:

```text
Summary OFF
     │
     ▼
Information unavailable
     │
     ▼
Incorrect / insufficient answer
```

while:

```text
Summary ON
     │
     ▼
Older information compressed into memory
     │
     ▼
Information available to the pipeline
     │
     ▼
Correct answer
```

Unlike simply verifying that a summary object existed, this experiment tested whether the architectural decision affected the final behavior of the system.

---

# Key Design Decisions

## 1. Build from first principles

The project intentionally avoids high-level RAG orchestration frameworks.

This made the implementation longer, but exposed the responsibilities and boundaries between:

- retrieval,
- generation,
- memory,
- summarization,
- question rewriting,
- prompt construction,
- and evaluation.

---

## 2. Keep orchestration separate from infrastructure

`ConversationEngine` does not need to know whether retrieval uses Chroma or another vector store, or whether generation uses OpenAI or another provider.

It coordinates abstractions rather than provider-specific implementations.

This also made controlled experiments easier because components such as question rewriting could be replaced with no-op implementations.

---

## 3. Represent conversation state explicitly

Instead of passing loose strings between components, the system introduces domain objects such as:

- `Conversation`
- `Message`
- `ConversationContext`
- `Summary`
- `Prompt`
- `RetrievalResult`
- `RetrievedChunk`

This makes the flow of information through the pipeline explicit.

---

## 4. Treat memory as context management

The system does not attempt to store the entire conversation indefinitely.

Instead, memory is treated as a context-management problem:

```text
recent detail + compressed historical information
```

This keeps the memory mechanism independent from generation.

---

## 5. Evaluate architectural choices independently

The evaluation phase intentionally changes one variable at a time when possible.

Examples:

```text
top-k = 3 vs 5 vs 10 vs 20

Question Rewriter = ON vs OFF

Summary = ON vs OFF
```

This makes it easier to reason about why system behavior changes.

---

# Tech Stack

- Python 3.12
- OpenAI API
- OpenAI embeddings
- ChromaDB
- pypdf
- `dataclasses`
- Abstract Base Classes for application boundaries

---

# Running the Project

## 1. Clone the repository

```bash
git clone <repository-url>
cd conversational-memory-rag
```

## 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```bash
.venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Configure the OpenAI API key

Create a `.env` file or export the environment variable:

```bash
export OPENAI_API_KEY="your-api-key"
```

Never commit API keys to the repository.

## 5. Provide the document corpus

Place the source PDF in:

```text
data/bedrock-ug.pdf
```

The PDF is intentionally not included in the repository.

## 6. Run ingestion

```bash
python -m conversational_memory_rag.ingestion.ingest
```

This loads the document, generates chunks and embeddings, and persists them in ChromaDB.

## 7. Run the conversational demo

```bash
python -m conversational_memory_rag.demo.demo_engine
```

---

# Running the Evaluations

## Memory evaluation

```bash
python -m conversational_memory_rag.evaluation.run_memory_evaluation
```

## Retrieval top-k experiment

```bash
python -m conversational_memory_rag.evaluation.run_retrieval_experiment
```

## Question Rewriter experiment

```bash
python -m conversational_memory_rag.evaluation.run_question_rewriter_experiment
```

## Summary ON/OFF experiment

```bash
python -m conversational_memory_rag.evaluation.run_summary_experiment
```

These evaluations make multiple LLM/API calls and therefore may incur API usage costs.

Because hosted LLM behavior can vary between executions, exact generated wording may also differ between runs.

---

# Limitations

This project is an educational and portfolio implementation rather than a production-ready RAG platform.

Current limitations include:

- Small synthetic evaluation datasets.
- LLM-as-a-judge is not an objective ground-truth evaluator.
- Retrieval evaluation focuses primarily on final-answer correctness rather than detailed chunk relevance.
- No systematic latency or token-cost benchmarking.
- Conversation summaries may lose information as conversations become substantially longer.
- Question rewriting has only been evaluated on a small number of conversational references.
- The experimental corpus is limited to a single documentation source.
- No production API, authentication, observability, or user interface is included.

---

# Future Work

Possible extensions include:

- Retrieval precision/recall evaluation.
- Retrieved-chunk relevance scoring.
- Larger evaluation datasets.
- More adversarial conversational-memory tests.
- Token and latency measurements.
- Cost analysis.
- Summary quality evaluation.
- More ambiguous Question Rewriter experiments.
- Alternative embedding models or vector stores.
- Automated regression evaluation.
- Tool calling and agent-style workflows.

These are intentionally outside the scope of v1.0.

---

# What I Learned

The most important lesson from this project was that building a conversational RAG system is not primarily about calling an LLM.

The difficult and interesting questions are architectural:

- What information should reach the model?
- What information should reach the retriever?
- How should conversation history be compressed?
- Which component owns each transformation?
- How can a component be replaced without changing the whole pipeline?
- How do we know whether an architectural decision actually improves behavior?

Building the system from first principles made those boundaries visible.

The evaluation phase added another important lesson:

> A component working as designed does not automatically mean it improves the final answer.

Increasing top-k did not improve the tested answers. Question rewriting produced better standalone queries but no clear improvement in final correctness. In contrast, summarization produced a directly measurable difference when relevant information moved outside the recent-message window.

That distinction between **implementation, behavior, and measurable impact** is the main takeaway from the project.

---

## Status

**v1.0 — Complete**

The core conversational RAG pipeline, conversational memory, question rewriting, document ingestion, vector retrieval, generation, and evaluation experiments are implemented.