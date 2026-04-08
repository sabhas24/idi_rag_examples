#!/bin/bash

echo "====================================="
echo "   ENCENDIENDO BASE DE DATOS DOCKER  "
echo "====================================="
# Movemos a la carpeta de infra y encendemos el contenedor pgvector
cd ../../infrastructure
sudo docker compose up -d vdb

echo ""
echo "📊 Estado del contenedor VDB:"
sudo docker logs infrastructure-vdb-1 --tail 5 2>&1 | grep -v '^$'

echo ""
echo "====================================="
echo "     INDEXANDO A POSTGRESQL         "
echo "====================================="
echo "(🔍 Enviando textos a Ollama en Colab para generar embeddings...)"
echo ""

# Volvemos a la carpeta original y corremos el script con el Python aislado
cd ../examples/SevenWonders
/home/pablo/RAG/.venv/bin/python 1_index_database.py

echo ""
echo "====================================="
