# 2_preguntar.py
import os
from haystack import Pipeline
from haystack.components.builders import PromptBuilder
from haystack_integrations.document_stores.pgvector import PgvectorDocumentStore
from haystack_integrations.components.retrievers.pgvector import PgvectorEmbeddingRetriever
from haystack_integrations.components.embedders.ollama import OllamaTextEmbedder
from haystack_integrations.components.generators.ollama import OllamaGenerator

OLLAMA_BASE_URL = "https://engineering-panel-baths-quantitative.trycloudflare.com"

# 1. Me conecto a Docker de PGVector (OJO: recreate_table=False para no borrar nada)
document_store = PgvectorDocumentStore(
    embedding_dimension=768,
    recreate_table=False,
    connection_string="postgresql://tu_usuario:tu_contraseña@localhost:5433/pgvdb"
)

# 2. Configurar Traductores y Generadores 
text_embedder = OllamaTextEmbedder(model="nomic-embed-text", url=OLLAMA_BASE_URL)
retriever = PgvectorEmbeddingRetriever(document_store=document_store)
generator = OllamaGenerator(model="llama3.1", url=OLLAMA_BASE_URL, generation_kwargs={"num_predict": 1000}, timeout=450)

# Plantilla y Tubería (exactamente igual que tenías antes)
template = """ Contexto: {% for document in documents %}{{ document.content }}{% endfor %}
               Pregunta: {{question}} \n Responde: """
prompt_builder = PromptBuilder(template=template)

p = Pipeline()
p.add_component("text_embedder", text_embedder)
p.add_component("retriever", retriever)
p.add_component("prompt_builder", prompt_builder)
p.add_component("llm", generator)

p.connect("text_embedder.embedding", "retriever.query_embedding")
p.connect("retriever.documents", "prompt_builder.documents") # Cuidado con este detalle de sintaxis en pgvector
p.connect("prompt_builder", "llm")

# ¡Tirar la pregunta que se ejecuta al instante!
question = "Make a short description of the Lighthouse of Alexandria"
results = p.run({
    "text_embedder": {"text": question},
    "prompt_builder": {"question": question}
})

print(results["llm"]["replies"][0])
