import streamlit as st
import google.generativeai as genai

# 1. Configuración de página
st.set_page_config(page_title="NeguentropIA", layout="centered")

# Logo UIS
try:
    st.image("logo_uis.png", width=150)
except:
    st.warning("Asegúrate de tener 'logo_uis.png' en la carpeta.")

st.title("NeguentropIA")
st.subheader("Tutor virtual en habilidades directivas")

# 2. Configuración API Key (usando Secrets de Streamlit)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("Error: Configura 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    st.stop()

# 3. Prompt del sistema
instrucciones_sistema = """
Eres NeguentropIA, un tutor experto en autoconocimiento gerencial basado en Whetten & Cameron, Peter Drucker, Daniel Goleman, Stephen Covey y Powell/Rodríguez.
Propósito y alcance: Desarrollar el criterio gerencial del estudiante mediante reflexión crítica. Tu función pedagógica es evaluar, corregir, explicar y proponer mejoras; no resuelves problemas por el usuario, lo guías para que descubra la solución.
Reglas obligatorias para tus respuestas:
No des respuestas directas. Usa preguntas socráticas para retar al usuario y exigirle profundidad analítica.
Fundamenta cada respuesta citando explícitamente a uno de los autores mencionados.
Estructura tu respuesta siempre en:
Diagnóstico breve: Evalúa y corrige la postura actual del usuario.
Análisis teórico: Explica el concepto gerencial subyacente.
Pregunta de autoconocimiento: Propón una mejora retando al usuario a aplicar la teoría.
Escribe solo la primera letra en mayúscula para frases (formato estándar). Evita mayúsculas sostenidas.
"""

# 4. Inicializar modelo
modelo = genai.GenerativeModel("gemini-3.5-flash")

# 5. Gestión del estado de la conversación (onboarding)
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.perfil_completado = False

# 6. Interfaz de Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Fase de Onboarding (humanización)
if not st.session_state.perfil_completado:
    if len(st.session_state.messages) == 0:
        bienvenida = "Hola, soy NeguentropIA. Para acompañarte mejor en tu proceso de autoconocimiento, ¿cuál es tu nombre y cuál es tu rol o principal objetivo profesional hoy?"
        st.session_state.messages.append({"role": "assistant", "content": bienvenida})
        st.chat_message("assistant").markdown(bienvenida)
    
    if prompt := st.chat_input("Escribe tu nombre y objetivo..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        mensaje_bienvenida = f"Un gusto saludarte. He registrado tu perfil: '{prompt}'. Mi misión es cuestionar tus certezas para fortalecer tu autoconocimiento. Comencemos. ¿Qué situación gerencial o dilema personal te gustaría analizar hoy?"
        st.session_state.messages.append({"role": "assistant", "content": mensaje_bienvenida})
        with st.chat_message("assistant"):
            st.markdown(mensaje_bienvenida)
        
        st.session_state.perfil_completado = True
        st.rerun()

# Fase de chat normal tras onboarding
else:
    if prompt := st.chat_input("Describe tu caso gerencial aquí..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analizando..."):
                try:
                    # Construimos el historial de la conversación
                    history_formatted = [
                        {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
                        for m in st.session_state.messages[:-1]
                    ]
                    
                    chat = modelo.start_chat(history=history_formatted)
                    full_prompt = f"{instrucciones_sistema}\n\nResponde al siguiente caso basándote en el perfil del usuario: {prompt}"
                    
                    response = chat.send_message(full_prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Error técnico: {e}. Intenta recargar la página.")
