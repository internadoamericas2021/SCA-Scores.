import streamlit as st
import datetime

# --- 1. CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="SCA-Scores Pro", page_icon="logo.png", layout="centered")

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

def nav(pantalla):
    st.session_state.p = pantalla
    st.session_state.pts = 0
    st.session_state.step = 0
    st.rerun()

def save(escala, puntos, riesgo=""):
    hora = datetime.datetime.now().strftime("%H:%M")
    st.session_state.h.append({"t": hora, "e": escala, "p": puntos, "r": riesgo})
    nav("menu")

# --- 3. PANTALLA: MENÚ PRINCIPAL ---
if st.session_state.p == "menu":
    import os

    # Encabezado con tu nuevo Logotipo
    col_logo, col_tit = st.columns([1, 5])
    
    with col_logo:
        # Buscamos el archivo que renombraste a logo.png
        if os.path.exists("logo.png"):
            st.image("logo.png", width=70)
       
    with col_tit:
        # Título alineado con el logo
        st.markdown('<h1 style="color: #e63946; margin-top: 5px; font-size: 2.2em;">SCA-Scores Pro</h1>', unsafe_allow_html=True)
    
    st.write("---")

    # (Aquí sigue el resto de tu rejilla de imágenes y botones que ya funciona)

    # Creamos la rejilla
    col1, col2 = st.columns(2)

    with col1:
        # HEART SCORE
        st.image("heart.png", use_container_width=True)
        if st.button("ACCEDER HEART", key="btn_h", use_container_width=True):
            nav("heart")
        
        st.write("") # Espaciador

        # TIMI SCORE
        st.image("timi.png", use_container_width=True)
        if st.button("ACCEDER TIMI", key="btn_t", use_container_width=True):
            nav("t_sel")

    with col2:
        # GRACE SCORE
        st.image("grace.png", use_container_width=True)
        if st.button("ACCEDER GRACE", key="btn_g", use_container_width=True):
            nav("grace")

        st.write("") # Espaciador

        # KILLIP & KIMBALL
        st.image("killip.png", use_container_width=True)
        if st.button("ACCEDER KILLIP", key="btn_k", use_container_width=True):
            nav("kk")

    # --- SECCIÓN DE REGISTROS (HISTORIAL) ---
    st.write("---")
    st.subheader("📋 Pacientes Evaluados")
    
    if not st.session_state.h:
        st.info("No hay registros en este turno.")
    else:
        for idx, i in enumerate(reversed(st.session_state.h)):
            with st.expander(f"🕒 {i['t']} - {i['e']}"):
                st.write(f"**Resultado:** {i['p']} puntos")
                if i['r']:
                    st.write(f"**Interpretación:** {i['r']}")
        
        if st.button("🗑️ Borrar Todo", key="del_hist"):
            st.session_state.h = []
            st.rerun()

# --- AQUÍ CONTINÚA EL RESTO DE TUS PANTALLAS (elif st.session_state.p == "kk", etc) ---

# --- 4. PANTALLA: KILLIP VISUAL ---
elif st.session_state.p == "kk":
    st.button("⬅️ Volver", on_click=lambda: nav("menu"))
    killips = [
        {"cl": "I", "pts": 0, "de": "Sin falla cardíaca. Pulmones limpios.", "img": "https://cdn-icons-png.flaticon.com/512/2491/2491280.png"},
        {"cl": "II", "pts": 20, "de": "Estertores basales, S3.", "img": "https://cdn-icons-png.flaticon.com/512/2491/2491321.png"},
        {"cl": "III", "pts": 39, "de": "Edema agudo de pulmón.", "img": "https://cdn-icons-png.flaticon.com/512/2864/2864323.png"},
        {"cl": "IV", "pts": 59, "de": "Shock cardiogénico.", "img": "https://cdn-icons-png.flaticon.com/512/564/564793.png"}
    ]
    for k in killips:
        c1, c2 = st.columns([1, 3])
        c1.image(k["img"], width=80)
        if c2.button(f"Seleccionar Clase {k['cl']}: {k['de']}", key=k['cl']):
            save(f"Killip {k['cl']}", k["pts"])

