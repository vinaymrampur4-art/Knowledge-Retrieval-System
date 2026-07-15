# Chunking

The system uses AST-aware semantic chunking.

Chunk types:

- File
- Class
- Method
- Function
- Code Block
- Import
- Constant

---

## Chunk Splitting

Large chunks are automatically split into embedding-sized chunks.

Configuration:

CHUNK_MAX_TOKENS=500

---

## Splitting Strategy

Chunks are split on line boundaries to preserve code structure.