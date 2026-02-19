import streamlit as st
import datetime

# --- 1. CONFIGURACIÓN Y ESTILO ---
st.set_page_config(page_title="SCA-Scores Pro", page_icon="🫀", layout="centered")

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
    st.title("🫀 SCA-Scores Pro")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📏 Escalas TIMI"): nav("t_sel")
        if st.button("🧬 HEART Score"): nav("heart")
    with col2:
        if st.button("📈 GRACE Score"): nav("grace")
        if st.button("🫁 Killip & Kimball"): nav("kk")
    st.write("---")
    st.subheader("📋 Pacientes Evaluados")
    if not st.session_state.h: st.caption("No hay registros.")
    else:
        for i in reversed(st.session_state.h):
            st.markdown(f'<div class="card"><strong>🕒 {i["t"]} - {i["e"]}</strong><br>Puntaje: {i["p"]} {i["r"]}</div>', unsafe_allow_html=True)

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
    t_qs = ["¿Edad ≥ 65?", "¿3+ Factores Riesgo?", "¿Estenosis ≥ 50%?", "¿Cambios ST?", "¿Angina Grave?", "¿Uso AAS 7d?", "¿Marcadores (+)?"]
    
    if st.session_state.step < len(t_qs):
        st.subheader(f"TIMI {st.session_state.tipo}")
        st.info(t_qs[st.session_state.step])
        col_si, col_no = st.columns(2)
        if col_si.button("SÍ (+1)"):
            st.session_state.pts += 1
            st.session_state.step += 1
            st.rerun()
        if col_no.button("NO (0)"):
            st.session_state.step += 1
            st.rerun()
    else:
        st.success(f"Puntaje Final: {st.session_state.pts}")
        if st.button("Guardar Resultado"):
            save(f"TIMI {st.session_state.tipo}", st.session_state.pts)
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
