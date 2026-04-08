#!/bin/bash
echo "====================================="
echo "   🛑 DETENIENDO INFRAESTRUCTURA 🛑  "
echo "====================================="
cd ../../infrastructure
sudo docker compose down

echo ""
echo "✅ Todos los contenedores han sido detenidos."
echo "💾 Los datos de la base de datos siguen guardados en disco."
echo ""
echo "Para volver a iniciar, ejecuta: ./run_chatbot.sh"
