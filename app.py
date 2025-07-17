# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import json
# Importa todas as configurações do arquivo config.py
from config import * # --- Configuração da Página do Streamlit ---
st.set_page_config(page_title="Resumo Caparaó", layout="wide")

# --- Função de Carregamento de Dados ---
# @st.cache_data garante que os dados sejam carregados apenas uma vez (lazy loading)
@st.cache_data
def load_all_data():
    """
    Carrega dados do cidades.csv e das diferentes abas do arquivo 
    base_de_dados.xlsx, tratando erros comuns.
    """
    try:
        # 1. Carrega o arquivo CSV principal
        df_cidades = pd.read_csv(CIDADES_FILE, sep=",", decimal=",")
        
        # 2. Limpa e converte as colunas de dados demográficos e financeiros
        df_cidades[HABITANTES_COL] = df_cidades[HABITANTES_COL].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float)
        df_cidades[POP_ATIVA_COL] = df_cidades[POP_ATIVA_COL].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float)
        df_cidades[POP_ESTIMADA_COL] = df_cidades[POP_ESTIMADA_COL].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float)
        df_cidades[IDH_COL] = df_cidades[IDH_COL].astype(float)
        df_cidades[POP_OCUPADA_COL] = df_cidades[POP_OCUPADA_COL].str.replace(",", ".").str.replace("%", "").astype(float)
        df_cidades[RENDA_PER_CAPITA_SM_COL] = df_cidades[RENDA_PER_CAPITA_SM_COL].astype(str).str.replace(",", ".").astype(float)
        df_cidades[PIB_PER_CAPITA_COL] = (
            df_cidades[PIB_PER_CAPITA_COL]
            .str.replace("R\$", "", regex=True)
            .str.replace(" ", "")
            .str.replace(".", "", regex=False)
            .str.replace(",", ".", regex=False)
            .astype(float)
        )

        # 3. Carrega dados das ABAS do arquivo Excel usando os nomes definidos no config.py
        data_sheets = {
            'cidades': df_cidades,
            'geo_dados': pd.read_excel(BASE_DE_DADOS_XLSX_FILE, sheet_name=SHEET_GEO),
            'empregos_setor': pd.read_excel(BASE_DE_DADOS_XLSX_FILE, sheet_name=SHEET_EMPREGOS_SETOR),
            'empregos_faixa_etaria': pd.read_excel(BASE_DE_DADOS_XLSX_FILE, sheet_name=SHEET_EMPREGOS_FAIXA),
            'empresas': pd.read_excel(BASE_DE_DADOS_XLSX_FILE, sheet_name=SHEET_EMPRESAS),
            'instituicoes_ensino': pd.read_excel(BASE_DE_DADOS_XLSX_FILE, sheet_name=SHEET_INST_ENSINO),
            'ideb': pd.read_excel(BASE_DE_DADOS_XLSX_FILE, sheet_name=SHEET_IDEB),
            'instituicoes': pd.read_excel(BASE_DE_DADOS_XLSX_FILE, sheet_name=SHEET_INSTITUICOES),
        }

        # 4. Carrega o arquivo GeoJSON para o mapa
        with open(GEOJSON_FILE, "r", encoding="utf-8") as f:
            geojson_data = json.load(f)
        data_sheets['geojson'] = geojson_data

        return data_sheets

    # 5. Tratamento de erros para ajudar a depurar problemas comuns
    except FileNotFoundError as e:
        st.error(f"ERRO: Arquivo não encontrado - {e.filename}. Verifique se todos os 3 arquivos (cidades.csv, base_de_dados.xlsx, municipios_caparao.geojson) estão na pasta principal do seu projeto no GitHub.")
        return None
    except ValueError as e:
        st.error(f"ERRO: Verifique se os nomes das abas no arquivo 'config.py' correspondem EXATAMENTE aos nomes das abas no seu arquivo 'base_de_dados.xlsx'. Detalhe: {e}")
        return None
    except Exception as e:
        st.error(f"Ocorreu um erro inesperado ao carregar os dados: {e}")
        return None

# --- Início do Layout do Aplicativo ---

# Carrega todos os dados usando a função acima
all_data = load_all_data()

