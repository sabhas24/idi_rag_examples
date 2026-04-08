#!/bin/bash
echo "====================================="
echo "  🚀 INICIANDO CHAT BOT (VISUAL) 🚀  "
echo "====================================="
cd ../../infrastructure
sudo docker compose up -d db open-webui vdb

echo ""
echo "✅ El Chatbot está corriendo en segundo plano."
echo "🌐 Abre tu navegador en: http://localhost:8080"
echo ""
echo "📋 Monitoreando logs de arranque (Ctrl+C para detener el log y volver a la terminal)..."
echo "====================================="
sudo docker logs -f infrastructure-open-webui-1
