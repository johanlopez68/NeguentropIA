import streamlit as st
import google.generativeai as genai
import os

# 1. Configuración de página
st.set_page_config(page_title="NeguentropIA", layout="centered")

# 2. Logo UIS
try:
    st.image("logo_uis.png", width=150)
except:
    st.warning("Asegúrate de tener el archivo 'logo_uis.png' en la carpeta.")

st.title("NeguentropIA")
st.subheader("Tutor virtual en habilidades directivas")

# 3. Configuración segura de la API (usando st.secrets)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("Error: Configura 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    st.stop()

# 4. Prompt del sistema
instrucciones_sistema = """
Eres NeguentropIA, un tutor virtual experto en habilidades gerenciales.
Tu objetivo es guiar al estudiante usando los documentos cargados.
Reglas:
* No des la respuesta directa; usa preguntas reflexivas.
* Fundamenta cada intervención citando los autores de los documentos (Drucker, Goleman, Covey, Whetten & Cameron).
* Escribe usando solo la primera letra en mayúscula para títulos y frases.
* Usa un tono profesional, objetivo y empático.
"""

# 5. Inicializar modelo
modelo = genai.GenerativeModel(model_name="gemini-1.5-pro")

# 6. Carga de Documentos
@st.cache_resource
def preparar_conocimiento():
    # Nombres exactos según tu lista
    nombres = [
        "7 hábitos de la gente altamente efectiva.pdf",
        "DIV - Desarrollo_de_habilidades_directivas_8Ed_Whettn&Cameron-82-108.pdf",
        "Gestionarse a sí mismo (PETER DRUCKER).pdf",
        "Qué hace a un líder (DANIEL GOLEMAN).pdf"
    ]
    archivos_cargados = []
    for nombre in nombres:
        if os.path.exists(nombre):
            archivo = genai.upload_file(path=nombre)
            archivos_cargados.append(archivo)
    return archivos_cargados

# 7. Inicio del Chat
if "chat_history" not in st.session_state:
    try:
        docs = preparar_conocimiento()
        st.session_state.chat_history = modelo.start_chat(
            history=[{"role": "user", "parts": docs + [instrucciones_sistema]}]
        )
    except Exception as e:
        st.error(f"Error al cargar documentos: {e}")

# 8. Interfaz de Chat
for mensaje in st.session_state.chat_history.history:
    if hasattr(mensaje.parts[0], 'text'):
        rol = "Asistente" if mensaje.role == "model" else "Usuario"
        with st.chat_message(rol):
            st.markdown(mensaje.parts[0].text)

if prompt := st.chat_input("Describe la situación gerencial aquí..."):
    with st.chat_message("Usuario"):
        st.markdown(prompt)
    with st.chat_message("Asistente"):
        respuesta = st.session_state.chat_history.send_message(prompt)
        st.markdown(respuesta.text)
