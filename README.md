# Knowledge Retrieval System (KRS)

A hybrid semantic code retrieval system that indexes Python repositories and provides intelligent code search through an MCP (Model Context Protocol) server.

The Knowledge Retrieval System (KRS) combines Abstract Syntax Tree (AST) parsing, semantic chunking, dense vector retrieval, BM25 lexical search, Reciprocal Rank Fusion (RRF), CrossEncoder reranking, and metadata filtering to enable efficient repository exploration and code understanding.

---

## Table of Contents

- [Features](#features)
- [System Architecture](#system-architecture)
- [Retrieval Pipeline](#retrieval-pipeline)
- [Project Structure](#project-structure)
- [Technologies](#technologies)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [MCP Tools](#mcp-tools)
- [Indexed Collections](#indexed-collections)
- [Chunking](#chunking)
- [Metadata Filtering](#metadata-filtering)
- [Performance](#performance)
- [Future Improvements](#future-improvements)
- [License](#license)

---

## Features

- AST-based Python repository parsing
- Semantic AST-aware chunking
- Configurable chunk splitting
- Dense semantic retrieval using Sentence Transformers
- BM25 lexical retrieval
- Hybrid retrieval (Dense + BM25)
- Reciprocal Rank Fusion (RRF)
- CrossEncoder reranking
- Metadata filtering
- Native ChromaDB filtering
- Repository-aware indexing
- Search by repository granularity
- Incremental synchronization
- Full repository indexing
- Repository statistics and reports
- MCP server integration
- Configurable embedding models
- Configurable reranker models
- Retrieval latency measurement
- Concurrent retrieval benchmarking
- Excel benchmark report generation

---

## System Architecture

```text
                GitHub Repository
                        │
                        ▼
               Repository Parser
                        │
                        ▼
                 AST Parsing
                        │
                        ▼
              Semantic Chunking
                        │
                        ▼
             Embedding Generation
                        │
         ┌──────────────┴──────────────┐
         ▼                             ▼
   ChromaDB Vector Index          BM25 Index
         │                             │
         └──────────────┬──────────────┘
                        ▼
                Hybrid Retriever
                        ▼
          Reciprocal Rank Fusion
                        ▼
            CrossEncoder Reranker
                        ▼
             Metadata Filtering
                        ▼
              Final Ranked Results
                        ▼
                  MCP Server
                        ▼
                 AI / MCP Client
```

---

## Retrieval Pipeline

```text
Repository
      │
      ▼
Repository Parser
      │
      ▼
AST Parsing
      │
      ▼
Document Generation
      │
      ▼
Semantic Chunking
      │
      ▼
Embedding Generation
      │
      ├───────────────┐
      ▼               ▼
 BM25 Index      ChromaDB
      │               │
      ▼               ▼
BM25 Search    Dense Retrieval
      └──────┬────────┘
             ▼
Reciprocal Rank Fusion (RRF)
             ▼
CrossEncoder Reranker
             ▼
Metadata Filtering
             ▼
Final Ranked Results
             ▼
MCP Server Response
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
│   ├── incremental_sync/
│   ├── indexing/
│   ├── parser/
│   ├── reports/
│   ├── retrieval/
│   ├── services/
│   └── vectordb/
│
├── mcp_server/
├── repositories/
├── outputs/
├── logs/
├── tests/
│
├── run.py
├── .env.example
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Technologies

| Category | Technology |
|---|---|
| Language | Python |
| Parser | Tree-Sitter |
| Vector Database | ChromaDB |
| Embeddings | Sentence Transformers (BAAI/bge-small-en-v1.5) |
| Sparse Retrieval | BM25 |
| Hybrid Ranking | Reciprocal Rank Fusion (RRF) |
| Reranker | CrossEncoder |
| MCP Framework | FastMCP |
| API Framework | FastAPI |
| Validation | Pydantic |
| ML Framework | HuggingFace Transformers |

---

## Installation

**Clone the repository**

```bash
git clone https://github.com/vinaymrampur4-art/Knowledge-Retrieval-System.git
```

**Move into the project**

```bash
cd Knowledge-Retrieval-System
```

**Create a virtual environment**

```bash
python -m venv .venv
```

**Activate the environment**

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

**Install dependencies**

```bash
pip install -r requirements.txt
```

---

## Configuration

Copy the example environment file:

```bash
cp .env.example .env
```

Configure the required environment variables. Important settings include:

- Repository location
- Embedding model
- Reranker model
- ChromaDB location
- MCP server configuration
- Retrieval parameters

---

## Usage

The project provides a unified command-line interface through `run.py`.

| Command | Description |
|---|---|
| `python run.py index` | Build repository indexes |
| `python run.py server` | Start the MCP server |
| `python run.py sync` | Run incremental synchronization |
| `python run.py benchmark` | Run concurrency benchmark |

### Build Repository Index

```bash
python run.py index
```

This command:

- Parses the repository
- Generates AST documents
- Performs semantic chunking
- Creates embeddings
- Builds BM25 indexes
- Indexes documents into ChromaDB

### Start MCP Server

```bash
python run.py server
```

Default configuration:

| Setting | Value |
|---|---|
| Host | 127.0.0.1 |
| Port | 8000 |
| Endpoint | /mcp |

### Incremental Synchronization

```bash
python run.py sync
```

Indexes only modified repository files without rebuilding the complete index.

### Run Concurrency Benchmark

```bash
python run.py benchmark
```

Measures concurrent retrieval performance and exports benchmark statistics to Excel.

---

## MCP Tools

**Search Tools**

- Search Repository
- Search Classes
- Search Methods
- Search Functions
- Search Files
- Search Code Blocks
- Search by Granularity

**Lookup Tools**

- Lookup by ID
- Lookup by Metadata Attributes

**Reporting Tools**

- Repository Statistics
- Repository Reports
- File Reports
- Branch Reports
- Class Reports
- Method Reports
- Repository Dashboard

---

## Indexed Collections

The system maintains dedicated collections for different code constructs:

- Files
- Classes
- Methods
- Functions
- Code Blocks

Hybrid retrieval performs parallel dense and BM25 retrieval across all indexed collections, merges results using Reciprocal Rank Fusion (RRF), and reranks them using a CrossEncoder before returning the final ranked results.
---

## Chunking

KRS performs AST-aware semantic chunking.

Supported chunk types include:

- Classes
- Methods
- Functions
- Imports
- Constants

Large semantic chunks are automatically divided into embedding-sized chunks while preserving the logical structure of the source code.

---

## Metadata Filtering

Supported filter operators:

| Operator | Description |
|---|---|
| `equals` | Exact match |
| `contains` | Substring match |
| `startswith` | Prefix match |
| `endswith` | Suffix match |
| `!=` | Not equal |
| `>` | Greater than |
| `>=` | Greater than or equal |
| `<` | Less than |
| `<=` | Less than or equal |

Example:

```python
SearchFilter(
    property="file_path",
    constraint="contains",
    value="routing.py",
)
```

---

## Performance

KRS includes benchmarking for:

- Dense retrieval latency
- BM25 retrieval latency
- Hybrid retrieval latency
- Reciprocal Rank Fusion latency
- CrossEncoder reranking latency
- Total search latency
- Concurrent throughput
- Average response time
- Minimum response time
- Maximum response time

Benchmark reports are exported to Excel under the `outputs/` directory.

---

## Future Improvements

- Retrieval quality evaluation (Precision@K, Recall@K, MRR, nDCG)
- Compound metadata filters (AND / OR / NOT)
- Remote ChromaDB support
- Docker deployment
- Multi-language repository support

---

## License

This project was developed as part of the **Tech Mahindra Internship** and is intended for educational, research, and intelligent code retrieval purposes.