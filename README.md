# Installation

## 1. Clone the repository

```bash
git clone https://github.com/yourusername/rag-project.git
cd rag-project
```

## 2. Create a virtual environment

```bash
python -m venv .venv
```

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Install PostgreSQL

Install PostgreSQL (version 15 or newer is recommended).

## 5. Enable pgvector

Connect to PostgreSQL and run:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

## 6. Create the database table

```sql
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    filename TEXT NOT NULL,
    page INTEGER NOT NULL,
    chunk_index INTEGER NOT NULL,
    chunk TEXT NOT NULL,
    embedding VECTOR(384),
    search_vector tsvector,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 7. Create Full Text Search index

```sql
CREATE INDEX documents_search_idx
ON documents
USING GIN(search_vector);
```

## 8. Create trigger

```sql
CREATE FUNCTION documents_search_vector_update()
RETURNS trigger AS $$
BEGIN
    NEW.search_vector := to_tsvector('simple', NEW.chunk);
    RETURN NEW;
END
$$ LANGUAGE plpgsql;

CREATE TRIGGER documents_search_vector_trigger
BEFORE INSERT OR UPDATE
ON documents
FOR EACH ROW
EXECUTE FUNCTION documents_search_vector_update();
```

## 9. Configure the database

Update your database connection in:

```
database/db.py
```

Example:

```python
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "rag_db"
DB_USER = "postgres"
DB_PASSWORD = "your_password"
```

## 10. Add PDF files

Place your PDF documents inside:

```
documents/
```

## 11. Ingest the documents

```bash
python ingestion/ingest.py
```

## 12. Start the API

```bash
uvicorn api.main:app --reload
```

## 13. Open the application

```
http://localhost:8000
```


PDF
 ↓
Text Extraction
 ↓
Chunking
 ↓
Embedding Generation
 ↓
PostgreSQL + pgvector
 ↓
Hybrid Search
(Vector + Keyword + RRF)
 ↓
LLM
 ↓
Answer + Sources
