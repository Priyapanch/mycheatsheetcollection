Yes. What you need is not a **“code conversion prompt”**. You need an **Engineering Adaptation / Productionization prompt** that tells the AI:

> “Take an existing linear GenAI/RAG implementation and transform it into an engineered, testable, modular, CI/CD-ready solution without losing the original business behavior.”

I would use the following as the master prompt.

# Role

Act as a **Senior GenAI Engineer + RAG Architect + Python Test Engineer + DevOps Engineer**.

You are given an existing **linear RAG implementation** generated from documentation, a tutorial, an LLM, or a proof of concept.

Your job is NOT to simply refactor the code.

Your job is to perform **Engineering Adaptation**:

> Transform the linear RAG code into a modular, testable, observable, configurable and CI/CD-ready RAG application while preserving the original business intent.

---

# INPUT

I will provide:

1. Existing RAG source code
2. Documentation/examples used to create the code
3. Optional configuration files
4. Optional sample documents/data

First analyze the existing implementation before modifying it.

---

# PHASE 1 — UNDERSTAND THE EXISTING RAG

Identify and document:

* LLM being used
* embedding model
* vector store
* document loader
* chunking strategy
* retrieval mechanism
* prompt construction
* generation logic
* configuration
* external dependencies
* hard-coded values
* secrets
* missing error handling
* missing tests
* missing observability
* vendor-specific dependencies

Create a mapping:

| Existing Code     | Current Responsibility | Engineering Gap   | Target Component |
| ----------------- | ---------------------- | ----------------- | ---------------- |
| document loading  | Load documents         | tightly coupled   | DocumentLoader   |
| split logic       | Chunk documents        | hard-coded        | Chunker          |
| embedding call    | Generate embeddings    | provider-specific | EmbeddingService |
| similarity search | Retrieve context       | tightly coupled   | Retriever        |
| LLM call          | Generate answer        | tightly coupled   | LLMService       |

Do not modify code until this analysis is complete.

---

# PHASE 2 — TARGET ARCHITECTURE

Transform the linear implementation into the following logical architecture:

```text
                    ┌──────────────────────┐
                    │      User Query      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │    RAG Orchestrator  │
                    └──────────┬───────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
       ┌────────────────┐           ┌─────────────────┐
       │ Query Processor│           │  Prompt Builder │
       └───────┬────────┘           └────────┬────────┘
               │                             │
               ▼                             │
       ┌────────────────┐                    │
       │   Retriever    │◄───────────────────┘
       └───────┬────────┘
               │
               ▼
       ┌────────────────┐
       │ Vector Store   │
       └───────┬────────┘
               │
               ▲
               │
       ┌───────┴────────┐
       │   Embeddings   │
       └───────┬────────┘
               ▲
               │
       ┌────────────────┐
       │    Chunker     │
       └───────┬────────┘
               ▲
               │
       ┌────────────────┐
       │ DocumentLoader │
       └────────────────┘

               RAG Response
                     │
                     ▼
              ┌────────────┐
              │ Evaluation │
              │   RAGAS    │
              └────────────┘
```

---

# PHASE 3 — CHUNKER ENGINEERING

Extract the document chunking logic into a dedicated component.

Create:

```text
Chunker
```

Requirements:

* configurable chunk size
* configurable overlap
* deterministic behavior
* metadata preservation
* document ID preservation
* source information preservation
* unit tests
* ability to replace the chunking strategy

Example interface:

```python
class Chunker:
    def chunk(self, documents):
        ...
```

Do not hard-code chunking parameters inside the business logic.

---

# PHASE 4 — EMBEDDING ENGINEERING

Extract embeddings into a dedicated abstraction.

Create:

```text
EmbeddingService
```

Requirements:

* configurable embedding provider
* configurable model
* configurable API endpoint
* configurable credentials
* batching where supported
* retry/error handling
* testability without calling the real embedding API

Example:

```python
class EmbeddingService:
    def embed_documents(self, documents):
        ...

    def embed_query(self, query):
        ...
```

The application must not directly instantiate an embedding provider throughout the codebase.

Use dependency injection/configuration.

---

# PHASE 5 — RETRIEVER ENGINEERING

Extract retrieval into:

```text
Retriever
```

Requirements:

* configurable top-k
* configurable similarity/search strategy
* metadata filtering
* deterministic response structure
* ability to replace vector database
* unit-testable without external infrastructure

Example:

```python
class Retriever:
    def retrieve(self, query, top_k=None):
        ...
```

Return structured results containing at least:

```text
document
content
metadata
score
```

---

# PHASE 6 — RAG ORCHESTRATION

Create a dedicated RAG orchestration layer.

Example:

```python
class RAGPipeline:

    def ingest(self, documents):
        ...

    def query(self, question):
        ...
```

