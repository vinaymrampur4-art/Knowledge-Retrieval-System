# Knowledge Retrieval System (KRS)

A hybrid code retrieval system that indexes Python repositories and provides semantic and keyword-based code search through an MCP (Model Context Protocol) server.

The system combines AST-based parsing, vector embeddings, BM25 retrieval, reranking, and metadata filtering to enable efficient repository exploration and code understanding.

---

## Features

- AST-based repository parsing
- Semantic AST-aware code chunking
- Configurable chunk splitting
- Dense semantic retrieval using BGE embeddings
- BM25 keyword retrieval
- Hybrid retrieval pipeline
- Reciprocal Rank Fusion (RRF)
- CrossEncoder reranking
- Metadata filtering
- Native ChromaDB metadata filtering
- ChromaDB vector storage
- Repository statistics and reports
- MCP server integration
- Configurable embedding models
- Configurable reranker models
- Repository exploration tools

---

## Retrieval Pipeline

```text
Repository
    ↓
Repository Parser
    ↓
AST Parsing
    ↓
Document Generation
    ↓
Embedding Generation
    ↓
BM25 Index + ChromaDB Index
    ↓
Dense Retrieval + BM25 Retrieval
    ↓
Reciprocal Rank Fusion (RRF)
    ↓
CrossEncoder Reranker
    ↓
Metadata Filtering
    ↓
MCP Server
```

---

## Project Structure

```text
Knowledge-Retrieval-System/

├── app/
│   ├── chunker/
│   ├── core/
│   ├── embedding/
│   ├── exporter/
│   ├── indexing/
│   ├── parser/
│   ├── reports/
│   ├── retrieval/
│   ├── services/
│   └── vectordb/
│
├── mcp_server/
│
├── repositories/
│
├── tests/
│
├── outputs/
│
├── README.md
├── requirements.txt
└── .env
```

---

## Technologies Used

- Python
- FastMCP
- ChromaDB
- Sentence Transformers
- BAAI BGE Small Embeddings
- CrossEncoder
- BM25
- FastAPI
- Tree-Sitter
- Pydantic
- HuggingFace Transformers

---

## Installation

Clone the repository:

```bash
git clone https://github.com/vinaymrampur4-art/Knowledge-Retrieval-System.git
```

Move into the project directory:

```bash
cd Knowledge-Retrieval-System
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment:

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Configuration

Project configuration is managed through the `.env` file.

Example:

```env
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5

RERANKER_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2

CHROMA_DB_PATH=chroma_db

DEFAULT_TOP_K=5

MAX_RESULTS=20

CHUNK_MAX_TOKENS=500
```

---

## Building the Index

Generate BM25 indexes and vector embeddings:

```bash
python -m tests.test_index_pipeline
```

---

## Running the MCP Server

Start the MCP server:

```bash
python -m mcp_server.server
```

Default configuration:

```text
Host: 127.0.0.1
Port: 8000
Endpoint: /mcp
```

---

## MCP Tools

The MCP server currently provides:

### Search Tools

- Search Repository
- Search Methods
- Search Classes
- Search Functions
- Search Files
- Search Code Blocks

### Lookup Tools

- Lookup by ID
- Lookup by Metadata Attributes

### Reporting Tools

- Repository Statistics
- Repository Reports
- File Reports
- Branch Reports
- Class Reports
- Method Reports
- Complete Repository Dashboard

---

## Indexed Collections

The retrieval system maintains multiple collections to improve retrieval quality.

- Files Collection
- Classes Collection
- Methods Collection
- Functions Collection
- Code Blocks Collection

Hybrid retrieval searches across these collections and merges results using Reciprocal Rank Fusion (RRF).


## Chunking

The system includes an AST-aware semantic chunking engine.

Chunk types include:

- Classes
- Methods
- Functions
- Imports
- Constants

Large semantic chunks are automatically split into embedding-sized chunks using configurable token limits.

Chunk splitting preserves code structure by splitting on line boundaries rather than exact token boundaries.

## Supported Metadata Filters

The retrieval engine supports both native ChromaDB filters and retrieval-level filters.

Supported operators:

- equals
- contains
- startswith
- endswith
- !=
- >
- >=
- <
- <=

Example:

```python
SearchFilter(
    property="file_path",
    constraint="contains",
    value="routing.py",
)
```

---


## Current Capabilities

- Repository Parsing
- AST Chunking
- Dense Retrieval
- Sparse Retrieval
- Hybrid Retrieval
- RRF Fusion
- CrossEncoder Reranking
- Metadata Filtering
- Repository Statistics
- MCP Integration

---

## Future Improvements

Planned improvements include:

- Compound metadata filters (`AND`, `OR`, `NOT`)
- Retrieval evaluation metrics
- Incremental indexing
- Docker deployment
- Remote ChromaDB support
- Extended project documentation

---

## License

This project was developed for educational, research, and internship purposes.