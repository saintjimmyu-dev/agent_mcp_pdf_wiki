"""
Herramientas locales del agente MCP Brain
- RAG sobre documento privado (PDF de AGUILA TRAINING)
- Resumen de Wikipedia remota (opcional, con Gemini para respuestas naturales)
"""

import os
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_chroma import Chroma

# ================= CONFIG =================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))  # Carga GOOGLE_API_KEY

PDF_PATH = os.path.join(BASE_DIR, "documento_origen.pdf")
VECTOR_DB = None  # Cache global para no recargar el PDF cada vez

# ================= PDF RAG (local y rápido) =================
def preparar_pdf_rag():
    """Carga el PDF una sola vez y crea la base de vectores (caché global)"""
    global VECTOR_DB
    if VECTOR_DB is not None:  # Si ya está cargado, no lo vuelve a hacer
        return VECTOR_DB

    print("📄 [RAG] Cargando PDF por primera vez...")
    loader = PyPDFLoader(PDF_PATH)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    chunks = splitter.split_documents(docs)
    print(f"📄 [RAG] Chunks creados: {len(chunks)}")

    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    VECTOR_DB = Chroma.from_documents(chunks, embeddings, persist_directory=None)  # En memoria
    print("📄 [RAG] Vector DB lista y cacheada")
    return VECTOR_DB

def buscar_en_pdf(consulta: str) -> str:
    """RAG optimizado: búsqueda rápida + respuesta natural con gemini-2.5-flash"""
    db = preparar_pdf_rag()
    docs = db.similarity_search(consulta, k=4)
    if not docs:
        return "No encontré información en el documento de AGUILA TRAINING."

    contexto = "\n\n".join([d.page_content for d in docs])

    # Usamos gemini-2.5-flash (el que te funciona bien)
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.2,
        max_output_tokens=500  # Limitamos para mayor velocidad
    )

    prompt = f"""
    Eres un asistente profesional de AGUILA TRAINING.
    Responde de forma clara, directa y natural usando solo la información del contexto.
    No menciones fuentes ni documentos.
    Sé conciso pero completo.

    Pregunta: {consulta}
    Contexto: {contexto}

    Respuesta:
    """

    try:
        respuesta = llm.invoke(prompt)
        return respuesta.content.strip()
    except Exception as e:
        return f"Error al generar respuesta: {str(e)}"

# ================= RESUMEN WIKIPEDIA (opcional, con gemini-2.5-flash) =================
def resumir_wikipedia(pregunta: str, contenido_crudo: str) -> str:
    """Resume contenido crudo de Wikipedia usando gemini-2.5-flash para respuestas naturales y concisas"""
    if not contenido_crudo or "NO_RESULTADOS" in contenido_crudo:
        return "No encontré información relevante en Wikipedia."

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.3,
        max_output_tokens=600
    )

    prompt = f"""
    Eres un asistente experto y muy conciso.
    Responde directamente a la pregunta usando solo la información proporcionada.
    - Si es pregunta simple (capital, fundador, fecha): 1-2 frases.
    - Si es compleja: máximo 5 frases.
    Habla en español natural.

    Pregunta: {pregunta}
    Información: {contenido_crudo}

    Respuesta:
    """

    try:
        respuesta = llm.invoke(prompt)
        return respuesta.content.strip()
    except Exception as e:
        return f"Error al resumir Wikipedia: {str(e)}"