The orchestrator should coordinate:

```text
DocumentLoader
       ↓
Chunker
       ↓
EmbeddingService
       ↓
VectorStore
       ↓
Retriever
       ↓
PromptBuilder
       ↓
LLMService
       ↓
Response
```

Do not put all of this logic in `main.py`.

---

# PHASE 7 — LLM ABSTRACTION

Create:

```text
LLMService
```

The RAG application should not directly depend on a specific LLM provider.

Support configuration such as:

```text
LLM_PROVIDER=
LLM_MODEL=
LLM_API_BASE_URL=
LLM_API_KEY=
LLM_VERIFY_SSL=false
```

If an OpenAI-compatible custom gateway is required, support:

```text
Custom Application
        ↓
LLMService
        ↓
OpenAI-compatible client
        ↓
Custom LLM API Gateway
        ↓
LLM
```

Keep provider-specific implementation behind the abstraction.

---

# PHASE 8 — RAGAS EVALUATION

Add an evaluation layer using **RAGAS**.

Create evaluation datasets containing:

```text
question
ground_truth
retrieved_context
generated_answer
```

Evaluate appropriate RAG metrics such as:

* faithfulness
* answer relevancy
* context precision
* context recall

Do not blindly add every available metric.

Select metrics appropriate to the available ground truth and test scenario.

Create:

```text
tests/
evaluation/
```

with a clear separation between:

### Unit tests

Test individual components:

```text
Chunker
EmbeddingService
Retriever
PromptBuilder
RAGPipeline
```

### RAG evaluation tests

Evaluate complete RAG behavior using RAGAS.

Do not make every unit test dependent on a live LLM.

Mock external services wherever appropriate.

---

# PHASE 9 — TEST PYRAMID

Implement the following test strategy:

```text
                 ┌──────────────┐
                 │ RAGAS / E2E  │
                 └───────▲──────┘
                         │
                 ┌───────┴──────┐
                 │ Integration   │
                 └───────▲──────┘
                         │
              ┌──────────┴──────────┐
              │     Unit Tests      │
              └─────────────────────┘
```

Provide:

* unit tests
* integration tests
* RAG evaluation tests
* smoke test

Clearly identify which tests require:

```text
REAL_LLM=true
```

and which tests can run offline.

---

# PHASE 10 — GITHUB INTEGRATION

Prepare the project for GitHub.

Create:

```text
.gitignore
README.md
requirements.txt or pyproject.toml
.github/
```

README must include:

* architecture
* setup
* environment variables
* local execution
* testing
* RAGAS evaluation
* CI/CD
* troubleshooting

Never commit:

```text
API keys
.env
credentials
cloud secrets
```

---

# PHASE 11 — CLAUDE / CODING-ASSISTANT INTEGRATION

If the project is intended to be developed using Claude or another coding agent, create appropriate project-level engineering guidance.

Provide:

```text
CLAUDE.md
```

or equivalent project instructions.

It should explain:

* architecture
* coding conventions
* testing requirements
* RAG design rules
* where new components should be placed
* how tests should be written
* forbidden practices
* how to run the project

The instructions must prevent the coding agent from collapsing the architecture back into one linear script.

---

# PHASE 12 — AWS INTEGRATION

Design the project so cloud dependencies are replaceable.

Identify appropriate AWS integration points, for example:

```text
S3
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
Vector Store
│
▼
Retriever
│
▼
LLMService
```

If AWS Bedrock is appropriate for the existing use case, isolate it behind the LLM/embedding abstractions.

Do not hard-code AWS-specific implementation throughout the application.

Use configuration/environment variables.

Provide local and AWS-compatible configurations where practical.

---

# PHASE 13 — GITHUB ACTIONS CI/CD

Create:

```text
.github/workflows/ci.yml
```

The pipeline should perform:

```text
Checkout
   ↓
Setup Python
   ↓
Install dependencies
   ↓
Lint
   ↓
Unit Tests
   ↓
Integration Tests
   ↓
RAGAS Evaluation
   ↓
Build/Package
```

Separate tests requiring external credentials from tests that can run in CI without secrets.

The default CI pipeline must NOT fail merely because an external LLM API key is unavailable.

Use environment variables/secrets for external integrations.

---

# PHASE 14 — QUALITY GATES

Define CI quality gates.

Example:

```text
Unit tests             → MUST PASS
Linting                → MUST PASS
Import validation      → MUST PASS
Smoke test             → MUST PASS
Integration tests      → configured separately
RAGAS evaluation       → threshold-based
```

Define configurable RAG evaluation thresholds.

Do not invent arbitrary thresholds without clearly marking them as initial/project-specific thresholds.

---

# PHASE 15 — OBSERVABILITY

Add structured logging around:

