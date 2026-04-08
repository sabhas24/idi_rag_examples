import os
from haystack import Document
from haystack.utils import Secret
from datasets import load_dataset
from dotenv import load_dotenv
from haystack_integrations.components.embedders.ollama import OllamaDocumentEmbedder
from haystack_integrations.document_stores.pgvector import PgvectorDocumentStore

# Cargar configuración desde el .env raíz
load_dotenv(dotenv_path="../../.env")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "pgvdb")
DB_PORT = os.getenv("DB_PORT", "5433")

# 1. Connect to local PGVector Docker
document_store = PgvectorDocumentStore(
    embedding_dimension=768,
    vector_function="cosine_similarity",
    recreate_table=True, 
    connection_string=Secret.from_token(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
)

print("1. Downloading dataset from HuggingFace...")
dataset = load_dataset("bilgeyucel/seven-wonders", split="train")
docs = [Document(content=doc["content"], meta=doc["meta"]) for doc in dataset]

print("2. Sending texts to Colab for Embeddings (This will take around 20 seconds)...")
doc_embedder = OllamaDocumentEmbedder(model="nomic-embed-text", url=OLLAMA_BASE_URL)
docs_with_embeddings = doc_embedder.run(docs)

print("3. Persisting results in PostgreSQL...")
document_store.write_documents(docs_with_embeddings["documents"])

print("\n✅ SUCCESS! Database indexed. You do not need to run this file again.")
