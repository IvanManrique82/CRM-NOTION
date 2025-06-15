
import streamlit as st
import plotly.express as px
import pandas as pd

def mostrar_dashboard(df):
    st.subheader("📊 Resumen visual de contratos")

    nombre_usuario = st.session_state.get("nombre_colaborador", "")
    es_ivan = nombre_usuario == "Ivan Manrique"

    # Filtros avanzados
    with st.expander("🔍 Filtros avanzados", expanded=True):
        col1, col2, col3, col4 = st.columns(4)

        meses_disponibles = df["MES AÑO"].dropna().unique().tolist()
        opciones_mes = ["Todos"] + sorted(meses_disponibles)

        with col1:
            mes = st.selectbox("Mes", options=opciones_mes, index=len(opciones_mes)-1)

        with col2:
            tipo_contrato = st.selectbox("Tipo de contrato", options=["Todos"] + sorted(df["TIPO CONTRATO"].dropna().unique().tolist()))

        with col3:
            comercializadora = st.selectbox("Comercializadora", options=["Todos"] + sorted(df["COMERCIALIZADORA"].dropna().unique().tolist()))

        with col4:
            usuario = st.selectbox("Usuario", options=["Todos"] + sorted(df["USUARIO"].dropna().unique().tolist()))

    # Aplicar filtros
    df_filtrado = df.copy()
    if mes != "Todos":
        df_filtrado = df_filtrado[df_filtrado["MES AÑO"] == mes]
    if tipo_contrato != "Todos":
        df_filtrado = df_filtrado[df_filtrado["TIPO CONTRATO"] == tipo_contrato]
    if comercializadora != "Todos":
        df_filtrado = df_filtrado[df_filtrado["COMERCIALIZADORA"] == comercializadora]
    if usuario != "Todos":
        df_filtrado = df_filtrado[df_filtrado["USUARIO"] == usuario]

    # Filtrar los contratos que no están en estado "Baja" ni "Activado"
    contratos_pendientes = df_filtrado[~df_filtrado["ESTADO"].isin(["Baja", "Activado"])]

    # KPIs filtrados
    total_clientes = df_filtrado["CLIENTE"].nunique()
    total_cups = df_filtrado["CUPS"].nunique()
    contratos_nuevos = len(df_filtrado)

    total_comisiones = df_filtrado["Comision"].sum() if es_ivan else df_filtrado["Comision COLABORADOR"].sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("👥 Total clientes", total_clientes)
    col2.metric("⚡ CUPS únicos", total_cups)
    col3.metric("📥 Contratos este mes", contratos_nuevos)
    col4.metric("💰 Comisiones del mes", f"{total_comisiones:,.2f} €")

    with st.expander(f"📌 Contratos pendientes de cerrar: {len(contratos_pendientes)}"):
        st.dataframe(contratos_pendientes[["CLIENTE", "CUPS", "ESTADO", "COMERCIALIZADORA", "TARIFA"]], use_container_width=True)

    # Gráficos
    col1, col2, col3 = st.columns(3)

    with col1:
        if 'TARIFA' in df_filtrado.columns:
            tarifa_counts = df_filtrado['TARIFA'].value_counts().reset_index()
            tarifa_counts.columns = ['Tarifa', 'Total']
            fig_tarifa = px.pie(
                tarifa_counts,
                values='Total',
                names='Tarifa',
                title='CUPS por Tarifa',
                hole=0.5
            )
            fig_tarifa.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_tarifa, use_container_width=True)

    with col2:
        if 'COMERCIALIZADORA' in df_filtrado.columns:
            comercializadora_counts = df_filtrado['COMERCIALIZADORA'].value_counts().reset_index()
            comercializadora_counts.columns = ['Comercializadora', 'Total Contratos']
            fig_comercializadora = px.pie(
                comercializadora_counts,
                values='Total Contratos',
                names='Comercializadora',
                title='Contratos por Comercializadora',
                hole=0.5
            )
            fig_comercializadora.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_comercializadora, use_container_width=True)

    with col3:
        if 'TIPO CLIENTE' in df_filtrado.columns:
            tipo_cliente_counts = df_filtrado['TIPO CLIENTE'].value_counts().reset_index()
            tipo_cliente_counts.columns = ['Tipo Cliente', 'Total']
            fig_cliente = px.pie(
                tipo_cliente_counts,
                values='Total',
                names='Tipo Cliente',
                title='Contratos por Tipo de Cliente',
                hole=0.5
            )
            fig_cliente.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_cliente, use_container_width=True)
