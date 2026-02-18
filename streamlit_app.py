import streamlit as st
import datetime

# --- 1. CONFIGURACIÓN Y ESTILO (Sin límites de espacio) ---
st.set_page_config(page_title="SCA-Scores Pro", page_icon="🫀", layout="centered")

st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 15px;
        height: 4em;
        background-color: #e63946;
        color: white;
        font-weight: bold;
        border: 2px solid #1f2937;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #ba2d3a;
        border: 2px solid white;
    }
    .card {
        padding: 20px;
        background-color: #1f2937;
        border-radius: 15px;
        margin-bottom: 10px;
        border-left: 5px solid #e63946;
    }
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
    st.write("Estratificación avanzada de riesgo coronario")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📏 Escalas TIMI"): nav("t_sel")
        if st.button("🧬 HEART Score"): nav("heart")
    with col2:
        if st.button("📈 GRACE Score"): st.info("Módulo en desarrollo")
        if st.button("🫁 Killip & Kimball"): nav("kk")

    st.write("---")
    st.subheader("📋 Pacientes Evaluados")
    if not st.session_state.h:
        st.caption("No hay registros en este turno.")
    else:
        for i in reversed(st.session_state.h):
            with st.container():
                st.markdown(f"""<div class="card">
                    <strong>🕒 {i['t']} - {i['e']}</strong><br>
                    Resultado: {i['p']} puntos {i['r']}
                </div>""", unsafe_allow_html=True)

# --- 4. PANTALLA: KILLIP VISUAL (Tarjetas) ---
elif st.session_state.p == "kk":
    st.button("⬅️ Volver", on_click=lambda: nav("menu"))
    st.header("Clasificación Killip & Kimball")
    
    # Definimos los datos de las tarjetas
    killips = [
        {"cl": "I", "pts": 0, "desc": "Sin insuficiencia cardíaca. Pulmones limpios.", "img": "https://cdn-icons-png.flaticon.com/512/2491/2491280.png"},
        {"cl": "II", "pts": 20, "desc": "Estertores basales, S3, congestión hiliar.", "img": "https://cdn-icons-png.flaticon.com/512/2491/2491321.png"},
        {"cl": "III", "pts": 39, "desc": "Edema agudo de pulmón franco.", "img": "https://cdn-icons-png.flaticon.com/512/2864/2864323.png"},
        {"cl": "IV", "pts": 59, "desc": "Shock cardiogénico. Hipoperfusión sistémica.", "img": "https://cdn-icons-png.flaticon.com/512/564/564793.png"}
    ]
    
    for k in killips:
        with st.container():
            c1, c2 = st.columns([1, 3])
            c1.image(k["img"], width=80)
            with c2:
                st.subheader(f"Clase {k['cl']}")
                st.write(k["desc"])
                if st.button(f"Seleccionar Clase {k['cl']}", key=k['cl']):
                    save(f"Killip {k['cl']}", k["pts"])
        st.write("---")

# --- 5. PANTALLA: HEART SCORE ---
elif st.session_state.p == "heart":
    st.button("⬅️ Cancelar", on_click=lambda: nav("menu"))
    st.header("HEART Score")
    
    qs = [
        ("Historia", [("Levemente sospechosa", 0), ("Moderadamente sospechosa", 1), ("Altamente sospechosa", 2)]),
        ("ECG", [("Normal", 0), ("Repolarización inespecífica", 1), ("Depresión ST significativa", 2)]),
        ("Edad", [("< 45 años", 0), ("45 - 64 años", 1), ("≥ 65 años", 2)]),
        ("Factores de Riesgo", [("0 factores", 0), ("1-2 factores", 1), ("≥ 3 o enfermedad vascular", 2)]),
        ("Troponina", [("≤ Límite normal", 0), ("1-3x Límite normal", 1), ("> 3x Límite normal", 2)])
    ]
    
    actual = qs[st.session_state.step]
    st.subheader(actual[0])
    for texto, valor in actual[1]:
        if st.button(texto):
            st.session_state.pts += valor
            st.session_state.step += 1
            st.rerun()
            
    if st.session_state.step == len(qs):
        riesgo = "Bajo" if st.session_state.pts <= 3 else "Intermedio" if st.session_state.pts <= 6 else "Alto"
        save("HEART", st.session_state.pts, f"({riesgo})")

# --- 6. PANTALLA: TIMI ---
elif st.session_state.p == "t_sel":
    st.button("⬅️ Volver", on_click=lambda: nav("menu"))
    if st.button("TIMI para NSTEMI/AI"): st.session_state.tipo = "NSTEMI"; nav("t_run")
    if st.button("TIMI para STEMI"): st.session_state.tipo = "STEMI"; nav("t_run")

elif st.session_state.p == "t_run":
    st.button("⬅️ Reiniciar", on_click=lambda: nav("t_sel"))
    t_qs = ["Edad ≥ 65?", "3+ Factores Riesgo?", "Estenosis ≥ 50%?", "Cambios ST?", "Angina Grave?", "AAS 7d?", "Marcadores (+)?" ]
    
    st.subheader(f"TIMI {st.session_state.tipo}")
    st.info(t_qs[st.session_state.step])
    col_si, col_no = st.columns(2)
    if col_si.button("SÍ"):
        st.session_state.pts += 1
        st.session_state.step += 1
        st.rerun()
    if col_no.button("NO"):
        st.session_state.step += 1
        st.rerun()
        
    if st.session_state.step == len(t_qs):
        save(f"TIMI {st.session_state.tipo}", st.session_state.pts)