# --- 5. PANTALLA: HEART SCORE (CORREGIDA) ---
elif st.session_state.p == "heart":
    st.button("⬅️ Cancelar", on_click=lambda: nav("menu"))
    qs = [
        ("Historia", [("Levemente sospechosa", 0), ("Moderadamente sospechosa", 1), ("Altamente sospechosa", 2)]),
        ("ECG", [("Normal", 0), ("Repolarización inespecífica", 1), ("Depresión ST significativa", 2)]),
        ("Edad", [("< 45 años", 0), ("45 - 64 años", 1), ("≥ 65 años", 2)]),
        ("Riesgo", [("0 factores", 0), ("1-2 factores", 1), ("≥ 3 o antecedente vascular", 2)]),
        ("Troponina", [("Normal", 0), ("1-3x Límite", 1), ("> 3x Límite", 2)])
    ]
    
    if st.session_state.step < len(qs):
        actual = qs[st.session_state.step]
        st.subheader(actual[0])
        for texto, valor in actual[1]:
            if st.button(texto):
                st.session_state.pts += valor
                st.session_state.step += 1
                st.rerun()
    else:
        riesgo = "Bajo" if st.session_state.pts <= 3 else "Intermedio" if st.session_state.pts <= 6 else "Alto"
        st.success(f"Resultado: {st.session_state.pts} puntos ({riesgo})")
        if st.button("Guardar en Historial"):
            save("HEART", st.session_state.pts, f"({riesgo})")

# --- 6. PANTALLA: TIMI ---
elif st.session_state.p == "t_sel":
    st.button("⬅️ Volver", on_click=lambda: nav("menu"))
    if st.button("NSTEMI (SCASEST)"): st.session_state.tipo = "NSTEMI"; nav("t_run")
    if st.button("STEMI (SCACEST)"): st.session_state.tipo = "STEMI"; nav("t_run")

elif st.session_state.p == "t_run":
    st.button("⬅️ Reiniciar", on_click=lambda: nav("t_sel"))
    
    # 1. Definición de preguntas según el caso
    if st.session_state.tipo == "NSTEMI":
        t_qs = [
            ("Edad ≥ 65?", 1), ("3+ Factores Riesgo?", 1), ("Estenosis ≥ 50%?", 1),
            ("Cambios ST?", 1), ("Angina Grave (2+ en 24h)?", 1), ("Uso AAS 7d?", 1), ("Marcadores (+)?", 1)
        ]
    else: # STEMI
        t_qs = [
            ("Edad ≥ 75? (3 pts) o 65-74? (2 pts)", "especial"), 
            ("PAS < 100 mmHg? (3 pts)", 3),
            ("FC > 100 lpm? (2 pts)", 2),
            ("Killip II-IV? (2 pts)", 2),
            ("Infarto Anterior o BRI? (1 pt)", 1),
            ("Peso < 67 kg? (1 pt)", 1),
            ("DM, HTA o Angina previa? (1 pt)", 1),
            ("Tiempo reperfusión > 4h? (1 pt)", 1)
        ]

    # 2. Lógica de preguntas
    if st.session_state.step < len(t_qs):
        st.subheader(f"TIMI {st.session_state.tipo}")
        pregunta, puntos = t_qs[st.session_state.step]
        st.info(pregunta)
        
        if pregunta.startswith("Edad"): # Manejo especial para edad en STEMI
            if st.session_state.tipo == "STEMI":
                c1, c2, c3 = st.columns(3)
                if c1.button("≥ 75"): st.session_state.pts += 3; st.session_state.step += 1; st.rerun()
                if c2.button("65-74"): st.session_state.pts += 2; st.session_state.step += 1; st.rerun()
                if c3.button("< 65"): st.session_state.step += 1; st.rerun()
            else: # NSTEMI común
                c1, c2 = st.columns(2)
                if c1.button("SÍ"): st.session_state.pts += 1; st.session_state.step += 1; st.rerun()
                if c2.button("NO"): st.session_state.step += 1; st.rerun()
        else:
            c1, c2 = st.columns(2)
            if c1.button("SÍ"):
                st.session_state.pts += puntos
                st.session_state.step += 1
                st.rerun()
            if c2.button("NO"):
                st.session_state.step += 1
                st.rerun()
                
    # 3. Interpretación de resultados
    else:
        p_total = st.session_state.pts
        if st.session_state.tipo == "STEMI":
            # Tabla de mortalidad STEMI a 30 días
            mortalidad = {
                0: "0.8%", 1: "1.6%", 2: "2.2%", 3: "4.4%", 4: "7.3%", 
                5: "12%", 6: "16%", 7: "23%", 8: "27%", 9: "36%"
            }
            riesgo_txt = mortalidad.get(p_total, "> 36%")
            color = "🔴" if p_total >= 5 else "🟡" if p_total >= 3 else "🟢"
            
            st.markdown(f"### {color} Puntaje TIMI STEMI: {p_total}")
            st.metric("Mortalidad estimada (30 días)", riesgo_txt)
        else:
            # (Aquí va la lógica de NSTEMI que ya pusimos antes...)
            riesgo_txt = "Calculado" 
            st.write(f"Puntaje NSTEMI: {p_total}")

        if st.button("💾 Guardar"):
            save(f"TIMI {st.session_state.tipo}", p_total, f"({riesgo_txt})")
