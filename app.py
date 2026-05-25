import streamlit as st
import google.generativeai as genai
import os

st.set_page_config(page_title="NeguentropIA", layout="centered")

# Logo UIS
try:
    st.image("logo_uis.png", width=150)
except:
    st.warning("Imagen 'logo_uis.png' no encontrada.")

st.title("NeguentropIA")
st.subheader("Tutor virtual en habilidades directivas")

# Configuración API Key privada (desde Streamlit Secrets)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    api_key = "TU_API_KEY_LOCAL" # Solo para pruebas en tu PC

genai.configure(api_key=api_key)

# Inicializar modelo
modelo = genai.GenerativeModel(model_name="gemini-1.5-pro")

# Cargar documentos (se ejecuta una vez)
@st.cache_resource
def cargar_documentos():
    nombres = [
        "7 hábitos de la gente altamente efectiva.pdf",
        "DIV - Desarrollo_de_habilidades_directivas_8Ed_Whettn&Cameron-82-108.pdf",
        "Gestionarse a sí mismo (PETER DRUCKER).pdf",
        "Qué hace a un líder (DANIEL GOLEMAN).pdf"
    ]
    archivos_subidos = []
    for nombre in nombres:
        if os.path.exists(nombre):
            archivos_subidos.append(genai.upload_file(path=nombre))
    return archivos_subidos

if "chat_history" not in st.session_state:
    docs = cargar_documentos()
    # Iniciamos chat con el prompt y los documentos como contexto
    system_instr = """Eres NeguentropIA, tutor de habilidades directivas. 
    Usa los documentos cargados para fundamentar tus respuestas.
    Reglas: No des la respuesta directa, usa preguntas socráticas, 
    usa solo la primera letra en mayúscula para frases."""
    
    st.session_state.chat_history = modelo.start_chat(
        history=[{"role": "user", "parts": docs + [system_instr]}]
    )

# Interfaz de Chat
for mensaje in st.session_state.chat_history.history:
    rol = "Asistente" if mensaje.role == "model" else "Usuario"
    with st.chat_message(rol):
        st.markdown(mensaje.parts[0].text)

if prompt := st.chat_input("Describe la situación gerencial..."):
    with st.chat_message("Usuario"):
        st.markdown(prompt)
    with st.chat_message("Asistente"):
        respuesta = st.session_state.chat_history.send_message(prompt)
        st.markdown(respuesta.text)
