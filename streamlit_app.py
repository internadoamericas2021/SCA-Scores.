import streamlit as st
import datetime
import os

# --- 1. CONFIGURACIÓN Y ESTILO ---
# Esta DEBE ser la primera instrucción de Streamlit
st.set_page_config(
    page_title="SCA-Scores Pro",
    page_icon="icono.png", 
    layout="centered"
)

# Inyectar HTML para compatibilidad con móviles (Android/iOS)
st.markdown(
    """
    <link rel="icon" href="icono.png">
    <link rel="apple-touch-icon" href="icono.png">
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 15px; height: 3.5em; background-color: #e63946; color: white; font-weight: bold; }
    .stButton>button:hover { background-color: #ba2d3a; border: 1px solid white; }
    .card { padding: 15px; background-color: #1f2937; border-radius: 15px; margin-bottom: 10px; border-left: 5px solid #e63946; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GESTIÓN DE ESTADO ---
if 'h' not in st.session_state: st.session_state.h = []
if 'p' not in st.session_state: st.session_state.p = "menu"
if 'pts' not in st.session_state: st.session_state.pts = 0
if 'step' not in st.session_state: st.session_state.step = 0
if 'tipo' not in st.session_state: st.session_state.tipo = ""

def nav(pantalla):
    st.session_state.p = pantalla
    st.session_state.pts = 0
    st.session_state.step = 0

def save(escala, puntos, riesgo=""):
    hora = datetime.datetime.now().strftime("%H:%M")
    st.session_state.h.insert(0, {"t": hora, "e": escala, "p": puntos, "r": riesgo})
    st.session_state.p = "menu"
    st.session_state.pts = 0
    st.session_state.step = 0

# --- 3. PANTALLA: MENÚ PRINCIPAL ---
# --- SECCIÓN DE AYUDA, GLOSARIO Y BIBLIOGRAFÍA ---
with st.expander("❓ Guía, Glosario y Bibliografía"):
    tab1, tab2, tab3 = st.tabs(["📖 Guía de Uso", "🔍 Glosario", "📚 Bibliografía"])
    
    with tab1:
        st.markdown("""
        **Flujo de Trabajo:**
        1. Seleccione la escala según el cuadro clínico del paciente.
        2. Ingrese los datos solicitados (ECG, biomarcadores, constantes).
        3. Observe la **Tarjeta de Resultado** con la conducta sugerida.
        4. Guarde el registro para consultas posteriores en el historial.
        """)

    with tab2:
        st.markdown("""
        | Término | Definición |
        | :--- | :--- |
        | **MACE** | Eventos Cardiacos Adversos Mayores (Muerte, IAM, Revascularización). |
        | **LSN** | Límite Superior de la Normalidad (Troponinas). |
        | **BRI** | Bloqueo de Rama Izquierda (nuevo o presumiblemente nuevo). |
        | **Killip I** | Sin signos de insuficiencia cardíaca. |
        | **Killip II** | Estertores crepitantes, S3 o hipertensión venosa capilar. |
        | **Killip III** | Edema agudo de pulmón franco. |
        | **Killip IV** | Shock cardiogénico (Hipotensión <90mmHg, oliguria). |
        """)

    with tab3:
        st.markdown("""
        **Fuentes Originales:**
        * **HEART Score:** *Sixau et al. (2008).* Chest pain in the emergency room: the HEART score.
        * **GRACE 2.0:** *Fox et al. (2014).* Improved risk prediction of mortality or heart failure in ACS.
        * **TIMI NSTEMI:** *Antman et al. (2000).* The TIMI risk score for NSTEMI/UA.
        * **TIMI STEMI:** *Morrow et al. (2000).* TIMI risk score for STEMI.
        * **Killip:** *Killip & Kimball (1967).* Treatment of myocardial infarction in a coronary care unit.
        """)
if st.session_state.p == "menu":
    col_izq, col_logo, col_tit, col_der = st.columns([1, 1, 4, 1])
    with col_logo:
        if os.path.exists("icono.png"): st.image("icono.png", width=60)
        else: st.write("❤️")
    with col_tit:
        st.markdown('<h1 style="color: #e63946; margin-left: -20px;">SCA-Scores Pro</h1>', unsafe_allow_html=True)
    
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        if os.path.exists("heart.png"): st.image("heart.png", use_container_width=True)
        st.button("ACCEDER HEART", key="btn_h", on_click=nav, args=("heart",))
        st.write("") 
        if os.path.exists("timi.png"): st.image("timi.png", use_container_width=True)
        st.button("ACCEDER TIMI", key="btn_t", on_click=nav, args=("t_sel",))

    with col2:
        if os.path.exists("grace.png"): st.image("grace.png", use_container_width=True)
        st.button("ACCEDER GRACE", key="btn_g", on_click=nav, args=("grace",))
        st.write("") 
        if os.path.exists("killip.png"): st.image("killip.png", use_container_width=True)
        st.button("ACCEDER KILLIP", key="btn_k", on_click=nav, args=("kk",))

    st.write("---")
    st.subheader("📋 Pacientes Evaluados")
    if not st.session_state.h:
        st.info("No hay registros en este turno.")
    else:
        for idx, i in enumerate(st.session_state.h):
            with st.expander(f"🕒 {i['t']} - {i['e']}"):
                st.write(f"**Resultado:** {i['p']} puntos")
                if i['r']: st.write(f"**Interpretación:** {i['r']}")
        
        if st.button("🗑️ Borrar Historial", key="del_hist"):
            st.session_state.h = []
            st.rerun()

    st.markdown("""
        <div style="margin-top: 50px; padding: 15px; background-color: #1a1a1a; border-radius: 10px; border-left: 5px solid #e63946;">
            <p style="color: #d1d5db; font-size: 0.8em; margin: 0; line-height: 1.4;">
                <b style="color: #e63946;">⚠️ AVISO MÉDICO LEGAL:</b> Esta app es apoyo clínico. El uso es responsabilidad del usuario.
            </p>
        </div> """, unsafe_allow_html=True)

# --- 4. PANTALLA: KILLIP & KIMBALL ---
elif st.session_state.p == "kk":
    st.button("⬅️ Volver al Menú", on_click=nav, args=("menu",), key="back_kk")
    st.markdown('<h2 style="color: #e63946; text-align: center;">Killip & Kimball</h2>', unsafe_allow_html=True)
    
    killips = [
        {"cl": "I", "pts": "6%", "img": "killip1.png", "interp": "Pulmones limpios."},
        {"cl": "II", "pts": "17%", "img": "killip2.png", "interp": "Estertores en bases, S3 o IY."},
        {"cl": "III", "pts": "38%", "img": "killip3.png", "interp": "Edema agudo de pulmón."},
        {"cl": "IV", "pts": "81%", "img": "killip4.png", "interp": "Shock cardiogénico."}
    ]

    for k in killips:
        with st.container():
            c1, c2 = st.columns([1.2, 2.5])
            with c1:
                if os.path.exists(k["img"]): st.image(k["img"], use_container_width=True)
                else: st.warning("Falta imagen")
            with c2:
                st.markdown(f"### Clase {k['cl']}")
                st.write(f"**Mortalidad:** {k['pts']}")
                st.write(f"**Clínica:** {k['interp']}")
                st.button(f"Seleccionar Clase {k['cl']}", key=f"btn_kk_{k['cl']}", on_click=save, args=(f"Killip {k['cl']}", k['pts'], f"Hallazgos: {k['interp']}"))
        st.write("---")

# --- 5. PANTALLA: HEART SCORE ---
elif st.session_state.p == "heart":
    st.button("⬅️ Cancelar", on_click=nav, args=("menu",))
    qs = [
        ("Historia", [("Levemente sospechosa", 0), ("Moderadamente sospechosa", 1), ("Altamente sospechosa", 2)]),
        ("ECG", [("Normal", 0), ("Repolarización inespecífica", 1), ("Depresión ST significativa", 2)]),
        ("Edad", [("< 45 años", 0), ("45 - 64 años", 1), ("≥ 65 años", 2)]),
        ("Riesgo (Factores)", [("0 factores", 0), ("1-2 factores", 1), ("≥ 3 o antecedente vascular", 2)]),
        ("Troponina", [("Normal (≤ LSN)", 0), ("1-3x LSN", 1), ("> 3x LSN", 2)])
    ]
    
    if st.session_state.step < len(qs):
        actual = qs[st.session_state.step]
        st.subheader(actual[0])
        for texto, valor in actual[1]:
            if st.button(texto, key=f"h_{st.session_state.step}_{valor}"):
                st.session_state.pts += valor
                st.session_state.step += 1
                st.rerun()
    else:
        p = st.session_state.pts
        if p <= 3:
            riesgo, tasa, color, conducta, hex_color = "Bajo", "0.9 - 1.7%", "🟢", "Alta probable / Manejo ambulatorio", "#2a9d8f"
        elif p <= 6:
            riesgo, tasa, color, conducta, hex_color = "Intermedio", "12 - 16.6%", "🟡", "Observación / Pruebas de detección de isquemia", "#e9c46a"
        else:
            riesgo, tasa, color, conducta, hex_color = "Alto", "50 - 65%", "🔴", "Estrategia invasiva temprana / Tratamiento agresivo", "#e63946"

        st.markdown(f"### {color} Resultado: {p} puntos")
        
        # TARJETA VISUAL HEART
        st.markdown(f"""
        <div style="padding: 20px; border-radius: 15px; background-color: #1f2937; border-left: 8px solid {hex_color};">
            <h4 style="margin: 0; color: white;">Riesgo {riesgo}</h4>
            <p style="margin: 5px 0; color: #d1d5db;"><b>MACE (6 semanas):</b> {tasa}</p>
            <p style="margin: 0; color: #d1d5db;"><b>Conducta:</b> {conducta}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.button("💾 Guardar en Historial", on_click=save, args=("HEART", p, f"Riesgo {riesgo} ({tasa})"), key="save_h")

# --- 6. PANTALLA: TIMI ---
elif st.session_state.p == "t_sel":
    st.button("⬅️ Volver", on_click=nav, args=("menu",))
    if st.button("NSTEMI (SCASEST)"): st.session_state.tipo = "NSTEMI"; nav("t_run"); st.rerun()
    if st.button("STEMI (SCACEST)"): st.session_state.tipo = "STEMI"; nav("t_run"); st.rerun()

elif st.session_state.p == "t_run":
    st.button("⬅️ Reiniciar", on_click=nav, args=("t_sel",))
    if st.session_state.tipo == "NSTEMI":
        t_qs = [("Edad ≥ 65?", 1), ("3+ Factores Riesgo?", 1), ("Estenosis ≥ 50%?", 1), ("Cambios ST?", 1), ("Angina Grave (2+ en 24h)?", 1), ("Uso AAS 7d?", 1), ("Marcadores (+)?", 1)]
    else:
        t_qs = [("Edad?", "especial"), ("PAS < 100 mmHg? (3 pts)", 3), ("FC > 100 lpm? (2 pts)", 2), ("Killip II-IV? (2 pts)", 2), ("Infarto Anterior o BRI? (1 pt)", 1), ("Peso < 67 kg? (1 pt)", 1), ("DM, HTA o Angina? (1 pt)", 1), ("Tiempo > 4h? (1 pt)", 1)]

    if st.session_state.step < len(t_qs):
        pregunta, puntos = t_qs[st.session_state.step]
        st.subheader(f"TIMI {st.session_state.tipo}")
        st.info(pregunta)
        if puntos == "especial":
            c1, c2, c3 = st.columns(3)
            if c1.button("≥75 (3)"): st.session_state.pts += 3; st.session_state.step += 1; st.rerun()
            if c2.button("65-74 (2)"): st.session_state.pts += 2; st.session_state.step += 1; st.rerun()
            if c3.button("<65 (0)"): st.session_state.step += 1; st.rerun()
        else:
            c1, c2 = st.columns(2)
            if c1.button("SÍ"): st.session_state.pts += puntos; st.session_state.step += 1; st.rerun()
            if c2.button("NO"): st.session_state.step += 1; st.rerun()
    else:
        p = st.session_state.pts
        tipo = st.session_state.tipo
        
        if tipo == "STEMI":
            mort = {0: "0.8%", 1: "1.6%", 2: "2.2%", 3: "4.4%", 4: "7.3%", 5: "12%", 6: "16%", 7: "23%", 8: "27%"}
            riesgo_val = mort.get(p, "≥ 36%")
            etiqueta = "Mortalidad (30 días)"
            hex_color = "#e63946" if p >= 5 else "#2a9d8f"
            conducta = "Reperfusión inmediata indicada" if p >= 3 else "Manejo estándar según protocolo"
        else:
            mace = {0: "4.7%", 1: "4.7%", 2: "8.3%", 3: "13.2%", 4: "19.9%", 5: "26.2%", 6: "40.9%", 7: "40.9%"}
            riesgo_val = mace.get(p, "40.9%")
            etiqueta = "Riesgo MACE (14 días)"
            hex_color = "#e63946" if p >= 3 else "#2a9d8f"
            conducta = "Estrategia invasiva temprana" if p >= 3 else "Evaluación no invasiva de isquemia"

        st.markdown(f"### Puntaje TIMI {tipo}: {p} pts")

        # TARJETA VISUAL TIMI
        st.markdown(f"""
        <div style="padding: 20px; border-radius: 15px; background-color: #1f2937; border-left: 8px solid {hex_color};">
            <h4 style="margin: 0; color: white;">{etiqueta}: {riesgo_val}</h4>
            <p style="margin: 10px 0 0 0; color: #d1d5db;"><b>Conducta sugerida:</b> {conducta}</p>
        </div>
        """, unsafe_allow_html=True)

        st.write("")
        st.button("💾 Guardar en Historial", on_click=save, args=(f"TIMI {tipo}", p, f"{etiqueta}: {riesgo_val}"), key="save_t")

# --- 7. PANTALLA: GRACE (CORREGIDA CON INTERPRETACIÓN DINÁMICA) ---
elif st.session_state.p == "grace":
    st.button("⬅️ Volver", on_click=nav, args=("menu",), key="back_grace")
    st.header("GRACE Score 2.0")
    st.caption("Predicción de mortalidad intrahospitalaria y a 6 meses.")

    # 1. ENTRADA DE DATOS
    col1, col2 = st.columns(2)
    with col1:
        ed = st.number_input("Edad", 18, 100, 65)
        fc = st.number_input("FC (lpm)", 30, 200, 80)
        ps = st.number_input("PAS (mmHg)", 50, 250, 120)
    with col2:
        cr = st.number_input("Creatinina (mg/dL)", 0.1, 10.0, 1.0)
        kl = st.selectbox("Clase Killip", ["I", "II", "III", "IV"])
    
    c3, c4, c5 = st.columns(3)
    paro = c3.checkbox("Paro al ingreso")
    st_seg = c4.checkbox("Desviación ST")
    enzimas = c5.checkbox("Enzimas (+)")

    # 2. MOTOR DE CÁLCULO (Se ejecuta siempre)
    pts = 0
    # Puntos por Edad
    if ed < 40: pts += 0
    elif ed < 50: pts += 18
    elif ed < 60: pts += 36
    elif ed < 70: pts += 55
    elif ed < 80: pts += 73
    else: pts += 91
    
    # Puntos por FC
    if fc < 70: pts += 0
    elif fc < 100: pts += 7
    elif fc < 150: pts += 24
    elif fc < 200: pts += 46
    else: pts += 64
    
    # Puntos por PAS
    if ps < 80: pts += 63
    elif ps < 100: pts += 53
    elif ps < 120: pts += 43
    elif ps < 140: pts += 34
    elif ps < 160: pts += 24
    else: pts += 0
    
    # Puntos por Creatinina
    if cr < 0.4: pts += 1
    elif cr < 0.8: pts += 4
    elif cr < 1.2: pts += 7
    elif cr < 1.6: pts += 10
    elif cr < 2.0: pts += 13
    else: pts += 21
    
    if paro: pts += 43
    if st_seg: pts += 30
    if enzimas: pts += 15
    pts += {"I": 0, "II": 21, "III": 43, "IV": 64}[kl]

    st.write("---")

    # 3. LÓGICA DE INTERPRETACIÓN (Aparece automáticamente)
    if pts > 140:
        riesgo_cat, color, conducta = "Alto", "🔴", "Estrategia invasiva temprana (< 24h)"
        mortalidad = "> 3%"
    elif pts > 108:
        riesgo_cat, color, conducta = "Intermedio", "🟡", "Estrategia invasiva en hospitalización"
        mortalidad = "1% - 3%"
    else:
        riesgo_cat, color, conducta = "Bajo", "🟢", "Manejo conservador / Evaluación no invasiva"
        mortalidad = "< 1%"

    # 4. MOSTRAR RESULTADOS
    st.markdown(f"### {color} Puntaje GRACE: {pts} puntos")
    
    # Tarjeta de interpretación
    st.markdown(f"""
    <div style="padding: 20px; border-radius: 15px; background-color: #1f2937; border-left: 8px solid {'#e63946' if pts > 108 else '#2a9d8f'};">
        <h4 style="margin: 0; color: white;">Riesgo {riesgo_cat}</h4>
        <p style="margin: 5px 0; color: #d1d5db;"><b>Mortalidad Intrahospitalaria:</b> {mortalidad}</p>
        <p style="margin: 0; color: #d1d5db;"><b>Conducta:</b> {conducta}</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    
    # 5. BOTÓN DE GUARDADO
    st.button("💾 Guardar en Historial", 
              on_click=save, 
              args=("GRACE", pts, f"Riesgo {riesgo_cat} ({mortalidad}) - {conducta}"),
              key="save_grace_final")

    st.write("---")
    # Tabla de referencia estática
    st.caption("Referencia rápida de mortalidad intrahospitalaria:")
    st.table({
        "Categoría": ["Bajo", "Intermedio", "Alto"],
        "Puntos": ["≤ 108", "109 - 140", "> 140"],
        "Mortalidad": ["< 1%", "1 - 3%", "> 3%"]
    })