```text
Document ingestion
Chunk creation
Embedding
Retrieval
LLM invocation
Response generation
RAG evaluation
```

Capture useful metadata such as:

```text
request_id
document_count
chunk_count
retrieved_documents
retrieval_scores
model
latency
evaluation_score
```

Never log:

```text
API keys
tokens/secrets
sensitive document content
```

unless explicitly required and safe.

---

# PHASE 16 — CONFIGURATION

Centralize configuration.

Use:

```text
.env
```

for local development.

Provide:

```text
.env.example
```

with placeholders.

Example:

```text
LLM_PROVIDER=
LLM_MODEL=
LLM_API_BASE_URL=
LLM_API_KEY=
LLM_VERIFY_SSL=false

EMBEDDING_PROVIDER=
EMBEDDING_MODEL=

VECTOR_STORE=
TOP_K=5

CHUNK_SIZE=500
CHUNK_OVERLAP=50

AWS_REGION=
AWS_PROFILE=
```

Do not hard-code credentials or infrastructure-specific values.

---

# PHASE 17 — PROJECT STRUCTURE

Create a professional structure similar to:

```text
rag-application/
│
├── src/
│   ├── config/
│   ├── ingestion/
│   │   ├── loader.py
│   │   └── chunker.py
│   │
│   ├── embeddings/
│   │   └── service.py
│   │
│   ├── retrieval/
│   │   └── retriever.py
│   │
│   ├── llm/
│   │   └── service.py
│   │
│   ├── rag/
│   │   └── pipeline.py
│   │
│   └── evaluation/
│       └── ragas_evaluator.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── evaluation/
│
├── data/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── .env.example
├── .gitignore
├── CLAUDE.md
├── README.md
├── requirements.txt
└── pyproject.toml
```

Adapt this structure if the existing application requires something different.

---

# PHASE 18 — ENGINEERING ADAPTATION RULES

Follow these rules strictly.

### Rule 1 — Preserve intent

Do not change the original business behavior unless required for engineering quality.

### Rule 2 — Separate responsibilities

Do not leave the RAG implementation as one linear script.

### Rule 3 — Abstract external dependencies

LLM, embeddings, vector database and cloud services must be replaceable.

### Rule 4 — Testability first

Every major component must be independently testable.

### Rule 5 — Configuration over hard-coding

Move model names, endpoints, credentials and tunable parameters to configuration.

### Rule 6 — No fake validation

Do not claim that code works unless it has actually been executed or clearly state that it has only undergone static validation.

### Rule 7 — No unnecessary complexity

Do not introduce frameworks or infrastructure merely because they are available.

Every component must have a reason to exist.

---

# FINAL DELIVERABLE

Return the result in this order:

## 1. Engineering Assessment

Explain:

* what the original code does
* current architecture
* major engineering gaps
* risks

## 2. Target Architecture

Provide a Mermaid architecture diagram.

## 3. Engineering Adaptation Matrix

```text
Existing Component
→ Target Component
→ Reason
→ Implementation
→ Test Strategy
```

## 4. Final Project Structure

Show the complete directory tree.

## 5. Implementation

Provide the complete files required to make the project runnable.

## 6. Test Strategy

Show:

```text
Unit
Integration
RAGAS
Smoke
CI
```

## 7. GitHub Actions

Provide the complete workflow.

## 8. AWS Integration Strategy

Clearly separate:

```text
Local
AWS
```

configuration.

## 9. Claude/Coding-Agent Instructions

Provide `CLAUDE.md`.

## 10. Execution Commands

Give exact commands:

```bash
install
configure
run
test
evaluate
```

## 11. Validation Report

For every component classify:

```text
PASS
PARTIAL
NOT VALIDATED
BLOCKED
```

Do not claim runtime success without actual execution.

## 12. Engineering Adaptation Summary

Finally explain:

**What was preserved from the original RAG code?**

**What was engineered differently?**

**Why was each adaptation necessary?**

**What remains to be validated in a real environment?**

### Why I would use this version

The key difference is that you're asking the AI to perform **six transformations simultaneously**:

```text
Linear RAG
   │
   ├──► Modular Architecture
   │
   ├──► Embedding abstraction
   │
   ├──► Chunking abstraction
   │
   ├──► Retriever abstraction
   │
   ├──► RAGAS evaluation
   │
   ├──► GitHub / Claude engineering workflow
   │
   ├──► AWS-ready architecture
   │
   └──► GitHub Actions CI/CD
            │
            ▼
     Engineering-grade RAG
```

And importantly, the prompt tells the model **not to blindly "improve" the code**. It first has to establish what the original code does, then map **original implementation → engineering adaptation → reason → test strategy**.

That distinction is what makes this useful as an **enterprise QE/GenAI workshop pattern**, rather than just another code-generation prompt.