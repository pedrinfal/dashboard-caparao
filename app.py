# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import json
from config import * # Importa todas as variáveis do config.py

# --- Configuração da Página ---
st.set_page_config(page_title="Resumo Caparaó", layout="wide")

# --- Função para Carregar os Dados ---
# A anotação @st.cache_data implementa o lazy loading.
@st.cache_data
def load_all_data():
    """
    Carrega dados do cidades.csv e das diferentes abas do arquivo 
    base_de_dados.xlsx.
    """
    try:
        # --- Carrega o CSV principal ---
        df = pd.read_csv(CIDADES_FILE, sep=",", decimal=",")
        # (Tratamento das colunas de cidades.csv)
        df[HABITANTES_COL] = df[HABITANTES_COL].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float)
        df[POP_ATIVA_COL] = df[POP_ATIVA_COL].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float)
        df[POP_ESTIMADA_COL] = df[POP_ESTIMADA_COL].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float)
        df[IDH_COL] = df[IDH_COL].astype(float)
        df[POP_OCUPADA_COL] = df[POP_OCUPADA_COL].str.replace(",", ".").str.replace("%", "").astype(float)
        df[RENDA_PER_CAPITA_SM_COL] = df[RENDA_PER_CAPITA_SM_COL].astype(str).str.replace(",", ".").astype(float)
        df[PIB_PER_CAPITA_COL] = (
            df[PIB_PER_CAPITA_COL]
            .str.replace("R\$", "", regex=True)
            .str.replace(" ", "")
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
            .astype(float)
        )

        # --- Carrega dados das ABAS do arquivo Excel ---
        data = {
            'cidades': df,
            'geo_dados': pd.read_excel(BASE_DE_DADOS_XLSX_FILE, sheet_name=SHEET_GEO),
            'empregos_setor': pd.read_excel(BASE_DE_DADOS_XLSX_FILE, sheet_name=SHEET_EMPREGOS_SETOR),
            'empregos_faixa_etaria': pd.read_excel(BASE_DE_DADOS_XLSX_FILE, sheet_name=SHEET_EMPREGOS_FAIXA),
            'empresas': pd.read_excel(BASE_DE_DADOS_XLSX_FILE, sheet_name=SHEET_EMPRESas),
            'instituicoes_ensino': pd.read_excel(BASE_DE_DADOS_XLSX_FILE, sheet_name=SHEET_INST_ENSINO),
            'ideb': pd.read_excel(BASE_DE_DADOS_XLSX_FILE, sheet_name=SHEET_IDEB),
            'instituicoes': pd.read_excel(BASE_DE_DADOS_XLSX_FILE, sheet_name=SHEET_INSTITUICOES),
        }

        # Carregar GeoJSON
        with open(GEOJSON_FILE, "r", encoding="utf-8") as f:
            geojson_data = json.load(f)
        data['geojson'] = geojson_data

        return data

    except FileNotFoundError as e:
        st.error(f"Erro: Arquivo não encontrado - {e.filename}. Verifique se os arquivos 'cidades.csv', 'base_de_dados.xlsx' e 'municipios_caparao.geojson' estão na mesma pasta que o script 'app.py'.")
        return None
    except ValueError as e:
        st.error(f"Erro ao ler o arquivo Excel: {e}. Verifique se os nomes das abas no arquivo 'config.py' correspondem exatamente aos nomes das abas no seu arquivo 'base_de_dados.xlsx'.")
        return None
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado ao carregar os dados: {e}")
        return None

# --- O restante do código permanece exatamente o mesmo ---
# (O código abaixo é idêntico ao anterior, apenas a função de carregar dados mudou)

data = load_all_data()

