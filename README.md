# CHUNKEN - CHUNK Extraction Node

CHUNKEN processes text from TEXTEN/webtexten by chunking it into manageable parts and creating embeddings for vector search. It supports both local (Ollama + ChromaDB + PostgreSQL) and cloud (OpenAI + Pinecone + MongoDB) providers.

Key Features
- Text Preprocessing: Cleans and preprocesses text, removing unnecessary elements
- Chunking: Divides large text files into smaller chunks
- Embeddings Generation: Uses Ollama (local) or OpenAI (cloud) for embeddings
- Storage: ChromaDB (local) or Pinecone (cloud) for vector storage
- Metadata: PostgreSQL (local) or MongoDB (cloud) for metadata storage

## Git Repositories
- https://github.com/open-qe-automation/texten.git
- https://github.com/open-qe-automation/webtexten.git
- https://github.com/open-qe-automation/chunken.git
- https://github.com/open-qe-automation/datamyn.git

## Related Packages
- https://github.com/open-qe-automation/package.utils.git
- https://github.com/open-qe-automation/package.data.loaders.git
- https://github.com/open-qe-automation/package.helpers.git

## Table of Contents
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)

## Prerequisites

- Python 3.12 or later
- pip
- For local stack: Ollama, PostgreSQL, ChromaDB
- For cloud stack: OpenAI API key, Pinecone, MongoDB

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/open-qe-automation/chunken.git
    cd chunken
    ```

2. **Set up a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    For local development, use dev-requirements.txt:
    ```bash
    pip install -r dev-requirements.txt
    ```

## Usage

To run the CHUNKEN application:

```bash
python app.py
```

### Local Stack Setup

1. **Start PostgreSQL:**
   ```bash
   # Using the provided script
   ./start_db.sh
   ```

2. **Start Ollama:**
   ```bash
   ollama serve
   # Pull the embedding model
   ollama pull nomic-embed-text
   ```

### Configuration

The configuration is managed through a `config.json` file:

```json
{
    "input_directories": ["../share/text_output"],
    "database": "rag-system",
    "namespace": "banking",
    "chunk_size": 1800,
    "chuck_extension_limit": 248,
    "scheduler_interval": 60,
    "embedding_provider": "ollama",
    "embedding_model": "nomic-embed-text",
    "embedding_base_url": "http://localhost:11434",
    "vector_db_provider": "chroma",
    "chroma_persist_directory": "../share/chroma_db",
    "metadata_db_provider": "postgresql",
    "postgresql_connection_string": "postgresql://postgres:ragpassword@localhost:5432/rag"
}
```

#### Provider Options

**Embedding Provider:**
- `ollama` (local): Uses Ollama with nomic-embed-text model
- `openai` (cloud): Uses OpenAI with text-embedding-3-small model

**Vector DB Provider:**
- `chroma` (local): Persists to local directory
- `pinecone` (cloud): Requires PINECONE_API_KEY env var

**Metadata DB Provider:**
- `postgresql` (local): Uses PostgreSQL connection string
- `mongodb` (cloud): Requires MONGO env var

## Testing

Run tests with pytest:

```bash
pip install -r dev-requirements.txt
pytest
```

Tests are located in the `tests/` directory. Some tests require external services (PostgreSQL, Ollama, ChromaDB) to be running.