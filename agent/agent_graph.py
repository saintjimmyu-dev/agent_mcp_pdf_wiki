import asyncio
from fastmcp import Client
from MCPBrain_Agent.tools.agente_tools import buscar_en_pdf, resumir_wikipedia

async def ejecutar_agente(pregunta: str, fuente: str) -> str:
    print("🧠 [AGENTE] Pregunta:", pregunta)
    print("🧠 [AGENTE] Fuente:", fuente)

    # ===== PDF → RAG LOCAL (rápido gracias al caché) =====
    if fuente == "PDF":
        return buscar_en_pdf(pregunta)

    # ===== WIKIPEDIA → MCP REMOTO + RESUMEN LOCAL =====
    print("🧩 [AGENTE] Conectando a MCP Server...")
    try:
        async with Client("http://127.0.0.1:8000/mcp") as client:
            print("🧩 [AGENTE] MCP conectado")

            result = await client.call_tool("wikipedia_mcp", {"tema": pregunta})

            contenido_crudo = ""
            for part in result.content:
                if hasattr(part, 'text'):
                    contenido_crudo += part.text
                elif isinstance(part, str):
                    contenido_crudo += part

            return resumir_wikipedia(pregunta, contenido_crudo.strip())

    except Exception as e:
        return f"Error MCP: {str(e)}"