if data:
    # --- TÍTULO ---
    st.markdown("<h1 style='text-align:center; color: #0dcaf0;'>Dashboard Gênesis Caparaó</h1>", unsafe_allow_html=True)

    # --- MAPA E FILTRO ---
    st.markdown("<h2 style='text-align:center;'>Mapa Interativo e Filtro Municipal</h2>", unsafe_allow_html=True)

    fig_mapa = px.choropleth_mapbox(
        data['cidades'],
        geojson=data['geojson'],
        locations="MUNICIPIO",
        featureidkey="properties.NM_MUN",
        color=IDH_COL,
        color_continuous_scale="Viridis",
        mapbox_style="carto-positron",
        center={"lat": -20.45, "lon": -41.5},
        zoom=8,
        opacity=0.6,
        hover_data={"MUNICIPIO": True, IDH_COL: True, PIB_PER_CAPITA_COL: ':.2f'}
    )
    fig_mapa.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_mapa, use_container_width=True)

    # --- Caixa de Seleção ---
    municipios_options = ["Visão Regional"] + sorted(data['cidades']["MUNICIPIO"].unique())
    municipio_escolhido = st.selectbox(
        "Selecione o município para filtrar os dados ou escolha 'Visão Regional' para ver o consolidado:",
        options=municipios_options
    )

    # --- Filtragem dos Dados ---
    is_regional_view = (municipio_escolhido == "Visão Regional")
    
    if is_regional_view:
        df_cidades_filtrado = data['cidades']
        df_empregos_setor = data['empregos_setor'].groupby(SETOR_COL, as_index=False)[EMPREGADOS_SETOR_VAL_COL].sum()
        df_empregos_faixa = data['empregos_faixa_etaria'].groupby(FAIXA_ETARIA_COL, as_index=False)[EMPREGADOS_FAIXA_ETARIA_VAL_COL].sum()
        df_empresas = data['empresas'].groupby(PORTE_EMPRESA_COL, as_index=False)[EMPRESAS_QTD_COL].sum()
        df_inst_ensino_rede = data['instituicoes_ensino'].groupby(REDE_ENSINO_COL, as_index=False).size().rename(columns={'size': INST_ENSINO_QTD_COL})
        df_inst_ensino_nivel = data['instituicoes_ensino'].groupby(NIVEL_ENSINO_COL, as_index=False).size().rename(columns={'size': INST_ENSINO_QTD_COL})
        df_ideb = data['ideb'].groupby(ETAPA_ENSINO_COL, as_index=False)[IDEB_VAL_COL].mean()
        df_instituicoes = data['instituicoes'].groupby(CATEGORIA_INST_COL, as_index=False).size().rename(columns={'size': INST_CATEGORIA_QTD_COL})
        df_geo = data['geo_dados'].groupby(ZONA_COL, as_index=False)[PERCENTUAL_COL].mean()
        df_inst_cards = data['instituicoes']
    else:
        df_cidades_filtrado = data['cidades'][data['cidades'][MUNICIPIO_COL] == municipio_escolhido]
        df_empregos_setor = data['empregos_setor'][data['empregos_setor'][MUNICIPIO_COL] == municipio_escolhido]
        df_empregos_faixa = data['empregos_faixa_etaria'][data['empregos_faixa_etaria'][MUNICIPIO_COL] == municipio_escolhido]
        df_empresas = data['empresas'][data['empresas'][MUNICIPIO_COL] == municipio_escolhido]
        df_inst_ensino_rede = data['instituicoes_ensino'][data['instituicoes_ensino'][MUNICIPIO_COL] == municipio_escolhido].groupby(REDE_ENSINO_COL, as_index=False).size().rename(columns={'size': INST_ENSINO_QTD_COL})
        df_inst_ensino_nivel = data['instituicoes_ensino'][data['instituicoes_ensino'][MUNICIPIO_COL] == municipio_escolhido].groupby(NIVEL_ENSINO_COL, as_index=False).size().rename(columns={'size': INST_ENSINO_QTD_COL})
        df_ideb = data['ideb'][data['ideb'][MUNICIPIO_COL] == municipio_escolhido]
        df_instituicoes = data['instituicoes'][data['instituicoes'][MUNICIPIO_COL] == municipio_escolhido].groupby(CATEGORIA_INST_COL, as_index=False).size().rename(columns={'size': INST_CATEGORIA_QTD_COL})
        df_geo = data['geo_dados'][data['geo_dados'][MUNICIPIO_COL] == municipio_escolhido]
        df_inst_cards = data['instituicoes'][data['instituicoes'][MUNICIPIO_COL] == municipio_escolhido]

    st.markdown("<hr style='margin-top:2em; margin-bottom:2em;'>", unsafe_allow_html=True)
    
    # --- Título Dinâmico ---
    view_title = "Resumo da Região do Caparaó" if is_regional_view else f"Resumo de {municipio_escolhido}"
    st.markdown(f"<h2 style='text-align:center;'>{view_title}</h2>", unsafe_allow_html=True)

    # --- KPIs ---
    if not df_cidades_filtrado.empty:
        idh_medio = df_cidades_filtrado[IDH_COL].mean()
        pib_per_capita = df_cidades_filtrado[PIB_PER_CAPITA_COL].mean()
        pop_estimada = df_cidades_filtrado[POP_ESTIMADA_COL].sum()
        habitantes = df_cidades_filtrado[HABITANTES_COL].sum()
        pop_idade_ativa = df_cidades_filtrado[POP_ATIVA_COL].sum()
        perc_pop_ocupada = df_cidades_filtrado[POP_OCUPADA_COL].mean()
        renda_per_capita_sm = df_cidades_filtrado[RENDA_PER_CAPITA_SM_COL].mean()
        perc_pop_ativa = (pop_idade_ativa / habitantes) * 100 if habitantes > 0 else 0

        def kpi_card(title, value, emoji, color="#000"):
            st.markdown(f"""
            <div style='border-radius: 10px; margin: 1em; padding: 15px; background-color: #f8f9fa; text-align: center;
                         box-shadow: 0 2px 4px rgba(0,0,0,0.1); height: 100%;'>
                <div style='font-size: 24px'>{emoji}</div>
                <div style='font-size: 13px; color: grey'>{title}</div>
                <div style='font-size: 20px; font-weight: bold; color:{color}'>{value}</div>
            </div>""", unsafe_allow_html=True)

        cols = st.columns(4)
        with cols[0]: kpi_card("IDH MÉDIO", f"{idh_medio:.3f}", "📈", "#FFA500")
        with cols[1]: kpi_card("PIB PER CAPITA", f"R$ {pib_per_capita:,.2f}", "💰", "#28a745")
        with cols[2]: kpi_card("POP. ESTIMADA 2024", f"{pop_estimada:,.0f}", "👥", "#007bff")
        with cols[3]: kpi_card("HABITANTES (CENSO)", f"{habitantes:,.0f}", "🏡", "#6f42c1")
        
        cols = st.columns(4)
        with cols[0]: kpi_card("POP. IDADE ATIVA", f"{pop_idade_ativa:,.0f}", "💪", "#dc3545")
        with cols[1]: kpi_card("% POP. ATIVA", f"{perc_pop_ativa:.1f}%", "🧠", "#6c757d")
        with cols[2]: kpi_card("% POP. OCUPADA", f"{perc_pop_ocupada:.1f}%", "👷", "#ffc107")
        with cols[3]: kpi_card("RENDA PER CAPITA (SM)", f"{renda_per_capita_sm:.2f}", "💵", "#20c997")

    st.markdown("<hr style='margin-top:2em; margin-bottom:2em;'>", unsafe_allow_html=True)
    
    # --- SEÇÕES DE GRÁFICOS ---
    # (O restante do código para exibir os gráficos é idêntico e não precisa ser alterado)

    # --- GEOGRAFIA ---
    if not df_geo.empty:
        st.markdown("<h3 style='text-align:center;'>Concentração Geográfica</h3>", unsafe_allow_html=True)
        # Handle potential empty results after filtering
        zona_urbana_df = df_geo[df_geo[ZONA_COL] == 'Urbana']
        zona_rural_df = df_geo[df_geo[ZONA_COL] == 'Rural']
        zona_urbana = zona_urbana_df[PERCENTUAL_COL].values[0] if not zona_urbana_df.empty else 0
        zona_rural = zona_rural_df[PERCENTUAL_COL].values[0] if not zona_rural_df.empty else 0

        geo_df_pie = pd.DataFrame({'Zona': ['Urbana', 'Rural'], 'Valor': [zona_urbana, zona_rural]})
        fig_geo = px.pie(geo_df_pie, names='Zona', values='Valor', hole=0.5, color_discrete_sequence=['#1f77b4', '#2ca02c'])
        fig_geo.update_traces(textinfo='none')
        fig_geo.update_layout(showlegend=False, margin=dict(t=20, b=20))
        
        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            st.plotly_chart(fig_geo, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1: st.markdown(f'<div style="text-align: center;">🏙️ <b>ZONA URBANA</b><h3 style="color:#1f77b4;">{zona_urbana:.2f}%</h3></div>', unsafe_allow_html=True)
        with col2: st.markdown(f'<div style="text-align: center;">🏡 <b>ZONA RURAL</b><h3 style="color:#2ca02c;">{zona_rural:.2f}%</h3></div>', unsafe_allow_html=True)
        st.markdown("<hr style='margin-top:2em; margin-bottom:2em;'>", unsafe_allow_html=True)

    # --- ECONOMIA ---
    st.markdown("<h2 style='text-align:center;'>Economia e Mercado de Trabalho</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h4 style='text-align:center;'>Empregos por Setor</h4>", unsafe_allow_html=True)
        if not df_empregos_setor.empty:
            fig = px.bar(df_empregos_setor.sort_values(EMPREGADOS_SETOR_VAL_COL, ascending=False), 
                         x=SETOR_COL, y=EMPREGADOS_SETOR_VAL_COL, color=SETOR_COL, text_auto='.2s')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Não há dados de empregos por setor para a seleção atual.")
    with col2:
        st.markdown("<h4 style='text-align:center;'>Empregos por Faixa Etária</h4>", unsafe_allow_html=True)
        if not df_empregos_faixa.empty:
            fig = px.bar(df_empregos_faixa, x=FAIXA_ETARIA_COL, y=EMPREGADOS_FAIXA_ETARIA_VAL_COL,
                         color=FAIXA_ETARIA_COL, text_auto='.2s')
            fig.update_layout(showlegend=False, xaxis={'categoryorder':'array', 'categoryarray':["15-17", "18-24", "25-29", "30-39", "40-49", "50-64", "65-mais"]})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Não há dados de empregos por faixa etária para a seleção atual.")

    # --- EMPREENDEDORISMO ---
    st.markdown("<h2 style='text-align:center;'>Empresas e Empreendedorismo</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h4 style='text-align:center;'>Empresas por Porte</h4>", unsafe_allow_html=True)
        if not df_empresas.empty:
            fig = px.pie(df_empresas, names=PORTE_EMPRESA_COL, values=EMPRESAS_QTD_COL, hole=0.5,
                         color_discrete_sequence=px.colors.sequential.Oranges_r)
            fig.update_traces(textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Não há dados de empresas para a seleção atual.")
    with col2:
        def indicador_card(label, valor):
            st.markdown(f"""
            <div style='border-radius: 8px; background-color:#f8f9fa; padding: 15px; margin-bottom: 10px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.1);'>
                <div style='font-size:14px; font-weight: bold; color:#555;'>{label}</div>
                <div style='font-size:24px; font-weight: bold; color:#007bff;'>{valor}</div>
            </div>""", unsafe_allow_html=True)
        
        ace_count = df_inst_cards[df_inst_cards[SUBCATEGORIA_INST_COL] == 'Aceleradora'].shape[0]
        cow_count = df_inst_cards[df_inst_cards[SUBCATEGORIA_INST_COL] == 'Coworking'].shape[0]
        inc_count = df_inst_cards[df_inst_cards[SUBCATEGORIA_INST_COL] == 'Incubadora'].shape[0]
        
        indicador_card("Aceleradoras", ace_count)
        indicador_card("Coworkings", cow_count)
        indicador_card("Incubadoras", inc_count)
    
    # --- EDUCAÇÃO ---
    st.markdown("<h2 style='text-align:center;'>Educação</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<h4 style='text-align:center;'>Escolas por Rede de Ensino</h4>", unsafe_allow_html=True)
        if not df_inst_ensino_rede.empty:
            fig = px.bar(df_inst_ensino_rede.sort_values(INST_ENSINO_QTD_COL, ascending=False), 
                         x=REDE_ENSINO_COL, y=INST_ENSINO_QTD_COL, color=REDE_ENSINO_COL, text_auto=True)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Não há dados de escolas por rede para a seleção atual.")
    with col2:
        st.markdown("<h4 style='text-align:center;'>IDEB Médio</h4>", unsafe_allow_html=True)
        if not df_ideb.empty:
            fig = px.bar(df_ideb, x=ETAPA_ENSINO_COL, y=IDEB_VAL_COL, color=ETAPA_ENSINO_COL, 
                         text=IDEB_VAL_COL, color_discrete_sequence=["#1f77b4", "#ff7f0e", "#2ca02c"])
            fig.update_traces(texttemplate='%{text:.2f}')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Não há dados de IDEB para a seleção atual.")
    with col3:
        st.markdown("<h4 style='text-align:center;'>Instituições por Nível</h4>", unsafe_allow_html=True)
        if not df_inst_ensino_nivel.empty:
            fig = px.bar(df_inst_ensino_nivel.sort_values(INST_ENSINO_QTD_COL, ascending=False), 
                         x=NIVEL_ENSINO_COL, y=INST_ENSINO_QTD_COL, color=NIVEL_ENSINO_COL, text_auto=True)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Não há dados de instituições por nível para a seleção atual.")
            
    # --- INSTITUIÇÕES ---
    st.markdown("<h2 style='text-align:center;'>Instituições Gerais</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center;'>Instituições por Categoria</h4>", unsafe_allow_html=True)
    if not df_instituicoes.empty:
        fig = px.bar(df_instituicoes.sort_values(INST_CATEGORIA_QTD_COL, ascending=False),
                     x=CATEGORIA_INST_COL, y=INST_CATEGORIA_QTD_COL, color=CATEGORIA_INST_COL, text_auto=True)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Não há dados de instituições para a seleção atual.")