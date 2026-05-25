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
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("Error: Configura 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    st.stop()

# 3. Prompt del sistema (Base de conocimiento integrada)
# Esta versión inyecta el conocimiento directamente para evitar errores de red
instrucciones_sistema = """
Eres NeguentropIA, un tutor experto en autoconocimiento gerencial basado en los siguientes pilares teóricos:
1. Whetten & Cameron: Las 5 dimensiones del autoconocimiento (inteligencia emocional, valores, estilo cognoscitivo, actitud ante el cambio, autoevaluación).
2. Peter Drucker: Gestión de fortalezas y feedback.
3. Daniel Goleman: Inteligencia emocional y liderazgo.
4. Stephen Covey: Proactividad vs. Reactividad.
5. Powell y Rodríguez: Mecanismos de defensa.

Reglas obligatorias:
* No des respuestas directas. Usa preguntas socráticas para retar al usuario.
* Fundamenta cada respuesta citando a uno de los autores mencionados.
* Estructura tu respuesta siempre en: 1. Diagnóstico breve, 2. Análisis teórico, 3. Pregunta de autoconocimiento.
* Escribe solo la primera letra en mayúscula para frases (no uses mayúsculas sostenidas).
"""

# 4. Inicializar modelo estable
modelo = genai.GenerativeModel("gemini-3.5-flash")


# 5. Gestión del estado de la conversación
if "messages" not in st.session_state:
    st.session_state.messages = []

# 6. Interfaz de Chat
# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capturar input del usuario
if prompt := st.chat_input("Describe tu caso gerencial aquí..."):
    # Guardar y mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Reconstrucción de la sesión para evitar errores de red
    with st.chat_message("assistant"):
        with st.spinner("Analizando..."):
            try:
                # Construimos el historial de la conversación
                history_formatted = [
                    {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
                    for m in st.session_state.messages[:-1]
                ]
                
                chat = modelo.start_chat(history=history_formatted)
                
                # Inyección de instrucciones en la primera interacción
                if len(st.session_state.messages) == 1:
                    full_prompt = f"{instrucciones_sistema}\n\nResponde al siguiente caso: {prompt}"
                else:
                    full_prompt = prompt

                response = chat.send_message(full_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
            except Exception as e:
                st.error(f"Error de conexión: {e}. Intenta recargar la página.")