elif st.session_state.p == "grace":
    st.button("⬅️ Volver", on_click=lambda: nav("menu"))
    st.header("GRACE Score 2.0")
    st.caption("Predicción de mortalidad intrahospitalaria y a 6 meses.")

    with st.form("grace_form"):
        col1, col2 = st.columns(2)
        with col1:
            edad = st.number_input("Edad", 18, 100, 65)
            fc = st.number_input("Frecuencia Cardíaca (lpm)", 30, 200, 80)
            pas = st.number_input("Presión Sistólica (mmHg)", 50, 250, 120)
        with col2:
            creat = st.number_input("Creatinina (mg/dL)", 0.1, 10.0, 1.0)
            kk = st.selectbox("Clase Killip", ["I", "II", "III", "IV"])
        
        st.write("---")
        paro = st.checkbox("Paro cardíaco al ingreso")
        st_seg = st.checkbox("Desviación del segmento ST")
        enzimas = st.checkbox("Enzimas cardíacas elevadas")
        
        submit = st.form_submit_button("Calcular Riesgo GRACE")

    if submit:
        # (Lógica de puntos que ya teníamos...)
        pts = 0
        if edad < 40: pts += 0
        elif edad < 50: pts += 18
        elif edad < 60: pts += 36
        elif edad < 70: pts += 55
        elif edad < 80: pts += 73
        else: pts += 91
        
        if fc < 70: pts += 0
        elif fc < 100: pts += 7
        elif fc < 150: pts += 24
        elif fc < 200: pts += 46
        else: pts += 64

        if pas < 80: pts += 63
        elif pas < 100: pts += 53
        elif pas < 120: pts += 43
        elif pas < 140: pts += 34
        elif pas < 160: pts += 24
        else: pts += 0

        if creat < 0.4: pts += 1
        elif creat < 0.8: pts += 4
        elif creat < 1.2: pts += 7
        elif creat < 1.6: pts += 10
        elif creat < 2.0: pts += 13
        else: pts += 21

        if paro: pts += 43
        if st_seg: pts += 30
        if enzimas: pts += 15
        
        dict_kk = {"I": 0, "II": 21, "III": 43, "IV": 64}
        pts += dict_kk[kk]

        # --- NUEVA SECCIÓN DE RESULTADOS Y TABLA ---
        st.subheader(f"Resultado: {pts} puntos")
        
        if pts > 140:
            riesgo_cat = "Alto"
            color = "🔴"
            conducta = "Estrategia invasiva temprana (< 24h)"
        elif pts > 108:
            riesgo_cat = "Intermedio"
            color = "🟡"
            conducta = "Estrategia invasiva en la hospitalización"
        else:
            riesgo_cat = "Bajo"
            color = "🟢"
            conducta = "Manejo conservador / Evaluación no invasiva"

        st.markdown(f"### {color} Riesgo {riesgo_cat}")
        
        # Tabla de Recomendación Clínica
        data = {
            "Categoría de Riesgo": ["Muy Alto", "Alto (GRACE >140)", "Bajo/Intermedio"],
            "Tiempo de Reperfusión": ["Inmediata (<2h)", "Temprana (<24h)", "Selectiva"],
            "Criterios": ["Inestabilidad HD/Eléctrica", "Cambios dinámicos ST", "Estable sin cambios"]
        }
        st.table(data)
        
        st.info(f"**Conducta sugerida:** {conducta}")

        if st.button("💾 Guardar en Historial"):
            save("GRACE", pts, f"({riesgo_cat} - {conducta})")
