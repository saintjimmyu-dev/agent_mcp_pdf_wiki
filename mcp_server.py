# mcp_server.py
# Propósito: Servidor MCP remoto que expone UNA herramienta pura: búsqueda en Wikipedia
# No usa LLM aquí → mantiene el servidor ligero y estable
# Usa fastmcp (el más estable en 2025)

from fastmcp import FastMCP  # Librería principal para crear servidores MCP modernos y estables (2025)
from langchain_community.utilities import WikipediaAPIWrapper  # Wrapper de LangChain para acceder a la API de Wikipedia
from langchain_community.tools import WikipediaQueryRun  # Herramienta de LangChain que ejecuta búsquedas en Wikipedia

import uvicorn  # Servidor ASGI ligero y rápido para levantar la app HTTP

# Configuración del servidor MCP
mcp = FastMCP(
    name="MCPBrain",  # Nombre del servidor (visible para clientes MCP)
    instructions="Tienes acceso a una herramienta para buscar información actualizada en Wikipedia en español. Úsala cuando la pregunta requiera conocimiento general del mundo."
    # Instrucciones para el LLM que use este servidor (ej. Claude, Grok, etc.)
)

@mcp.tool()  # Decorador que registra esta función como herramienta MCP disponible
def wikipedia_mcp(tema: str) -> str:
    """
    Herramienta pura: realiza una búsqueda en Wikipedia y devuelve el contenido crudo.
    No usa LLM aquí → mantiene el servidor rápido y sin dependencias pesadas.
    """
    wiki = WikipediaQueryRun(
        api_wrapper=WikipediaAPIWrapper(
            lang="es",  # Búsqueda en español
            top_k_results=1,  # Solo la página más relevante
            doc_content_chars_max=2000  # Limita la longitud para evitar respuestas eternas
        )
    )
    resultado = wiki.run(tema)  # Ejecuta la búsqueda
    return resultado if resultado else "No se encontró información en Wikipedia."

if __name__ == "__main__":
    print("MCP Server iniciado (Wikipedia)")
    print("Levantando servidor HTTP en http://127.0.0.1:8000")
    # Levanta el servidor HTTP usando el app de fastmcp (endpoint en /mcp)
    uvicorn.run(mcp.http_app(), host="127.0.0.1", port=8000)