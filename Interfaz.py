import streamlit as st
import google.generativeai as genai

# Configuración inicial de la página
st.set_page_config(page_title="NeguentropIA", layout="centered")

# Mostrar el logo de la universidad
try:
    st.image("logo_uis.png", width=150)
except FileNotFoundError:
    st.warning("Asegúrate de guardar el archivo de imagen como 'logo_uis.png' en esta misma carpeta para que se visualice el escudo.")

st.title("NeguentropIA")
st.subheader("Tutor virtual en habilidades directivas y autoconocimiento")

# Configuración de la clave de la API
# Reemplaza el texto entre comillas con la clave que generaste en Google AI Studio
GOOGLE_API_KEY = "PEGA_AQUI_TU_API_KEY"
genai.configure(api_key=GOOGLE_API_KEY)

# Definición de las instrucciones del sistema (Tu prompt estructurado)
instrucciones_sistema = """
Eres NeguentropIA, un asistente y tutor virtual diseñado exclusivamente para evaluar, corregir y mejorar las habilidades gerenciales de los estudiantes, con un enfoque estricto en el autoconocimiento. Tu nivel de exigencia es universitario avanzado.

Reglas de comportamiento y respuesta:
* No des la respuesta directa ni resuelvas el problema por el usuario en tu primera intervención.
* Guía al usuario para que él mismo descubra su error mediante preguntas reflexivas.
* Fundamenta cada corrección citando explícitamente a los autores y modelos teóricos proporcionados en tu base de conocimiento.
* Mantén un tono profesional, objetivo, riguroso y empático.
* Escribe usando solo la primera letra en mayúscula para títulos y frases, evitando por completo el uso de palabras en mayúsculas sostenidas.

Base conceptual obligatoria:
* David Whetten y Kim Cameron: Diagnostica si el usuario está cruzando su línea sensible... (Asegúrate de incluir toda tu teoría aquí).
* Peter Drucker: Aplica el análisis de feedback para descubrir fortalezas...
* Daniel Goleman: Evalúa los componentes de la inteligencia emocional...
* Stephen Covey: Diferencia entre comportamientos proactivos y reactivos...
* John Powell y Andy Rodríguez: Detecta e identifica si el usuario está usando mecanismos de defensa...

Protocolo pedagógico:
* Evaluar: Analiza brevemente la decisión o actitud del usuario.
* Explicar y corregir: Identifica la falla utilizando un concepto teórico de los autores base.
* Proponer: Sugiere un camino de acción gerencial alternativo.
* Retar: Finaliza siempre con una sola pregunta reflexiva de estilo socrático.
"""

# Configuración del modelo de inteligencia artificial
# Mantenemos la temperatura baja (0.2) para que las respuestas sean rigurosas y analíticas
configuracion = {
    "temperature": 0.2,
}

# Inicialización del modelo Gemini 1.5 Pro
modelo = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=configuracion,
    system_instruction=instrucciones_sistema
)

# Inicializar el historial de la conversación en la memoria de la aplicación
if "chat_history" not in st.session_state:
    st.session_state.chat_history = modelo.start_chat(history=[])

# Mostrar todos los mensajes anteriores en la pantalla
for mensaje in st.session_state.chat_history.history:
    rol = "Asistente" if mensaje.role == "model" else "Usuario"
    with st.chat_message(rol):
        st.markdown(mensaje.parts[0].text)

# Barra inferior para que los compañeros de equipo introduzcan sus casos de prueba
entrada_usuario = st.chat_input("Describe la situación gerencial o tu decisión aquí...")

if entrada_usuario:
    # 1. Mostrar lo que el usuario acaba de escribir
    with st.chat_message("Usuario"):
        st.markdown(entrada_usuario)
    
    # 2. Enviar el mensaje a NeguentropIA y esperar la respuesta
    respuesta = st.session_state.chat_history.send_message(entrada_usuario)
    
    # 3. Mostrar la respuesta generada por la IA
    with st.chat_message("Asistente"):
        st.markdown(respuesta.text)