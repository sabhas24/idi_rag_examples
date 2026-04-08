#!/bin/bash
echo "====================================="
echo "   CONSULTANDO RAG VIA CLOUDFLARE    "
echo "====================================="

# Cargar URL de Ollama desde el .env raíz
OLLAMA_URL=$(grep OLLAMA_BASE_URL ../../.env | cut -d '=' -f2)
echo "🔗 Conectando a Ollama en: $OLLAMA_URL"
echo ""

/home/pablo/RAG/.venv/bin/python 2_query_database.py
