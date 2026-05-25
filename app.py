import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="NeguentropIA", layout="centered")

st.title("NeguentropIA")
st.subheader("Tutor virtual en habilidades directivas")

# Configuración de API
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("Configura GOOGLE_API_KEY en Secrets.")
    st.stop()

# Prompt mejorado con la base teórica embebida
instrucciones_sistema = """
Eres NeguentropIA, un tutor experto en autoconocimiento gerencial basado en:
1. Whetten & Cameron: Las 5 dimensiones del autoconocimiento.
2. Peter Drucker: Gestión de fortalezas y feedback.
3. Daniel Goleman: Inteligencia emocional.
4. Stephen Covey: Proactividad y hábitos efectivos.
5. Powell y Rodríguez: Mecanismos de defensa.

Tu rol es ser socrático. NUNCA des respuestas directas.
Ante cualquier caso, aplica esta estructura:
1. Diagnóstico: ¿Qué dimensión del autoconocimiento está fallando?
2. Análisis teórico: ¿Qué dicen los autores sobre esto?
3. Pregunta Socrática: Un reto que obligue al usuario a ver su "línea sensible".
"""

modelo = genai.GenerativeModel(model_name="gemini-1.5-pro")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = modelo.start_chat(history=[])
    st.session_state.chat_history.send_message(instrucciones_sistema)

# Interfaz
for mensaje in st.session_state.chat_history.history:
    if hasattr(mensaje.parts[0], 'text'):
        rol = "Asistente" if mensaje.role == "model" else "Usuario"
        with st.chat_message(rol):
            st.markdown(mensaje.parts[0].text)

if prompt := st.chat_input("Describe tu caso..."):
    with st.chat_message("Usuario"):
        st.markdown(prompt)
    with st.chat_message("Asistente"):
        # Esto ya no fallará porque no depende de archivos externos
        respuesta = st.session_state.chat_history.send_message(prompt)
        st.markdown(respuesta.text)
