import os
from haystack import Pipeline
from haystack.utils import Secret
from haystack.components.builders import PromptBuilder
from haystack_integrations.document_stores.pgvector import PgvectorDocumentStore
from haystack_integrations.components.retrievers.pgvector import PgvectorEmbeddingRetriever
from haystack_integrations.components.embedders.ollama import OllamaTextEmbedder
from haystack_integrations.components.generators.ollama import OllamaGenerator
from dotenv import load_dotenv

# Cargar configuración desde el .env raíz
load_dotenv(dotenv_path="../../.env")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "pgvdb")
DB_PORT = os.getenv("DB_PORT", "5433")

# 1. Connect to local PGVector Docker (recreate_table=False to keep data)
document_store = PgvectorDocumentStore(
    embedding_dimension=768,
    recreate_table=False,
    connection_string=Secret.from_token(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
)

# 2. Configure Components 
text_embedder = OllamaTextEmbedder(model="nomic-embed-text", url=OLLAMA_BASE_URL)
retriever = PgvectorEmbeddingRetriever(document_store=document_store)
generator = OllamaGenerator(model="llama3.1", url=OLLAMA_BASE_URL, generation_kwargs={"num_predict": 1000}, timeout=450)

# 3. Pipeline
template = """ Context: {% for document in documents %}{{ document.content }}{% endfor %}
               Question: {{question}} \n Answer: """
prompt_builder = PromptBuilder(template=template)

p = Pipeline()
p.add_component("text_embedder", text_embedder)
p.add_component("retriever", retriever)
p.add_component("prompt_builder", prompt_builder)
p.add_component("llm", generator)

p.connect("text_embedder.embedding", "retriever.query_embedding")
p.connect("retriever.documents", "prompt_builder.documents")
p.connect("prompt_builder", "llm")