# Só executa o resto do aplicativo se os dados foram carregados com sucesso
if all_data:
    
    # --- Título Principal ---
    st.markdown("<h1 style='text-align:center; color: #0dcaf0;'>Dashboard Gênesis Caparaó</h1>", unsafe_allow_html=True)

    # --- Mapa Interativo e Filtro ---
    st.markdown("<h2 style='text-align:center;'>Mapa Interativo e Filtro Municipal</h2>", unsafe_allow_html=True)

    fig_mapa = px.choropleth_mapbox(
        all_data['cidades'],
        geojson=all_data['geojson'],
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

    # Caixa de seleção para escolher um município ou a visão regional
    municipios_options = ["Visão Regional"] + sorted(all_data['cidades']["MUNICIPIO"].unique())
    municipio_escolhido = st.selectbox(
        "Selecione o município para filtrar os dados ou escolha 'Visão Regional' para ver o consolidado:",
        options=municipios_options
    )

    # --- Lógica de Filtragem dos Dados ---
    # Define se a visão é regional ou de um município específico
    is_regional_view = (municipio_escolhido == "Visão Regional")
    
    if is_regional_view:
        # Para a visão regional, os dados são agregados (somados ou calculada a média)
        df_cidades_filtrado = all_data['cidades']
        df_geo = all_data['geo_dados'].groupby(ZONA_COL, as_index=False)[PERCENTUAL_COL].mean()
        df_empregos_setor = all_data['empregos_setor'].groupby(SETOR_COL, as_index=False)[EMPREGADOS_SETOR_VAL_COL].sum()
        df_empregos_faixa = all_data['empregos_faixa_etaria'].groupby(FAIXA_ETARIA_COL, as_index=False)[EMPREGADOS_FAIXA_ETARIA_VAL_COL].sum()
        df_empresas = all_data['empresas'].groupby(PORTE_EMPRESA_COL, as_index=False)[EMPRESAS_QTD_COL].sum()
        df_inst_ensino_rede = all_data['instituicoes_ensino'].groupby(REDE_ENSINO_COL, as_index=False).size().rename(columns={'size': INST_ENSINO_QTD_COL})
        df_inst_ensino_nivel = all_data['instituicoes_ensino'].groupby(NIVEL_ENSINO_COL, as_index=False).size().rename(columns={'size': INST_ENSINO_QTD_COL})
        df_ideb = all_data['ideb'].groupby(ETAPA_ENSINO_COL, as_index=False)[IDEB_VAL_COL].mean()
        df_instituicoes = all_data['instituicoes'].groupby(CATEGORIA_INST_COL, as_index=False).size().rename(columns={'size': INST_CATEGORIA_QTD_COL})
        df_inst_cards = all_data['instituicoes']
    else:
        # Para a visão municipal, os dados são filtrados pelo nome do município
        df_cidades_filtrado = all_data['cidades'][all_data['cidades'][MUNICIPIO_COL] == municipio_escolhido]
        df_geo = all_data['geo_dados'][all_data['geo_dados'][MUNICIPIO_COL] == municipio_escolhido]
        df_empregos_setor = all_data['empregos_setor'][all_data['empregos_setor'][MUNICIPIO_COL] == municipio_escolhido]
        df_empregos_faixa = all_data['empregos_faixa_etaria'][all_data['empregos_faixa_etaria'][MUNICIPIO_COL] == municipio_escolhido]
        df_empresas = all_data['empresas'][all_data['empresas'][MUNICIPIO_COL] == municipio_escolhido]
        df_inst_ensino_rede = all_data['instituicoes_ensino'][all_data['instituicoes_ensino'][MUNICIPIO_COL] == municipio_escolhido].groupby(REDE_ENSINO_COL, as_index=False).size().rename(columns={'size': INST_ENSINO_QTD_COL})
        df_inst_ensino_nivel = all_data['instituicoes_ensino'][all_data['instituicoes_ensino'][MUNICIPIO_COL] == municipio_escolhido].groupby(NIVEL_ENSINO_COL, as_index=False).size().rename(columns={'size': INST_ENSINO_QTD_COL})
        df_ideb = all_data['ideb'][all_data['ideb'][MUNICIPIO_COL] == municipio_escolhido]
        df_instituicoes = all_data['instituicoes'][all_data['instituicoes'][MUNICIPIO_COL] == municipio_escolhido].groupby(CATEGORIA_INST_COL, as_index=False).size().rename(columns={'size': INST_CATEGORIA_QTD_COL})
        df_inst_cards = all_data['instituicoes'][all_data['instituicoes'][MUNICIPIO_COL] == municipio_escolhido]

    st.markdown("<hr style='margin-top:2em; margin-bottom:2em;'>", unsafe_allow_html=True)
    
    # --- Título Dinâmico da Seção ---
    view_title = "Resumo da Região do Caparaó" if is_regional_view else f"Resumo de {municipio_escolhido}"
    st.markdown(f"<h2 style='text-align:center;'>{view_title}</h2>", unsafe_allow_html=True)

    # --- Seção: KPIs (Indicadores Chave) ---
    if not df_cidades_filtrado.empty:
        # Cálculos dos KPIs com base nos dados filtrados
        idh_medio = df_cidades_filtrado[IDH_COL].mean()
        pib_per_capita = df_cidades_filtrado[PIB_PER_CAPITA_COL].mean()
        pop_estimada = df_cidades_filtrado[POP_ESTIMADA_COL].sum()
        habitantes = df_cidades_filtrado[HABITANTES_COL].sum()
        pop_idade_ativa = df_cidades_filtrado[POP_ATIVA_COL].sum()
        perc_pop_ocupada = df_cidades_filtrado[POP_OCUPADA_COL].mean()
        renda_per_capita_sm = df_cidades_filtrado[RENDA_PER_CAPITA_SM_COL].mean()
        perc_pop_ativa = (pop_idade_ativa / habitantes) * 100 if habitantes > 0 else 0

        # Função para criar os cartões de KPI
        def kpi_card(title, value, emoji, color="#000"):
            st.markdown(f"""
            <div style='border-radius: 10px; margin: 1em; padding: 15px; background-color: #f8f9fa; text-align: center;
                         box-shadow: 0 2px 4px rgba(0,0,0,0.1); height: 100%;'>
                <div style='font-size: 24px'>{emoji}</div>
                <div style='font-size: 13px; color: grey'>{title}</div>
                <div style='font-size: 20px; font-weight: bold; color:{color}'>{value}</div>
            </div>""", unsafe_allow_html=True)

        # Exibição dos KPIs em duas linhas
        cols_kpi1 = st.columns(4)
        with cols_kpi1[0]: kpi_card("IDH MÉDIO", f"{idh_medio:.3f}", "📈", "#FFA500")
        with cols_kpi1[1]: kpi_card("PIB PER CAPITA", f"R$ {pib_per_capita:,.2f}", "💰", "#28a745")
        with cols_kpi1[2]: kpi_card("POP. ESTIMADA 2024", f"{pop_estimada:,.0f}", "👥", "#007bff")
        with cols_kpi1[3]: kpi_card("HABITANTES (CENSO)", f"{habitantes:,.0f}", "🏡", "#6f42c1")
        
        cols_kpi2 = st.columns(4)
        with cols_kpi2[0]: kpi_card("POP. IDADE ATIVA", f"{pop_idade_ativa:,.0f}", "💪", "#dc3545")
        with cols_kpi2[1]: kpi_card("% POP. ATIVA", f"{perc_pop_ativa:.1f}%", "🧠", "#6c757d")
        with cols_kpi2[2]: kpi_card("% POP. OCUPADA", f"{perc_pop_ocupada:.1f}%", "👷", "#ffc107")
        with cols_kpi2[3]: kpi_card("RENDA PER CAPITA (SM)", f"{renda_per_capita_sm:.2f}", "💵", "#20c997")

    st.markdown("<hr style='margin-top:2em; margin-bottom:2em;'>", unsafe_allow_html=True)
    
    # --- Seção: Gráficos ---

    # Gráfico de Concentração Geográfica
    if not df_geo.empty:
        st.markdown("<h3 style='text-align:center;'>Concentração Geográfica</h3>", unsafe_allow_html=True)
        zona_urbana_df = df_geo[df_geo[ZONA_COL] == 'Urbana']
        zona_rural_df = df_geo[df_geo[ZONA_COL] == 'Rural']
        zona_urbana = zona_urbana_df[PERCENTUAL_COL].values[0] if not zona_urbana_df.empty else 0
        zona_rural = zona_rural_df[PERCENTUAL_COL].values[0] if not zona_rural_df.empty else 0

        geo_df_pie = pd.DataFrame({'Zona': ['Urbana', 'Rural'], 'Valor': [zona_urbana, zona_rural]})
        fig_geo = px.pie(geo_df_pie, names='Zona', values='Valor', hole=0.5, color_discrete_sequence=['#1f77b4', '#2ca02c'])
        fig_geo.update_traces(textinfo='none', hoverinfo='label+percent')
        fig_geo.update_layout(showlegend=False, margin=dict(t=20, b=20))
        
        c1, c2, c3 = st.columns([1, 1.5, 1])
        with c2:
            st.plotly_chart(fig_geo, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1: st.markdown(f'<div style="text-align: center;">🏙️ <b>ZONA URBANA</b><h3 style="color:#1f77b4;">{zona_urbana:.2f}%</h3></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div style="text-align: center;">🏡 <b>ZONA RURAL</b><h3 style="color:#2ca02c;">{zona_rural:.2f}%</h3></div>', unsafe_allow_html=True)
        st.markdown("<hr style='margin-top:2em; margin-bottom:2em;'>", unsafe_allow_html=True)

    # Gráficos de Economia
    st.markdown("<h2 style='text-align:center;'>Economia e Mercado de Trabalho</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h4 style='text-align:center;'>Empregos por Setor</h4>", unsafe_allow_html=True)
        if not df_empregos_setor.empty:
            fig = px.bar(df_empregos_setor.sort_values(EMPREGADOS_SETOR_VAL_COL, ascending=False), x=SETOR_COL, y=EMPREGADOS_SETOR_VAL_COL, color=SETOR_COL, text_auto='.2s')
            fig.update_layout(showlegend=False, yaxis_title="Total de Empregados", xaxis_title=None)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Não há dados de empregos por setor para a seleção atual.")
    with col2:
        st.markdown("<h4 style='text-align:center;'>Empregos por Faixa Etária</h4>", unsafe_allow_html=True)
        if not df_empregos_faixa.empty:
            # Garante a ordem correta das faixas etárias no eixo X
            faixa_etaria_ordem = ["15-17", "18-24", "25-29", "30-39", "40-49", "50-64", "65-mais"]
            fig = px.bar(df_empregos_faixa, x=FAIXA_ETARIA_COL, y=EMPREGADOS_FAIXA_ETARIA_VAL_COL, color=FAIXA_ETARIA_COL, text_auto='.2s')
            fig.update_layout(showlegend=False, yaxis_title="Total de Empregados", xaxis_title="Faixa Etária", xaxis={'categoryorder':'array', 'categoryarray':faixa_etaria_ordem})
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Não há dados de empregos por faixa etária para a seleção atual.")

    # Gráficos de Empreendedorismo
    st.markdown("<h2 style='text-align:center;'>Empresas e Empreendedorismo</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h4 style='text-align:center;'>Empresas por Porte</h4>", unsafe_allow_html=True)
        if not df_empresas.empty:
            fig = px.pie(df_empresas, names=PORTE_EMPRESA_COL, values=EMPRESAS_QTD_COL, hole=0.5, color_discrete_sequence=px.colors.sequential.Oranges_r)
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
        
        # Contagem de instituições específicas com base nos dados filtrados
        ace_count = df_inst_cards[df_inst_cards[SUBCATEGORIA_INST_COL] == 'Aceleradora'].shape[0]
        cow_count = df_inst_cards[df_inst_cards[SUBCATEGORIA_INST_COL] == 'Coworking'].shape[0]
        inc_count = df_inst_cards[df_inst_cards[SUBCATEGORIA_INST_COL] == 'Incubadora'].shape[0]
        
        indicador_card("Aceleradoras", ace_count)
        indicador_card("Coworkings", cow_count)
        indicador_card("Incubadoras", inc_count)
    
    # Gráficos de Educação
    st.markdown("<h2 style='text-align:center;'>Educação</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<h4 style='text-align:center;'>Escolas por Rede de Ensino</h4>", unsafe_allow_html=True)
        if not df_inst_ensino_rede.empty:
            fig = px.bar(df_inst_ensino_rede.sort_values(INST_ENSINO_QTD_COL, ascending=False), x=REDE_ENSINO_COL, y=INST_ENSINO_QTD_COL, color=REDE_ENSINO_COL, text_auto=True)
            fig.update_layout(showlegend=False, yaxis_title="Nº de Escolas", xaxis_title=None)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Não há dados de escolas por rede para a seleção atual.")
    with col2:
        st.markdown("<h4 style='text-align:center;'>IDEB Médio</h4>", unsafe_allow_html=True)
        if not df_ideb.empty:
            fig = px.bar(df_ideb, x=ETAPA_ENSINO_COL, y=IDEB_VAL_COL, color=ETAPA_ENSINO_COL, text=IDEB_VAL_COL, color_discrete_sequence=["#1f77b4", "#ff7f0e", "#2ca02c"])
            fig.update_traces(texttemplate='%{text:.2f}')
            fig.update_layout(showlegend=False, yaxis_title="Nota IDEB", xaxis_title=None)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Não há dados de IDEB para a seleção atual.")
    with col3:
        st.markdown("<h4 style='text-align:center;'>Instituições por Nível</h4>", unsafe_allow_html=True)
        if not df_inst_ensino_nivel.empty:
            fig = px.bar(df_inst_ensino_nivel.sort_values(INST_ENSINO_QTD_COL, ascending=False), x=NIVEL_ENSINO_COL, y=INST_ENSINO_QTD_COL, color=NIVEL_ENSINO_COL, text_auto=True)
            fig.update_layout(showlegend=False, yaxis_title="Nº de Instituições", xaxis_title=None)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Não há dados de instituições por nível para a seleção atual.")
            
    # Gráfico de Instituições Gerais
    st.markdown("<h2 style='text-align:center;'>Instituições Gerais</h2>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align:center;'>Instituições por Categoria</h4>", unsafe_allow_html=True)
    if not df_instituicoes.empty:
        fig = px.bar(df_instituicoes.sort_values(INST_CATEGORIA_QTD_COL, ascending=False), x=CATEGORIA_INST_COL, y=INST_CATEGORIA_QTD_COL, color=CATEGORIA_INST_COL, text_auto=True)
        fig.update_layout(showlegend=False, yaxis_title="Nº de Instituições", xaxis_title=None)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Não há dados de instituições para a seleção atual.")