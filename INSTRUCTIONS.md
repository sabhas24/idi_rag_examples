# 📘 Manual de Operación: Sistema RAG (Arquitectura Híbrida)

Este documento detalla el funcionamiento y la gestión del sistema de Generación Aumentada por Recuperación (RAG). El proyecto utiliza una arquitectura híbrida diseñada para optimizar los recursos locales mediante el procesamiento distribuido.

---

## 🏗️ 1. Arquitectura del Sistema

El ecosistema se divide en tres capas fundamentales:

1.  **Capa de Cómputo (Google Colab)**: Ejecuta los modelos de lenguaje (LLM) y de embeddings (`llama3.1` y `nomic-embed-text`) mediante Ollama, aprovechando la aceleración por GPU en la nube.
2.  **Capa de persistencia (Docker)**: Gestiona la base de datos de vectores (`PostgreSQL` + `pgvector`) y la interfaz de usuario de forma local y segura.
3.  **Entorno de Ejecución (.venv)**: Entorno Python aislado que garantiza la compatibilidad de librerías y la integridad del sistema operativo anfitrión.

---

## ☁️ 2. Preparación del Entorno Remoto (Google Colab)

Dado que las instancias de Google Colab son efímeras, se debe inicializar el servidor de inferencia en cada sesión de trabajo siguiendo estos pasos:

1.  Acceda a su cuaderno de Google Colab.
2.  Ejecute el siguiente bloque de código para inicializar el servidor y el túnel de comunicación:

```python
# 1. Instalación de dependencias del sistema y Ollama
!apt-get install -y zstd
!curl -fsSL https://ollama.com/install.sh | sh

# 2. Configuración de servicios de red y modelos
import os, subprocess, time, re

# Limpieza de procesos previos
os.system("pkill cloudflared")
os.system("pkill ollama")
time.sleep(2)

# Descarga del cliente para el túnel de red
!wget -q -c https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O cloudflared
!chmod +x cloudflared

# Variables de entorno para Ollama
os.environ["OLLAMA_HOST"] = "0.0.0.0"
os.environ["OLLAMA_ORIGINS"] = "*"

# Inicialización del servidor Ollama
print("🚀 Inicializando servidor de inferencia...")
subprocess.Popen(["/usr/local/bin/ollama", "serve"])
time.sleep(5)

# Descarga de modelos requeridos
print("📥 Descargando modelos de lenguaje y embeddings...")
!/usr/local/bin/ollama pull nomic-embed-text
!/usr/local/bin/ollama pull llama3.1

# Apertura del túnel de comunicación seguro
print("🔗 Estableciendo túnel de comunicación...")
subprocess.Popen(["./cloudflared", "tunnel", "--url", "http://127.0.0.1:11434"], stderr=open("tunnel.log", "w"))

# Detección y extracción de la URL de acceso
url_encontrada = False
for _ in range(30):
    time.sleep(1)
    if os.path.exists("tunnel.log"):
        with open("tunnel.log", "r") as f:
            log_content = f.read()
            match = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', log_content)
            if match:
                print("\n" + "="*45)
                print("✅ COPIE LA SIGUIENTE URL DE COMUNICACIÓN:")
                print(match.group())
                print("="*45)
                url_encontrada = True
                break
if not url_encontrada:
    print("\n❌ Error en la detección del túnel. Verifique 'tunnel.log'.")
```

---

## ⚙️ 3. Configuración Centralizada (.env)

El proyecto utiliza un sistema de configuración unificado. Una vez obtenida la URL desde Google Colab, siga este procedimiento:

1.  Localice el archivo [`.env`] en el directorio raíz del proyecto.
2.  Actualice la variable `OLLAMA_BASE_URL` con la dirección obtenida en el paso anterior.

> [!Observacion]
> Al modificar este archivo único, tanto los scripts de indexación como la interfaz web se reconfigurarán automáticamente sin necesidad de ediciones adicionales.

---

## 🚀 4. Guía de Operación y Scripts

Navegue a la carpeta del ejemplo: `cd examples/SevenWonders/` y ejecute los scripts según su necesidad:

### A. Indexación de Datos (`run_indexer.sh`)
*   **Propósito**: Inicializa la base de datos local y procesa el dataset para generar los vectores de búsqueda.
*   **Cuándo usar**: Solo la primera vez que configure el proyecto o cuando desee actualizar la base de conocimientos.

### B. Consulta por Terminal - CLI (`run_query.sh`)
*   **Propósito**: Permite interactuar con el sistema RAG directamente desde la consola mediante una interfaz de texto.
*   **Uso**: para consultas rápidas y depuración técnica.

### C. Despliegue de Interfaz Gráfica (`run_chatbot.sh`)
*   **Propósito**: Inicia el servidor de Docker y despliega la aplicación **Open WebUI**.
*   **Acceso**: Una vez iniciado, acceda a [http://localhost:8180](http://localhost:8180) en su navegador web.
*   **Nota**: Este modo ofrece la experiencia completa de usuario similar a ChatGPT.
