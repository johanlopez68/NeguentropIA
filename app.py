import streamlit as st
import google.generativeai as genai
import os

# 1. Configuración de página
st.set_page_config(page_title="NeguentropIA", layout="centered")

# Logo UIS
try:
    st.image("logo_uis.png", width=150)
except:
    st.warning("Imagen 'logo_uis.png' no encontrada.")

st.title("NeguentropIA")
st.subheader("Tutor virtual en habilidades directivas")

# 2. Configuración API Key (usando Secrets)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("Error: Configura 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    st.stop()

# 3. Prompt del sistema
instrucciones_sistema = """
Eres NeguentropIA, tutor experto en autoconocimiento gerencial. 
Tu propósito es formar líderes que se gobiernen a sí mismos.
Reglas:
* No des respuestas directas. Usa preguntas socráticas para retar al usuario.
* Fundamenta cada respuesta citando autores (Drucker, Goleman, Covey, Whetten & Cameron).
* Estructura: 1. Diagnóstico breve, 2. Análisis teórico, 3. Pregunta de autoconocimiento.
* Escribe solo la primera letra en mayúscula para frases.
"""

# 4. Inicializar modelo
modelo = genai.GenerativeModel(model_name="gemini-1.5-pro")

# 5. Carga de Documentos robusta
@st.cache_resource
def preparar_conocimiento():
    nombres = [
        "7 hábitos de la gente altamente efectiva.pdf",
        "DIV - Desarrollo_de_habilidades_directivas_8Ed_Whettn&Cameron-82-108.pdf",
        "El_Autoconocimiento_como_Habilidad_Geren.pdf",
        "Gestionarse a sí mismo (PETER DRUCKER).pdf",
        "Qué hace a un líder (DANIEL GOLEMAN).pdf"
    ]
    archivos_cargados = []
    for nombre in nombres:
        if os.path.exists(nombre):
            try:
                archivo = genai.upload_file(path=nombre)
                archivos_cargados.append(archivo)
            except Exception as e:
                st.warning(f"No se pudo subir {nombre}: {e}")
    return archivos_cargados

# 6. Inicio del Chat sin errores
if "chat_history" not in st.session_state:
    docs = preparar_conocimiento()
    # Iniciamos el chat pasando los documentos y el prompt inicial en un solo bloque
    st.session_state.chat_history = modelo.start_chat(
        history=[
            {"role": "user", "parts": docs + [instrucciones_sistema + "\nInicia la conversación."]}
        ]
    )

# 7. Interfaz de Chat
for mensaje in st.session_state.chat_history.history:
    # Mostramos el texto del mensaje si existe
    if mensaje.parts and hasattr(mensaje.parts[0], 'text'):
        rol = "Asistente" if mensaje.role == "model" else "Usuario"
        with st.chat_message(rol):
            st.markdown(mensaje.parts[0].text)

if prompt := st.chat_input("Describe la situación gerencial aquí..."):
    with st.chat_message("Usuario"):
        st.markdown(prompt)
    with st.chat_message("Asistente"):
        respuesta = st.session_state.chat_history.send_message(prompt)
        st.markdown(respuesta.text)
