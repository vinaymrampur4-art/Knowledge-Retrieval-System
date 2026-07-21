"""
config.py

Central configuration for the Knowledge Retrieval System (KRS).

All application settings are loaded from the .env file.
"""

from pathlib import Path
from dotenv import load_dotenv
import os

# ==========================================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================================

load_dotenv()

# ==========================================================
# PROJECT PATHS
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

APP_DIR = PROJECT_ROOT / "app"

REPOSITORIES_DIR = PROJECT_ROOT / "repositories"

OUTPUT_DIR = PROJECT_ROOT / "outputs"

JSON_OUTPUT_DIR = OUTPUT_DIR / "json"

LOGS_DIR = PROJECT_ROOT / "logs"

# ==========================================================
# REPOSITORY CONFIGURATION
# ==========================================================

REPOSITORY_NAME = os.getenv(
    "REPOSITORY_NAME",
    "fastapi",
)

REPOSITORY_FOLDER = os.getenv(
    "REPOSITORY_FOLDER",
    "fastapi-master",
)

GITHUB_REPOSITORY = os.getenv(
    "GITHUB_REPOSITORY",
    "https://github.com/fastapi/fastapi",
)

DEFAULT_BRANCH = os.getenv(
    "DEFAULT_BRANCH",
    "master",
)

# ==========================================================
# PROJECT SETTINGS
# ==========================================================

PROJECT_NAME = os.getenv(
    "PROJECT_NAME",
    "Knowledge Retrieval System",
)

PROJECT_VERSION = os.getenv(
    "PROJECT_VERSION",
    "1.0.0",
)

DEBUG = os.getenv(
    "DEBUG",
    "False",
).lower() == "true"

# ==========================================================
# MCP SERVER CONFIGURATION
# ==========================================================

MCP_HOST = os.getenv(
    "MCP_HOST",
    "127.0.0.1",
)

MCP_PORT = int(
    os.getenv(
        "MCP_PORT",
        "8000",
    )
)

MCP_PATH = os.getenv(
    "MCP_PATH",
    "/mcp",
)

MCP_TRANSPORT = os.getenv(
    "MCP_TRANSPORT",
    "http",
)

# ==========================================================
# VECTOR DATABASE
# ==========================================================

CHROMA_DB_PATH = PROJECT_ROOT / os.getenv(
    "CHROMA_DB_PATH",
    "chroma_db",
)

# ==========================================================
# CHROMA COLLECTIONS
# ==========================================================

FILES_COLLECTION = os.getenv(
    "FILES_COLLECTION",
    "Files_Collection_v1",
)

CLASSES_COLLECTION = os.getenv(
    "CLASSES_COLLECTION",
    "Classes_Collection_v1",
)

METHODS_COLLECTION = os.getenv(
    "METHODS_COLLECTION",
    "Methods_Collection_v1",
)

FUNCTIONS_COLLECTION = os.getenv(
    "FUNCTIONS_COLLECTION",
    "Functions_Collection_v1",
)

CODE_BLOCK_COLLECTION = os.getenv(
    "CODE_BLOCK_COLLECTION",
    "Code_Block_Collection_v1",
)

# ==========================================================
# BM25
# ==========================================================

BM25_OUTPUT_DIR = OUTPUT_DIR / "bm25"

# Legacy paths (still kept for compatibility)
BM25_INDEX_FILE = BM25_OUTPUT_DIR / "bm25_index.pkl"

BM25_STORE_FILE = BM25_OUTPUT_DIR / "bm25_store.pkl"

# ==========================================================
# EMBEDDING MODEL
# ==========================================================

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "BAAI/bge-small-en-v1.5",
)

# ==========================================================
# CHUNKING SETTINGS
# ==========================================================

CHUNK_MAX_TOKENS = int(
    os.getenv(
        "CHUNK_MAX_TOKENS",
        "500",
    )
)

CHUNK_MIN_TOKENS = int(
    os.getenv(
        "CHUNK_MIN_TOKENS",
        "80",
    )
)

# ==========================================================
# RERANKER
# ==========================================================

RERANKER_MODEL = os.getenv(
    "RERANKER_MODEL",
    "cross-encoder/ms-marco-MiniLM-L-6-v2",
)

# ==========================================================
# RETRIEVAL SETTINGS
# ==========================================================

DEFAULT_ALPHA = float(
    os.getenv(
        "DEFAULT_ALPHA",
        "0.8",
    )
)

DEFAULT_TOP_K = int(
    os.getenv(
        "DEFAULT_TOP_K",
        "5",
    )
)

MAX_RESULTS = int(
    os.getenv(
        "MAX_RESULTS",
        "20",
    )
)

# ==========================================================
# LOGGING
# ==========================================================

LOG_LEVEL = os.getenv(
    "LOG_LEVEL",
    "INFO",
)

LOG_FILE = PROJECT_ROOT / os.getenv(
    "LOG_FILE",
    "logs/krs.log",
)

# ==========================================================
# CREATE REQUIRED DIRECTORIES
# ==========================================================

for directory in [
    REPOSITORIES_DIR,
    OUTPUT_DIR,
    JSON_OUTPUT_DIR,
    LOGS_DIR,
    CHROMA_DB_PATH,
    BM25_OUTPUT_DIR,
]:
    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

# ==========================================================
# Incremental Sync
# ==========================================================

SYNC_OUTPUT_DIR = (
    OUTPUT_DIR /
    "sync"
)

SYNC_OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True,
)

# ==========================================================
# Reranker
# ==========================================================

RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# Number of hybrid candidates passed to the CrossEncoder
RERANK_CANDIDATES = 20