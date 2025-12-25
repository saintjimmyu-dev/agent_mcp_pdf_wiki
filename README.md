# MCP Brain 🧠

Asistente híbrido inteligente con:
- **RAG local** sobre documento privado (AGUILA TRAINING)
- **Herramienta remota vía MCP** (Wikipedia en español)
- Respuestas naturales con Gemini-2.5-flash

¡Demo interactiva con Gradio!

## Demo

![Demo](demo.png)

## Arquitectura

```mermaid
graph TD
    A[Usuario] --> B["Interfaz Gradio<br><small>app_gradio.py</small>"]
    B --> C["Agente Orquestador<br><small>agent_graph.py</small>"]

    subgraph Fuentes
        C -->|PDF| D["RAG Local<br><small>agente_tools.py</small>"]
        D --> E["Chroma Vector DB"]
        E --> F["Embeddings Gemini"]
        F --> G["Gemini-2.5-flash"]
        G --> H[Respuesta]

        C -->|Wikipedia| I["Cliente MCP"]
        I --> J["Servidor MCP"]
        J --> K["Wikipedia API"]
        K --> L["Contenido"]
        L --> M["Gemini Resumen"]
        M --> H
    end


---

### 🔹 2️⃣ Bloque 2 – Flujo (Sequence Diagram)

```md
## Flujo de ejecución

```mermaid
sequenceDiagram
    autonumber
    participant U as Usuario
    participant G as Gradio
    participant A as Orquestador
    participant T as Tools
    participant C as ChromaDB
    participant L as Gemini
    participant M as MCP Server

    U->>G: Ingresa pregunta
    G->>A: ejecutar_agente()

    alt Fuente PDF
        A->>T: buscar_en_pdf()
        T->>C: query vectors
        C-->>T: resultados
        T->>L: generar respuesta
        L-->>A: texto final
    else Fuente Wikipedia
        A->>M: wikipedia_mcp()
        M-->>A: contenido
        A->>L: resumir
    end

    A-->>G: respuesta
    G-->>U: mostrar resultado
