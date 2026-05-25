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
st.subheader("Tutor virtual en habilidades directivas (autoconocimiento)")

# 3. Configuración segura de la API (usando st.secrets)
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("Error: Configura 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    st.stop()

# 4. Prompt del sistema
instrucciones_sistema = """
Eres NeguentropIA, tutor experto en autoconocimiento gerencial. Tu propósito es formar líderes capaces de gobernarse a sí mismos antes de gobernar a otros. 

Tu nivel de exigencia es universitario avanzado. Debes analizar cada situación basándote exclusivamente en los marcos teóricos de los documentos cargados:
1. Whetten & Cameron: Diagnóstico de dimensiones del autoconocimiento (inteligencia emocional, valores, estilo cognoscitivo, actitud hacia el cambio, autoevaluación).
2. Peter Drucker: Análisis de feedback para la gestión de fortalezas.
3. Daniel Goleman: Componentes de la inteligencia emocional y liderazgo.
4. Stephen Covey: Proactividad vs. Reactividad.
5. John Powell y Andy Rodríguez: Identificación de mecanismos de defensa y líneas sensibles.

Reglas de respuesta obligatorias:
- Diagnóstico: Antes de cualquier consejo, identifica qué dimensión del autoconocimiento está fallando en el usuario.
- Socrático: NUNCA des soluciones directas. Si el usuario pide una solución, responde con una pregunta que lo obligue a revisar sus propios valores o prejuicios.
- Teoría: Cada respuesta debe citar al menos un autor y un concepto del documento correspondiente.
- Estilo: Escribe solo la primera letra en mayúscula para títulos y frases. Evita mayúsculas sostenidas.
- Estructura: 
    1. Diagnóstico breve: ¿Qué dimensión del autoconocimiento está involucrada?
    2. Análisis teórico: ¿Qué dicen los autores sobre este comportamiento?
    3. Pregunta de autoconocimiento: Un cuestionamiento socrático profundo que rete la "línea sensible" del usuario.

Ejemplo de tono: "Detecto una reacción defensiva que, según la teoría de mecanismos de defensa de Powell, podría estar ocultando un miedo a perder el control. ¿Te has preguntado si tu necesidad de imponer autoridad es realmente una medida de eficiencia o una respuesta ante la inseguridad de tu propia autoevaluación?"
"""

# 5. Inicializar modelo
modelo = genai.GenerativeModel(model_name="gemini-1.5-pro")

# 1. Ajusta la función para que no cree conflictos de caché si falla
@st.cache_resource
def preparar_conocimiento():
    nombres = [
        "7 hábitos de la gente altamente efectiva.pdf",
        "DIV - Desarrollo_de_habilidades_directivas_8Ed_Whettn&Cameron-82-108.pdf",
        "El_Autoconocimiento_como_Habilidad_Geren.pdf",
        "Gestionarse a sí mismo (PETER DRUCKER).pdf",
        "Qué hace a un líder (DANIEL GOLEMAN).pdf" # Revisa que este nombre coincida EXACTAMENTE con tu GitHub
    ]
    archivos_cargados = []
    for nombre in nombres:
        if os.path.exists(nombre):
            archivos_cargados.append(genai.upload_file(path=nombre))
    return archivos_cargados

# 2. Ajusta la inicialización del chat
if "chat_history" not in st.session_state:
    docs = preparar_conocimiento()
    
    # Creamos un mensaje inicial que contenga los documentos
    # Esto evita el error de "Not Found" al intentar llamar archivos que expiraron
    st.session_state.chat_history = modelo.start_chat(history=[])
    st.session_state.chat_history.send_message(
        [instrucciones_sistema] + docs + ["Inicia la conversación como NeguentropIA."]
    )

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
