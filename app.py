import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="NeguentropIA", layout="centered")

st.title("NeguentropIA")
st.subheader("Tutor virtual en habilidades directivas")

# Configuración API
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("Configura GOOGLE_API_KEY en los Secrets.")
    st.stop()

# Configuración del modelo
model = genai.GenerativeModel("gemini-1.5-flash")

# Historial simple de mensajes para mostrar
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial previo
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Captura de input del usuario
if prompt := st.chat_input("Describe tu caso gerencial..."):
    # Guardar y mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Reconstrucción de la sesión para evitar el error NotFound
    # Enviamos todo el historial al modelo en cada interacción
    with st.chat_message("assistant"):
        with st.spinner("Analizando..."):
            try:
                # Construimos el historial de la conversación
                history_formatted = [
                    {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
                    for m in st.session_state.messages[:-1]
                ]
                
                chat = model.start_chat(history=history_formatted)
                
                # Instrucción de sistema inyectada en el primer mensaje
                if len(st.session_state.messages) == 1:
                    full_prompt = f"Actúa como NeguentropIA (Tutor experto en autoconocimiento gerencial basado en Whetten & Cameron, Drucker, Goleman, Covey y Powell). Instrucciones: No des respuestas directas, usa preguntas socráticas, estructura tu respuesta en: 1. Diagnóstico, 2. Análisis, 3. Pregunta socrática. Responde al siguiente caso: {prompt}"
                else:
                    full_prompt = prompt

                response = chat.send_message(full_prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                
            except Exception as e:
                st.error(f"Error de conexión: {e}. Intenta recargar la página.")
