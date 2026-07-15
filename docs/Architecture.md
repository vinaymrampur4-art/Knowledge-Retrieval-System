# System Architecture

## Overview

The Knowledge Retrieval System (KRS) is a hybrid code retrieval platform designed to index Python repositories and provide semantic code search.

The system combines:

- AST Parsing
- Dense Retrieval
- Sparse Retrieval
- Reranking
- Metadata Filtering
- MCP Integration

---

## High Level Architecture

Repository
    ↓
Repository Parser
    ↓
AST Parser
    ↓
Document Generation
    ↓
Embedding Generation
    ↓
BM25 + ChromaDB Indexing
    ↓
Hybrid Retrieval
    ↓
RRF Fusion
    ↓
CrossEncoder Reranking
    ↓
MCP Server

---

## Main Components

- Parser
- Indexer
- Retriever
- Reranker
- MCP Server