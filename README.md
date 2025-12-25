# MCP Brain 🧠

Asistente híbrido inteligente con:
- **RAG local** sobre documento privado (AGUILA TRAINING)
- **Herramienta remota vía MCP** (Wikipedia en español)
- Respuestas naturales con Gemini-2.5-flash

¡Demo interactiva con Gradio!

## Demo

![Demo](demo.png)

## Arquitectura
graph TD
    A[Usuario] --> B["Interfaz Gradio<br><small>app_gradio.py</small>"]
    B --> C["Agente Orquestador<br><small>agent_graph.py</small>"]
    
    subgraph Fuentes
        C -->|Fuente = PDF| D["RAG Local<br><small>agente_tools.py</small>"]
        D --> E["Chroma Vector DB<br><small>Cache global</small>"]
        E --> F["Embeddings Gemini<br><small>text-embedding-004</small>"]
        F --> G["Gemini-2.5-flash<br><small>Respuesta natural</small>"]
        G --> H[Respuesta al usuario]
        
        C -->|Fuente = Wikipedia| I["Cliente fastmcp<br><small>Client('http://127.0.0.1:8000/mcp')</small>"]
        I --> J["Servidor MCP Remoto<br><small>mcp_server.py - puerto 8000</small>"]
        J --> K["Herramienta wikipedia_mcp<br><small>Búsqueda Wikipedia ES</small>"]
        K --> L[Contenido crudo]
        L --> M["Gemini-2.5-flash<br><small>Resumen conciso</small>"]
        M --> H
    end

    %% Estilos corregidos para asegurar contraste y legibilidad
    style A fill:#f0f8ff,stroke:#333,color:#000
    style B fill:#fffacd,stroke:#333,color:#000
    style C fill:#e6f3ff,stroke:#333,color:#000
    style D fill:#f0fff0,stroke:#333,color:#000
    style E fill:#f5f5dc,stroke:#333,color:#000
    style F fill:#f0fff0,stroke:#333,color:#000
    style G fill:#e0ffff,stroke:#333,color:#000
    style H fill:#fff0f5,stroke:#333,color:#000
    style I fill:#f0e6ff,stroke:#333,color:#000
    style J fill:#ffe6e6,stroke:#333,color:#000
    style K fill:#f0e6ff,stroke:#333,color:#000
    style L fill:#fff5ee,stroke:#333,color:#000
    style M fill:#e0ffff,stroke:#333,color:#000
    style Fuentes fill:#f8f8f8,stroke:#aaa,stroke-dasharray: 5 5,color:#000