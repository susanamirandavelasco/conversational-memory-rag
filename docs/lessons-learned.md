# Lessons Learned

This project was built incrementally as a hands-on exercise to understand conversational RAG architecture from first principles.

These are the main lessons I want to keep from the process.

## Project setup matters earlier than expected

For Python projects using a `src/` layout, installing the package in editable mode (`pip install -e .`) from the beginning avoids unnecessary import and execution problems.

This was one of the first practical lessons of the project.

---

## Components should encapsulate decisions

One of the earliest architectural lessons was:

> Components should exist because they encapsulate decisions, not simply because they store data.

This became a useful criterion when deciding whether concepts such as retrieval, memory management, question rewriting, and prompt construction deserved separate components.

---

## RAG is more than vector search

At the beginning, RAG can appear to be primarily:

```text
question → embedding → vector search → LLM
```

Building the complete conversational pipeline showed that retrieval is only one part of the problem.

A conversational RAG system also needs to decide:

- what conversational information to preserve,
- what information the retriever should see,
- how references from previous turns should be resolved,
- how retrieved knowledge and conversational memory should be combined,
- and how each of those decisions can be evaluated.

---

## Conversation history and retrieval queries are different things

The LLM may need conversation history to understand the user, while the retriever often needs a self-contained query.

This is why question rewriting became a separate responsibility.

A question such as:

```text
How do they work?
```

may make sense inside a conversation but is a weak semantic-search query without its conversational subject.

---

## Memory is a context-management problem

Keeping every message forever is not the only way to implement conversational memory.

This project explored a combination of:

```text
recent messages + compressed conversation summary
```

The Summary ON/OFF experiment made this lesson particularly concrete: once information moved outside the recent-message window, the summary could preserve information that otherwise became unavailable to the final generation step.

---

## More retrieved context is not automatically better

The top-k experiment compared:

```text
3, 5, 10, and 20 retrieved chunks
```

All configurations passed the small retrieval evaluation set.

For these cases, retrieving substantially more context did not improve final answer correctness.

This does not establish an optimal top-k value, but it challenged the assumption that more retrieved context necessarily produces a better answer.

---

## A better intermediate step does not guarantee a better final answer

Question rewriting produced clearer standalone retrieval queries.

However, in the small evaluation set, this improvement did not translate into a clear improvement in final answer correctness.

That distinction was important:

> A component can work as designed without producing a measurable downstream improvement in every scenario.

---

## Evaluation changes how I think about architecture

Before the evaluation phase, it was possible to say:

> "The memory component works."

After implementing controlled experiments, a better question became:

> "What changes in observable system behavior when this component is enabled?"

The Summary ON/OFF experiment was the clearest example:

```text
Summary OFF → 0/2
Summary ON  → 2/2
```

This provided stronger evidence than simply inspecting the generated summary.

---

## Small experiments can still be useful

The evaluation dataset in this project is too small to make claims about production accuracy.

However, it was sufficient to test hypotheses about architecture.

This helped distinguish between:

- functional verification,
- architectural experimentation,
- and production benchmarking.

They are not the same thing.

---

## Building from first principles was slower — and that was the point

Using a high-level RAG framework could have produced a working pipeline much faster.

Implementing the components directly exposed questions that a framework might otherwise hide:

- Who owns conversational state?
- Who decides what reaches retrieval?
- Where should rewriting happen?
- What belongs in the domain?
- What belongs in infrastructure?
- How should components communicate?
- How can one component be disabled without rewriting the pipeline?

For this project, understanding those boundaries was more valuable than minimizing the amount of code.

---

## Main takeaway

The biggest lesson from this project is that the quality of a GenAI application depends on more than the model.

Architecture determines:

```text
what the model knows
+
what the retriever searches for
+
what context is preserved
+
how evidence is assembled
```

Evaluation then helps determine whether those architectural choices actually change system behavior.