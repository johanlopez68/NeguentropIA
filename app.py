import streamlit as st
import google.generativeai as genai

# 1. Configuración de página
st.set_page_config(page_title="NeguentropIA", layout="centered")

# --- SECCIÓN DE LOGOS (Tamaños fijos ajustados) ---
# Usamos columnas asimétricas para que el logo de la UIS (rectangular) tenga más espacio
espacio_izq, col_logo1, col_logo2, espacio_der = st.columns([0.5, 1.5, 1, 0.5])

# Columna central 1: Logo UIS
with col_logo1:
    try:
        # Le damos un tamaño mayor en píxeles porque es rectangular
        st.image("logo_uis.png", width=200)
    except:
        st.warning("Asegúrate de tener 'logo_uis.png' en la carpeta.")

# Columna central 2: Nuevo Logo NeguentropIA
with col_logo2:
    try:
        # Lo hacemos más pequeño en píxeles para que no se vea gigante a lo alto
        st.image("logo_neguentropia.png", width=120)
    except:
        st.warning("Asegúrate de tener 'logo_neguentropia.png' en la carpeta.")
# ------------------------

st.title("NeguentropIA")
st.subheader("Tutor virtual en habilidades directivas (autoconocimiento)")

# 2. Configuración API Key (usando Secrets de Streamlit)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except:
    st.error("Error: Configura 'GOOGLE_API_KEY' en los Secrets de Streamlit.")
    st.stop()

# 3. Prompt del sistema
instrucciones_sistema = """
Eres NeguentropIA, un tutor experto en autoconocimiento gerencial basado en Whetten & Cameron, Peter Drucker, Daniel Goleman, Stephen Covey y Powell/Rodríguez.

Tono y estilo:
- Eres conversacional, empático y cercano (nivel de formalidad 6/10).
- Habla de tú a tú, como un mentor experimentado pero accesible, NO como un libro de texto.
- Fluye con naturalidad. Valida brevemente lo que siente el usuario antes de pasar a la teoría.
- MUY IMPORTANTE: Adapta tu lenguaje para principiantes. Usa metáforas, analogías de la vida cotidiana y evita a toda costa la jerga técnica o académica abrumadora.

Propósito y alcance: Desarrollar el criterio gerencial del estudiante mediante reflexión crítica. Tu función pedagógica es evaluar, corregir, explicar y proponer mejoras.

Reglas obligatorias para tus respuestas:
1. Usa preguntas socráticas para retar al usuario (SOLO en Escenario A).
2. Fundamenta cada respuesta citando a uno de los autores, pero "traduciendo" su teoría a palabras súper sencillas.
3. Escribe solo la primera letra en mayúscula para frases (formato estándar). Evita mayúsculas sostenidas.

Estructura condicional (EVALÚA LA INTENCIÓN DEL USUARIO ANTES DE RESPONDER):

ESCENARIO A - El usuario plantea un caso o aún necesita reflexión (Uso por defecto):
Estructura tu respuesta enlazando estos 3 enfoques como una conversación natural:
- Diagnóstico breve: Evalúa y corrige la postura actual del usuario con empatía.
- Análisis teórico: Explica el concepto gerencial de forma ultra-didáctica. Imagina que se lo explicas a un amigo tomando un café. 
- Pregunta de autoconocimiento: Propón una mejora retando al usuario a aplicar la teoría.

ESCENARIO B - Criterio de Cierre Inmediato (El usuario dice que entendió, agradece o se despide):
Si el usuario escribe cosas como "gracias", "ya entendí", "listo", o demuestra de cualquier forma que ya captó el mensaje, DETÉN EL INTERROGATORIO INMEDIATAMENTE.
Estructura tu respuesta final fluyendo de forma natural con:
- Validación cálida: Celebra brevemente que haya comprendido el punto o la actitud positiva que muestra.
- Despedida bonita y personalizada: Despídete de forma cercana. Deséale éxito EXPLÍCITAMENTE en el proyecto, situación o rol específico que te mencionó durante la charla.
- REGLA DE ORO: En este escenario ESTÁ PROHIBIDO hacer más preguntas. NO incluyas diagnósticos ni análisis. Simplemente cierra la conversación deseando lo mejor.
"""

# 4. Inicializar modelo
modelo = genai.GenerativeModel("gemini-1.5-flash") 

# 5. Gestión del estado de la conversación (onboarding)
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.perfil_completado = False

# 6. Interfaz de Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Fase de Onboarding (humanización e instrucciones)
if not st.session_state.perfil_completado:
    if len(st.session_state.messages) == 0:
        bienvenida = "Hola, soy NeguentropIA. Para acompañarte mejor en tu proceso de autoconocimiento, ¿cuál es tu nombre y cuál es tu rol o principal objetivo profesional hoy?"
        st.session_state.messages.append({"role": "assistant", "content": bienvenida})
        st.chat_message("assistant").markdown(bienvenida)
    
    if prompt := st.chat_input("Escribe tu nombre y objetivo..."):
        st.session_state.perfil_usuario = prompt 
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
      
        mensaje_bienvenida = """¡Un gusto saludarte! Gracias por presentarte. 
        
Mi misión es acompañarte en el desarrollo de tu **autoconocimiento**, la habilidad gerencial fundamental de la que parten todas las demás. No te daré respuestas directas, sino que te guiaré con preguntas basadas en autores como Peter Drucker, Daniel Goleman y Stephen Covey para que tú mismo descubras la solución.

💡 **¿Para qué puedes usarme? (Casos de uso)**
* **Conflictos interpersonales:** "Discutí con un compañero que no aporta nada".
* **Dilemas de liderazgo:** "No sé cómo dar retroalimentación negativa sin desmotivar a mi equipo".
* **Gestión personal y emocional:** "Me frustro mucho cuando cambian los planes a última hora".

📌 **¿Cómo interactuar conmigo?**
1. Escribe tu situación, reto o dilema actual con sinceridad.
2. Lee mi breve análisis y responde a la pregunta de reflexión que te haré al final.
3. Cuando sientas que ya comprendiste el concepto y sepas qué acciones tomar, dímelo (ej. *"listo, ya entendí"*) y cerraremos la sesión.

¿Qué situación de autoconocimiento o dilema personal te gustaría analizar hoy?"""

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
                    history_formatted = [
                        {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
                        for m in st.session_state.messages[:-1]
                    ]
                    
                    chat = modelo.start_chat(history=history_formatted)
                    
                    perfil_guardado = st.session_state.perfil_usuario
                    full_prompt = (
                        f"{instrucciones_sistema}\n\n"
                        f"Información del usuario: {perfil_guardado}\n"
                        f"REGLA EXTRA: Inicia SIEMPRE tu respuesta dirigiéndote al usuario por su nombre extraído de la información anterior.\n\n"
                        f"Caso a analizar: {prompt}"
                    )
                    
                    response = chat.send_message(full_prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Error técnico: {e}. Intenta recargar la página o espera unos segundos si excediste el límite de peticiones.")

# --- PIE DE PÁGINA (Footer) ---
st.markdown(
    """
    <hr style="border: none; height: 1px; background-color: #e0e0e0; margin-top: 3rem; margin-bottom: 1rem;">
    <p style="text-align: center; font-size: 12px; color: #888888;">
        Creado por: Neguentrópicos (Johan López, Alejandra Díaz, Luis Vargas, Juan Salazar)
    </p>
    """,
    unsafe_allow_html=True
)
