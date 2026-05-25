import streamlit as st
import google.generativeai as genai

# 1. Configuración de página
st.set_page_config(page_title="NeguentropIA", layout="centered")

# Logo UIS
try:
    st.image("logo_uis.png", width=150)
except:
    st.warning("Asegúrate de tener el archivo 'logo_uis.png' en la carpeta.")

st.title("NeguentropIA")
st.subheader("Tutor virtual en habilidades directivas")

# 2. Configuración API Key (usando Secrets de Streamlit)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("Error: Configura 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    st.stop()

# 3. Prompt del sistema (Base de conocimiento integrada)
instrucciones_sistema = """
Eres NeguentropIA, un tutor experto en autoconocimiento gerencial basado en los siguientes autores:
1. Whetten & Cameron: Las 5 dimensiones del autoconocimiento (inteligencia emocional, valores, estilo cognoscitivo, actitud ante el cambio, autoevaluación).
2. Peter Drucker: Gestión de fortalezas y feedback.
3. Daniel Goleman: Inteligencia emocional y liderazgo.
4. Stephen Covey: Proactividad vs. Reactividad.
5. Powell y Rodríguez: Mecanismos de defensa.

Reglas:
* No des respuestas directas. Usa preguntas socráticas para retar al usuario.
* Fundamenta cada respuesta citando a uno de los autores mencionados.
* Estructura: 1. Diagnóstico breve, 2. Análisis teórico, 3. Pregunta de autoconocimiento.
* Escribe solo la primera letra en mayúscula para frases.
"""

# 4. Inicializar modelo estable
modelo = genai.GenerativeModel(model_name="gemini-1.5-flash")

# 5. Inicio del Chat seguro
if "chat_history" not in st.session_state:
    st.session_state.chat_history = modelo.start_chat(history=[])
    # Enviamos las instrucciones iniciales
    try:
        st.session_state.chat_history.send_message(instrucciones_sistema)
    except Exception as e:
        st.error(f"Error al inicializar la sesión: {e}")

# 6. Interfaz de Chat
for mensaje in st.session_state.chat_history.history:
    if hasattr(mensaje.parts[0], 'text'):
        rol = "Asistente" if mensaje.role == "model" else "Usuario"
        with st.chat_message(rol):
            st.markdown(mensaje.parts[0].text)

if prompt := st.chat_input("Describe tu caso gerencial aquí..."):
    with st.chat_message("Usuario"):
        st.markdown(prompt)
    with st.chat_message("Asistente"):
        with st.spinner("Analizando..."):
            respuesta = st.session_state.chat_history.send_message(prompt)
            st.markdown(respuesta.text)
