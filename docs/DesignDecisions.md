# Design Decisions

This document describes the major architectural decisions made during the development of the Knowledge Retrieval System (KRS) and the reasoning behind each choice.

---

## Why Hybrid Retrieval?

Modern retrieval systems generally rely on one of two approaches:

- Dense semantic retrieval
- Sparse keyword retrieval

Dense retrieval models are highly effective at capturing semantic relationships between queries and documents, allowing the system to retrieve relevant results even when exact keywords do not match.

### Example

**Query**

```text
How are routes registered in FastAPI?
```

**Relevant Document**

```python
def add_api_route(...):
```

Although the query does not explicitly contain `add_api_route`, dense retrieval can identify the semantic similarity.

However, dense retrieval often struggles with:

- Exact identifiers
- Function names
- Class names
- File names
- Version numbers

Sparse retrieval using BM25 performs exceptionally well for these exact-match scenarios.

By combining both approaches, the system benefits from:

- Semantic understanding from dense retrieval
- Lexical precision from BM25 retrieval

This hybrid architecture consistently outperforms either retrieval method in isolation.

---

## Why Reciprocal Rank Fusion (RRF)?

Once dense and sparse retrievers produce independent rankings, their results must be merged into a single ranked list.

Several fusion strategies exist:

- Weighted score averaging
- Learning-to-rank approaches
- Reciprocal Rank Fusion (RRF)

The project uses Reciprocal Rank Fusion (RRF) because:

- It is simple to implement
- It is robust across different retrieval systems
- It requires no score normalization
- It performs competitively with more complex fusion algorithms

RRF rewards documents that appear near the top of multiple ranked lists, producing stable retrieval quality without introducing additional training complexity.

---

## Why ChromaDB?

The project requires a vector database capable of:

- Efficient similarity search
- Metadata filtering
- Local deployment
- Simple integration with Python applications

ChromaDB was selected because it provides:

- Lightweight local deployment
- Native metadata filtering
- Persistent storage
- Straightforward developer experience
- Compatibility with SentenceTransformer embeddings

While alternatives such as Pinecone, Qdrant, and Weaviate provide additional scalability features, ChromaDB offers an excellent balance between functionality and operational simplicity for local repository indexing workloads.

---

## Why CrossEncoder Reranking?

Embedding similarity retrieval is highly effective for candidate generation but is less reliable for precise ranking.

To improve final result quality, the system applies a CrossEncoder reranker after hybrid retrieval.

Unlike bi-encoder embeddings, CrossEncoders jointly process:

- Query
- Candidate document

This allows the model to capture much richer interactions between the query and document content.

The reranker significantly improves:

- Ranking accuracy
- Relevance ordering
- Retrieval precision in top results

The selected model:

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

offers an effective balance between latency and ranking quality.

---

## Why AST-Based Parsing?

Traditional text chunking approaches treat source code as plain text.

This often results in:

- Broken functions
- Incomplete classes
- Loss of structural information
- Poor retrieval quality

The project instead relies on Abstract Syntax Tree (AST) parsing to preserve code semantics.

The parser extracts:

- Files
- Classes
- Methods
- Functions
- Imports
- Constants

This allows retrieval to operate on meaningful semantic units rather than arbitrary text fragments.

AST-based indexing improves:

- Retrieval precision
- Explainability
- Metadata extraction
- Repository understanding

---

## Why Configurable Models?

Embedding models and rerankers evolve rapidly.

Hardcoding model choices would make experimentation difficult and increase maintenance effort.

The system therefore exposes:

- Embedding model selection
- Reranker model selection
- Chunk size limits

through environment configuration.

This allows the retrieval pipeline to adapt to:

- Different repositories
- Different hardware constraints
- Future model upgrades

without requiring code changes.

---

## Why Metadata Filtering?

Semantic similarity alone is often insufficient for code retrieval tasks.

Developers frequently require searches constrained by:

- File path
- Class name
- Method name
- Repository branch
- Repository name

Metadata filtering allows the retrieval system to narrow the search space before ranking, improving both performance and retrieval quality.

Where possible, filtering is delegated directly to ChromaDB to avoid unnecessary post-processing and improve retrieval efficiency.

---

## Why MCP?

The Model Context Protocol (MCP) provides a standardized mechanism for exposing retrieval capabilities to LLM agents.

By exposing retrieval functionality as MCP tools, the system becomes immediately usable by:

- AI coding assistants
- Autonomous agents
- IDE integrations
- Conversational interfaces

This design separates retrieval infrastructure from application logic and improves long-term extensibility.

---

## Summary

The architectural decisions made in KRS prioritize:

- Retrieval quality
- Modularity
- Extensibility
- Configurability
- Developer productivity

The resulting system provides a robust foundation for repository understanding, semantic code search, and future AI-assisted development workflows.