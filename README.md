# Knowledge Retrieval System (KRS)

A hybrid code retrieval system that indexes Python repositories and enables semantic and keyword-based search through an MCP (Model Context Protocol) server.

The project combines AST-based code parsing, vector embeddings, keyword search, and reranking to provide accurate retrieval of source code and repository metadata.

---

# Features

- AST-based repository parsing
- Automatic code chunking
- ChromaDB vector indexing
- BM25 keyword indexing
- Hybrid retrieval (Dense + BM25)
- Reciprocal Rank Fusion (RRF)
- CrossEncoder reranking
- Metadata filtering
- Repository statistics
- Repository reporting tools
- MCP Server integration
- Configurable embedding models
- Configurable reranker models

---

# Retrieval Pipeline

```
Repository
        │
        ▼
Repository Parser
        │
        ▼
AST Chunking
        │
        ▼
Embedding Generation
        │
        ▼
BM25 Index + ChromaDB Index
        │
        ▼
Hybrid Retrieval
(Dense + BM25)
        │
        ▼
Reciprocal Rank Fusion (RRF)
        │
        ▼
CrossEncoder Reranker
        │
        ▼
MCP Server
```

---

# Project Structure

```text
Knowledge_Retrieval_System/

│
├── app/
│   ├── chunker/
│   ├── core/
│   ├── embedding/
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
├── outputs/
│
├── tests/
│
├── docs/
│
├── requirements.txt
│
├── .env
│
└── README.md
```

---

# Technologies Used

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

---

# Installation

Clone the repository

```bash
git clone <repository-url>
```

Navigate to the project directory

```bash
cd Knowledge_Retrieval_System
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Configuration

The project uses a `.env` file for configuration.

Example:

```env
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5

RERANKER_MODEL=cross-encoder/ms-marco-MiniLM-L-6-v2

CHROMA_DB_PATH=chroma_db

DEFAULT_TOP_K=5

MAX_RESULTS=20
```

---

# Running the Project

## Build the Index

```bash
python -m tests.test_index_pipeline
```

## Start the MCP Server

```bash
python -m mcp_server.server
```

---

# MCP Tools

The MCP server currently provides the following tools:

- Search Repository
- Search Methods
- Search Classes
- Search Functions
- Search Files
- Search Code Blocks
- Lookup by ID
- Lookup by Metadata Attributes
- Repository Statistics
- Repository Reports

---

# Search Features

The retrieval engine supports:

- Semantic Search
- Keyword Search
- Hybrid Search
- Metadata Filtering

Supported filter operators:

- equals
- contains
- startswith
- endswith
- !=
- >
- >=
- <
- <=

---

# Current Capabilities

- Repository Parsing
- AST Chunking
- Embedding Generation
- Hybrid Retrieval
- Metadata Filtering
- Repository Statistics
- Repository Reports
- MCP Integration

---

# Future Improvements

Planned enhancements include:

- Compound metadata filters (AND / OR / NOT)
- Retrieval evaluation metrics
- Incremental indexing
- Docker deployment
- Remote ChromaDB support
- Extended project documentation

---

# License

This project is intended for educational and research purposes.