
import streamlit as st
import pandas as pd
from auth import validar_usuario
from dashboard import mostrar_dashboard
from clientes import mostrar_clientes
from notion_api import obtener_datos_notion

st.set_page_config(page_title="AAFF CRM", layout="wide")

NOTION_TOKEN = "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"
DATABASE_ID = "2112a72faa1f800e9de5d5a6a2a7a003"

with open("styles.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

usuarios_df = pd.read_excel("usuarios.xlsx")

if "logueado" not in st.session_state:
    st.session_state.logueado = False
if "nombre_colaborador" not in st.session_state:
    st.session_state.nombre_colaborador = ""
if "rol" not in st.session_state:
    st.session_state.rol = ""
if "seccion" not in st.session_state:
    st.session_state.seccion = "Dashboard"

def login():
    st.sidebar.image("img_login.png", use_container_width=True)
    st.sidebar.markdown("## Iniciar sesión")
    usuario_input = st.sidebar.text_input("Usuario")
    password_input = st.sidebar.text_input("Contraseña", type="password")
    if st.sidebar.button("Entrar"):
        nombre_colaborador, rol = validar_usuario(usuario_input, password_input, usuarios_df)
        if nombre_colaborador:
            st.session_state.logueado = True
            st.session_state.nombre_colaborador = nombre_colaborador
            st.session_state.rol = rol
            st.rerun()
        else:
            st.sidebar.error("Usuario o contraseña incorrectos")

def main():
    st.sidebar.markdown("### Menú")

    # Agregar la opción "Alertas" al menú lateral (eliminamos la opción de alertas)
    st.session_state.seccion = st.sidebar.radio("Ir a", ["Dashboard", "Clientes", "Facturas"], index=0)

    if st.sidebar.button("Cerrar sesión"):
        st.session_state.logueado = False
        st.rerun()

    df = obtener_datos_notion(NOTION_TOKEN, DATABASE_ID)
    if df.empty:
        st.warning("No se pudieron cargar los datos desde Notion.")
        return

    if st.session_state.rol.lower() != "admin":
        df = df[df["USUARIO"] == st.session_state.nombre_colaborador]

    if st.session_state.seccion == "Dashboard":
        mostrar_dashboard(df)
    elif st.session_state.seccion == "Clientes":
        mostrar_clientes(df)
    elif st.session_state.seccion == "Facturas":
        st.subheader("📄 Facturas")
        st.info("Aquí irán las facturas y sus visualizaciones.")

if not st.session_state.logueado:
    login()
else:
    main()
