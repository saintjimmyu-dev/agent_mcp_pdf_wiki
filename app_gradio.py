import gradio as gr

# Import correcto del agente
from MCPBrain_Agent.agent.agent_graph import ejecutar_agente


# ✅ FUNCIÓN ASYNC (Gradio la soporta)
async def consultar(pregunta, fuente):
    if not pregunta.strip():
        return "❌ Escribe una pregunta válida."

    # 👇 AQUÍ SÍ SE AWAITEA
    resultado = await ejecutar_agente(pregunta, fuente)
    return resultado


with gr.Blocks(title="🧠 MCP Brain") as demo:
    gr.Markdown("## 🧠 MCP Brain (PDF + Wikipedia)")

    fuente = gr.Radio(
        choices=["PDF", "Wikipedia"],
        label="¿Dónde deseas consultar?",
        value="PDF"
    )

    pregunta = gr.Textbox(
        label="Escribe tu pregunta",
        placeholder="Ej: ¿Quién es Jimmy Uruchima?"
    )

    boton = gr.Button("Consultar")
    salida = gr.Textbox(label="Respuesta", lines=10)

    boton.click(
        fn=consultar,          # 👈 función async
        inputs=[pregunta, fuente],
        outputs=salida
    )

demo.launch()
