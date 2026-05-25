import streamlit as st
import google.generativeai as genai
import os

# 1. Configuración de página
st.set_page_config(page_title="NeguentropIA", layout="centered")

# 2. Logo UIS
try:
    st.image("logo_uis.png", width=150)
except:
    st.warning("Asegúrate de tener el archivo 'logo_uis.png' en la misma carpeta.")

st.title("NeguentropIA")
st.subheader("Tutor virtual en habilidades directivas")

# 3. Configuración segura de la API
try:
    # Esto busca el valor en los "Secrets" de Streamlit Cloud
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("Error: No se encontró la API Key en los secretos. Configúralos en Streamlit Cloud.")
    st.stop()

# 4. Prompt y Modelo
instrucciones_sistema = """
Eres NeguentropIA, un asistente y tutor virtual diseñado exclusivamente para evaluar, corregir y mejorar las habilidades gerenciales de los estudiantes, con un enfoque estricto en el autoconocimiento. Tu nivel de exigencia es universitario avanzado.

Reglas:
* No des la respuesta directa ni resuelvas el problema por el usuario en tu primera intervención.
* Guía al usuario para que él mismo descubra su error mediante preguntas reflexivas.
* Fundamenta cada corrección citando explícitamente a los autores (Whetten, Cameron, Drucker, Goleman, Covey, Powell) de los documentos proporcionados.
* Escribe usando solo la primera letra en mayúscula para títulos y frases, evitando mayúsculas sostenidas.

Protocolo pedagógico:
* Evaluar: Analiza brevemente la decisión del usuario.
* Explicar y corregir: Identifica la falla usando la teoría de los documentos cargados.
* Proponer: Sugiere un camino de acción gerencial alternativo.
* Retar: Finaliza con una sola pregunta reflexiva socrática.
"""

modelo = genai.GenerativeModel(model_name="gemini-1.5-pro")

# 5. Carga de Documentos (Solo una vez)
@st.cache_resource
def preparar_conocimiento():
    nombres = [
        "7 hábitos de la gente altamente efectiva.pdf",
        "DIV - Desarrollo_de_habilidades_directivas_8Ed_Whettn&Cameron-82-108.pdf",
        "Gestionarse a sí mismo (PETER DRUCKER).pdf",
        "Qué hace a un líder (DANIEL GOLEMAN).pdf"
    ]
    archivos_cargados = []
    for nombre in nombres:
        if os.path.exists(nombre):
            archivos_cargados.append(genai.upload_file(path=nombre))
    return archivos_cargados

# 6. Inicio del Chat
if "chat_history" not in st.session_state:
    docs = preparar_conocimiento()
    # Vinculamos los documentos y las instrucciones desde el inicio
    st.session_state.chat_history = modelo.start_chat(
        history=[{"role": "user", "parts": docs + [instrucciones_sistema]}]
    )

# 7. Interfaz de Chat
for mensaje in st.session_state.chat_history.history:
    # Filtramos para mostrar solo texto (los docs son partes internas)
    if isinstance(mensaje.parts[0].text, str):
        rol = "Asistente" if mensaje.role == "model" else "Usuario"
        with st.chat_message(rol):
            st.markdown(mensaje.parts[0].text)

if prompt := st.chat_input("Describe la situación gerencial o tu decisión aquí..."):
    with st.chat_message("Usuario"):
        st.markdown(prompt)
    with st.chat_message("Asistente"):
        respuesta = st.session_state.chat_history.send_message(prompt)
        st.markdown(respuesta.text)
