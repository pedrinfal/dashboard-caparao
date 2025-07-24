import streamlit as st
import pandas as pd
import plotly.express as px
import json
from pathlib import Path
import unicodedata

# =============================================================================
# CONFIGURAÇÕES GERAIS
# =============================================================================
st.set_page_config(page_title="Resumo Caparaó", layout="wide")

# Caminhos --------------------------------------------------------------------
DATA_XLSX = Path("base_de_dados.xlsx")          # planilha com dados reais
CIDADES_GEOJSON = Path("municipios_caparao.geojson")  # arquivo geojson local (opcional)

# =============================================================================
# FUNÇÕES DE APOIO
# =============================================================================
def load_sheet(sheet_name: str) -> pd.DataFrame:
    """Lê uma aba da planilha, remove colunas totalmente vazias (Unnamed),
    tira espaços extras dos nomes e renomeia a coluna 'Cidade*' para 'MUNICIPIO'.
    Não altera os demais nomes de colunas (mantemos para compatibilidade com o layout).
    """
    df = pd.read_excel(DATA_XLSX, sheet_name=sheet_name)
    # descarta colunas Unnamed
    df = df.loc[:, ~df.columns.astype(str).str.contains(r'^Unnamed', case=False, na=False)]
    # tira espaços extras no nome das colunas
    df.columns = df.columns.astype(str).str.strip()
    # renomeia Cidade -> MUNICIPIO (independente de acento/maiúscula)
    for col in df.columns:
        if col.strip().lower().startswith("cidade"):
            df = df.rename(columns={col: "MUNICIPIO"})
            break
    return df

def strip_accents(text: str) -> str:
    return ''.join(c for c in unicodedata.normalize('NFKD', str(text)) if not unicodedata.combining(c))

# =============================================================================
# LEITURA DE TODAS AS ABAS
# =============================================================================
df_demo              = load_sheet("Dados demográficos")
df_geo_sheet         = load_sheet("Dados geográficos")
df_emp_setor_sheet   = load_sheet("Empregados por setor")
df_emp_faixa_sheet   = load_sheet("Empregados por faixa etária")
df_empresas_seg_sheet= load_sheet("Empresas por segmento")
df_inst_ens_sheet    = load_sheet("Instituições de ensino")
df_ideb_sheet        = load_sheet("Índices educacionais (IDEB)")
df_instituicoes_sheet= load_sheet("Instituições")

# =============================================================================
# TRATAMENTO / LIMPEZA DOS DADOS DEMOGRÁFICOS PRINCIPAIS
# =============================================================================
df = df_demo.copy()

# Conversões numéricas defensivas ------------------------------------------------
df["HABITANTES (IJSN/2022)"] = (
    df["HABITANTES (IJSN/2022)"].astype(str)
    .str.replace(".", "", regex=False)
    .str.replace(",", ".", regex=False)
    .astype(float)
)
df["POPUL. COM IDADE ATIVA (IJSN/2022)"] = (
    df["POPUL. COM IDADE ATIVA (IJSN/2022)"].astype(str)
    .str.replace(".", "", regex=False)
    .str.replace(",", ".", regex=False)
    .astype(float)
)
df["POPUL. ESTIMADA (IBGE/2024)"] = (
    df["POPUL. ESTIMADA (IBGE/2024)"].astype(str)
    .str.replace(".", "", regex=False)
    .str.replace(",", ".", regex=False)
    .astype(float)
)
df["IDH (IBGE/2010)"] = pd.to_numeric(df["IDH (IBGE/2010)"], errors="coerce")

# Índice de população ocupada já está em proporção (0-1) na planilha.
# Mantemos como float e mais tarde multiplicamos por 100 ao exibir.
df["ÍNDICE DE POPUL. OCUPADA (IBGE/2022)"] = pd.to_numeric(
    df["ÍNDICE DE POPUL. OCUPADA (IBGE/2022)"], errors="coerce"
)

df["MÉDIA DE RENDA PER CAPITA EM Nº DE SALÁRIOS MÍNIMOS (IBGE/2022)"] = (
    df["MÉDIA DE RENDA PER CAPITA EM Nº DE SALÁRIOS MÍNIMOS (IBGE/2022)"].astype(str)
    .str.replace(",", ".", regex=False)
    .astype(float)
)
df["PIB / RENDA PER CAPITA (IBGE/2021)"] = (
    df["PIB / RENDA PER CAPITA (IBGE/2021)"].astype(str)
    .str.replace("R$", "", regex=False)
    .str.replace(" ", "", regex=False)
    .str.replace(".", "", regex=False)   # remove milhar
    .str.replace(",", ".", regex=False)  # decimal
    .astype(float)
)

# =============================================================================
# CÁLCULOS REGIONAIS (AGREGADOS)
# =============================================================================
# Área urbana/rural: valores na planilha estão em proporção (0-1). Convertendo p/ %.
zona_rural  = df_geo_sheet["ÁREA RURAL"].mean()  * 100.0
zona_urbana = df_geo_sheet["ÁREA URBANA"].mean() * 100.0

idh_medio          = df["IDH (IBGE/2010)"].mean()
pib_per_capita     = df["PIB / RENDA PER CAPITA (IBGE/2021)"].mean()
pop_estimada       = df["POPUL. ESTIMADA (IBGE/2024)"].sum()
habitantes         = df["HABITANTES (IJSN/2022)"].sum()
pop_idade_ativa    = df["POPUL. COM IDADE ATIVA (IJSN/2022)"].sum()
perc_pop_ocupada   = df["ÍNDICE DE POPUL. OCUPADA (IBGE/2022)"].mean() * 100.0
renda_per_capita_sm= df["MÉDIA DE RENDA PER CAPITA EM Nº DE SALÁRIOS MÍNIMOS (IBGE/2022)"].mean()
perc_pop_ativa     = (pop_idade_ativa / habitantes) * 100.0 if habitantes else 0.0

# =============================================================================
# LAYOUT: TÍTULOS
# =============================================================================
st.markdown("<h1 style='text-align:center; color: ##0dcaf0;'>Dashboard Gênesis Caparaó</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center;'>Resumo da Região do Caparaó</h2>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# GRÁFICO DONUT - CONCENTRAÇÃO GEOGRÁFICA (URBANA x RURAL)
# -----------------------------------------------------------------------------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<h3 style='text-align:center;'>Concentração Geográfica</h3>", unsafe_allow_html=True)
    geo_df = pd.DataFrame({"Zona": ["Urbana", "Rural"], "Valor": [zona_urbana, zona_rural]})
    fig_geo = px.pie(geo_df, names='Zona', values='Valor', hole=0.5,
                     color_discrete_sequence=['#1f77b4', '#2ca02c'])
    fig_geo.update_traces(textinfo='none')
    fig_geo.update_layout(showlegend=False, margin=dict(t=20, b=20))
    st.plotly_chart(fig_geo, use_container_width=True)

colu1, colu2 = st.columns(2)
with colu1:
    st.markdown(f"""
    <div style="display: flex; flex-direction: column; align-items: flex-start;">
        <div style="font-size: 16px;">🏙️ <b>ZONA URBANA</b></div>
        <h3 style="color:#1f77b4; margin: 0;">{zona_urbana:.2f}%</h3>
    </div>
    """, unsafe_allow_html=True)

with colu2:
    st.markdown(f"""
    <div style="display: flex; flex-direction: column; align-items: flex-end;">
        <div style="font-size: 16px;">🏡 <b>ZONA RURAL</b></div>
        <h3 style="color:#2ca02c; margin: 0 0 0 1em;">{zona_rural:.2f}%</h3>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='margin-top:2em; margin-bottom:2em;'>", unsafe_allow_html=True)

# =============================================================================
# FUNÇÃO PARA CRIAR CARDS DE KPI
# =============================================================================
def kpi_card(title, value, emoji, color="#000"):
    st.markdown(
        f"""
        <div style='border-radius: 10px; margin: 1em; padding: 15px; background-color: #f8f9fa; text-align: center;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);'>
            <div style='font-size: 24px'>{emoji}</div>
            <div style='font-size: 13px; color: grey'>{title}</div>
            <div style='font-size: 20px; font-weight: bold; color:{color}'>{value}</div>
        </div>
        """, unsafe_allow_html=True
    )

# -----------------------------------------------------------------------------
# LINHA 1 KPIs
# -----------------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    kpi_card("IDH MÉDIO", f"{idh_medio:.3f}", "📈", "#FFA500")
with col2:
    kpi_card("PIB PER CAPITA", f"R$ {pib_per_capita:,.2f}", "💰", "#28a745")
with col3:
    kpi_card("POP. ESTIMADA 2024", f"{pop_estimada:,.0f}", "👥", "#007bff")
with col4:
    kpi_card("HABITANTES (CENSO)", f"{habitantes:,.0f}", "🏡", "#6f42c1")

# -----------------------------------------------------------------------------
# LINHA 2 KPIs
# -----------------------------------------------------------------------------
col1, col2, col3, col4 = st.columns(4)
with col1:
    kpi_card("POP. IDADE ATIVA", f"{pop_idade_ativa:,.0f}", "💪", "#dc3545")
with col2:
    kpi_card("% POP. ATIVA", f"{perc_pop_ativa:.1f}%", "🧠", "#6c757d")
with col3:
    kpi_card("% POP. OCUPADA", f"{perc_pop_ocupada:.1f}%", "👷", "#ffc107")
with col4:
    kpi_card("RENDA PER CAPITA (SM)", f"{renda_per_capita_sm:.2f}", "💵", "#20c997")

st.markdown("</div>", unsafe_allow_html=True)

# =============================================================================
# ECONOMIA E MERCADO DE TRABALHO REGIONAL
# =============================================================================
st.markdown("<h2 style='text-align:center;'>Economia e Mercado de Trabalho Regional</h2>", unsafe_allow_html=True)

# --- Empregos por Setor (REGIÃO) --------------------------------------------
emp_setor_tot = {
    "Agricultura":          df_emp_setor_sheet["AGRICULTURA"].sum(skipna=True),
    "Industria":            df_emp_setor_sheet["INDÚSTRIA"].sum(skipna=True),
    "Comercio":             df_emp_setor_sheet["COMÉRCIO"].sum(skipna=True),
    "AdministracaoPublica": df_emp_setor_sheet["ADMINISTRAÇÃO PÚBLICA"].sum(skipna=True),
    "Servicos":             df_emp_setor_sheet["SERVIÇOS"].sum(skipna=True),
}
empregos_setor = pd.DataFrame({"Setor": list(emp_setor_tot.keys()), "Total Empregados": list(emp_setor_tot.values())})

# --- Empregos por Faixa Etária (REGIÃO) --------------------------------------
emp_faixa_tot = {
    "15-17":   df_emp_faixa_sheet["15 A 17 ANOS"].fillna(0).sum(),
    "18-24":   df_emp_faixa_sheet["18 A 24 ANOS"].fillna(0).sum(),
    "25-29":   df_emp_faixa_sheet["25 A 29 ANOS"].fillna(0).sum(),
    "30-39":   df_emp_faixa_sheet["30 A 39 ANOS"].fillna(0).sum(),
    "40-49":   df_emp_faixa_sheet["40 A 49 ANOS"].fillna(0).sum(),
    "50-64":   df_emp_faixa_sheet["50 A 64 ANOS"].fillna(0).sum(),
    "65-mais": df_emp_faixa_sheet["65 OU MAIS"].fillna(0).sum(),
}
empregos_faixa_etaria = pd.DataFrame({"Faixa Etária": list(emp_faixa_tot.keys()), "Total Empregados": list(emp_faixa_tot.values())})

col1, col2 = st.columns(2)
with col1:
    st.markdown("<h4 style='text-align:center;'>Empregos por Setor</h4>", unsafe_allow_html=True)
    fig_setor = px.bar(empregos_setor, x="Setor", y="Total Empregados",
                       color="Setor", text="Total Empregados",
                       color_discrete_sequence=px.colors.qualitative.Plotly)
    fig_setor.update_traces(textposition="outside")
    fig_setor.update_layout(xaxis_title="Setor", yaxis_title="Total Empregados",
                            showlegend=False, margin=dict(t=30, b=30))
    st.plotly_chart(fig_setor, use_container_width=True)

with col2:
    st.markdown("<h4 style='text-align:center;'>Empregos por Faixa Etária</h4>", unsafe_allow_html=True)
    fig_faixa = px.bar(empregos_faixa_etaria, x="Faixa Etária", y="Total Empregados",
                       color="Faixa Etária", text="Total Empregados",
                       color_discrete_sequence=px.colors.qualitative.Pastel)
    fig_faixa.update_traces(textposition="outside")
    fig_faixa.update_layout(xaxis_title="Faixa Etária", yaxis_title="Total Empregados",
                            showlegend=False, margin=dict(t=30, b=30))
    st.plotly_chart(fig_faixa, use_container_width=True)

# =============================================================================
# EMPRESAS E EMPREENDEDORISMO REGIONAL
# =============================================================================
st.markdown("<h2 style='text-align:center;'>Empresas e Empreendedorismo Regional</h2>", unsafe_allow_html=True)

# A aba 'Empresas por segmento' traz proporções (0-1) por município; usamos média.
empresas_mean = df_empresas_seg_sheet[["ME", "MEI", "OUTRAS", "EPP"]].mean()
empresas_tipo = pd.DataFrame({"Tipo": empresas_mean.index, "Quantidade": empresas_mean.values})

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("<h4 style='text-align:center; padding: 0em 2em 0em 0em; margin: 0em 2em 0em 0em;'>Empresas por Tipo</h4>", unsafe_allow_html=True)
    fig_empresas = px.pie(empresas_tipo, names='Tipo', values='Quantidade', hole=0.5,
                          color_discrete_sequence=['#fdae6b', '#fdd0a2', '#d9d0ec', '#80cdc1'])
    fig_empresas.update_traces(textinfo='percent+label')
    fig_empresas.update_layout(margin=dict(t=20, b=20))
    st.plotly_chart(fig_empresas, use_container_width=True)

with col2:
    # Mantidos valores fixos (não estão na planilha) conforme pedido original
    def indicador_card(label, valor):
        st.markdown(f"""
        <div style='border-radius: 8px; background-color:#f8f9fa; padding: 15px; margin-bottom: 10px;
                    text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.1);'>
            <div style='font-size:14px; font-weight: bold; color:#555;'>{label}</div>
            <div style='font-size:24px; font-weight: bold; color:#007bff;'>{valor}</div>
        </div>
        """, unsafe_allow_html=True)
    indicador_card("Aceleradora de Empresas", 1)
    indicador_card("Coworking", 2)
    indicador_card("Incubadora de Empresas", 4)

# =============================================================================
# EDUCAÇÃO REGIONAL
# =============================================================================
st.markdown("<h2 style='text-align:center;'>Educação Regional</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

# Escolas por Rede (soma região)
escolas_soma = df_inst_ens_sheet[["MUNICIPAIS", "ESTADUAIS", "PARTICULAR", "FEDERAL"]].fillna(0).sum()
escolas_rede = pd.DataFrame({
    "Rede de Ensino": ["Municipais", "Estaduais", "Particulares", "Federais"],
    "Número de Escolas": [int(escolas_soma["MUNICIPAIS"]),
                           int(escolas_soma["ESTADUAIS"]),
                           int(escolas_soma["PARTICULAR"]),
                           int(escolas_soma["FEDERAL"])]
})

# IDEB Médio (média simples)
ideb_mean = df_ideb_sheet[["ANOS INICIAS", "ANOS FINAIS", "MÉDIO"]].mean()
ideb_medio = pd.DataFrame({
    "Etapa de Ensino": ["Anos Iniciais", "Anos Finais", "Ensino Médio"],
    "IDEB": [
        round(ideb_mean["ANOS INICIAS"], 2),
        round(ideb_mean["ANOS FINAIS"], 2),
        round(ideb_mean["MÉDIO"], 2)
    ]
})


# Instituições de Ensino por Nível (a partir da aba Instituições / Subcategoria)
level_map = {
    "SUPERIOR": "Superior",
    "TÉCNICA": "Tecnico",
    "TECNICA": "Tecnico",
    "INFANTIL": "Infantil",
    "FUNDAMENTAL": "Fundamental",
    "MÉDIO": "Medio",
    "MEDIO": "Medio",
}
_inst_levels = df_instituicoes_sheet[["MUNICIPIO", "Subcategoria"]].copy()
_inst_levels["Subcategoria"] = _inst_levels["Subcategoria"].astype(str).str.strip().str.upper()
_inst_levels["NivelNorm"] = _inst_levels["Subcategoria"].map(level_map)
inst_level_counts = _inst_levels.dropna(subset=["NivelNorm"]).groupby("NivelNorm").size()
_levels_order = ["Fundamental", "Infantil", "Medio", "Superior", "Tecnica"]
inst_level_counts = inst_level_counts.reindex(_levels_order).fillna(0).astype(int)
instituicoes_nivel = pd.DataFrame({
    "Nível de Ensino": inst_level_counts.index,
    "Nº de Instituições": inst_level_counts.values
})

with col1:
    st.markdown("<h4 style='text-align:center;'>Escolas por Rede de Ensino</h4>", unsafe_allow_html=True)
    fig_rede = px.bar(escolas_rede, x="Rede de Ensino", y="Número de Escolas",
                      color="Rede de Ensino", text="Número de Escolas",
                      color_discrete_sequence=px.colors.qualitative.Set1)
    fig_rede.update_traces(textposition="outside")
    fig_rede.update_layout(xaxis_title="Rede de Ensino", yaxis_title="Número de Escolas",
                           showlegend=False, margin=dict(t=20, b=20))
    st.plotly_chart(fig_rede, use_container_width=True)

with col2:
    st.markdown("<h4 style='text-align:center;'>IDEB Médio</h4>", unsafe_allow_html=True)
    fig_ideb = px.bar(ideb_medio, x="Etapa de Ensino", y="IDEB",
                      color="Etapa de Ensino", text="IDEB",
                      color_discrete_sequence=["#1f77b4", "#ff7f0e", "#2ca02c"])
    fig_ideb.update_traces(textposition="outside")
    fig_ideb.update_layout(xaxis_title="Etapa de Ensino", yaxis_title="IDEB",
                           showlegend=False, margin=dict(t=20, b=20))
    st.plotly_chart(fig_ideb, use_container_width=True)

with col3:
    st.markdown("<h4 style='text-align:center;'>Instituições de Ensino por Nível</h4>", unsafe_allow_html=True)
    fig_inst = px.bar(instituicoes_nivel, x="Nível de Ensino", y="Nº de Instituições",
                      color="Nível de Ensino", text="Nº de Instituições",
                      color_discrete_sequence=px.colors.qualitative.Set2)
    fig_inst.update_traces(textposition="outside")
    fig_inst.update_layout(xaxis_title="Nível de Ensino", yaxis_title="Nº de Instituições",
                           showlegend=False, margin=dict(t=20, b=20))
    st.plotly_chart(fig_inst, use_container_width=True)

# =============================================================================
# INSTITUIÇÕES REGIONAIS
# =============================================================================
st.markdown("<h2 style='text-align:center; color: ##0dcaf0;'>INSTITUIÇÕES REGIONAIS</h2>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center;'>Instituições por Categoria</h4>", unsafe_allow_html=True)

_inst = df_instituicoes_sheet.copy()
_inst["CategoriaNorm"] = _inst["Categoria"].map(strip_accents).str.upper().str.strip()
_cat_order = ["ASSOCIACAO", "ECONOMIA", "EDUCACAO", "EMPREENDEDORISMO", "FOMENTO", "GOVERNO", "SINDICATO"]
cat_counts = _inst.groupby("CategoriaNorm").size()
cat_counts = cat_counts.reindex(_cat_order).fillna(0).astype(int)
instituicoes_categoria = pd.DataFrame({
    "Categoria": cat_counts.index,
    "Nº de Instituições": cat_counts.values
})
fig_inst_cat = px.bar(instituicoes_categoria, x="Categoria", y="Nº de Instituições",
                      color="Categoria", text="Nº de Instituições",
                      color_discrete_sequence=["#4c78a8", "#f58518", "#00cc96", "#ab63fa", "#ffa15a", "#19d3f3", "#ff6692"])
fig_inst_cat.update_traces(textposition="outside")
fig_inst_cat.update_layout(
    xaxis_title="Categoria",
    yaxis_title="Nº de Instituições",
    showlegend=False,
    margin=dict(t=20, b=20)
)
st.plotly_chart(fig_inst_cat, use_container_width=True)

# =============================================================================
# MAPA INTERATIVO
# =============================================================================

st.markdown("<h2 style='text-align:center;'>Mapa Interativo dos Municípios</h2>", unsafe_allow_html=True)
if CIDADES_GEOJSON.exists():
    with open(CIDADES_GEOJSON, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)
else:
    geojson_data = None

if geojson_data is not None:
    fig_mapa = px.choropleth_mapbox(
        df,
        geojson=geojson_data,
        locations="MUNICIPIO",
        featureidkey="properties.NM_MUN",
        color="IDH (IBGE/2010)",
        color_continuous_scale="Viridis",
        mapbox_style="carto-positron",
        center={"lat": -20.7, "lon": -41.8},
        zoom=8,
        opacity=0.5,
        hover_data={"MUNICIPIO": True, "IDH (IBGE/2010)": True, "PIB / RENDA PER CAPITA (IBGE/2021)": True}
    )
    fig_mapa.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig_mapa, use_container_width=True)
else:
    st.info("Arquivo GeoJSON não encontrado. Mapa omitido.")

# =============================================================================
# FILTRO POR MUNICÍPIO (DETALHES)
# =============================================================================

municipio_escolhido = st.selectbox(
    "Selecione o município para filtrar os dados:",
    options=df["MUNICIPIO"].unique()
)
df_filtrado = df[df["MUNICIPIO"] == municipio_escolhido]

if not df_filtrado.empty:
    habitantes_mun = float(df_filtrado["HABITANTES (IJSN/2022)"].iloc[0])

    # ------------------------------------------------------------------
    # EMPREGOS (municipal)
    # ------------------------------------------------------------------

    st.markdown("<h2 style='text-align:center;'>Economia e Mercado de Trabalho do Município</h2>", unsafe_allow_html=True)
    row_setor = df_emp_setor_sheet[df_emp_setor_sheet["MUNICIPIO"] == municipio_escolhido]
    if not row_setor.empty:
        r = row_setor.fillna(0).iloc[0]
        empregos_setor_mun = pd.DataFrame({
            "Setor": ["Agricultura", "Indústria", "Comércio", "Administração Pública", "Serviços"],
            "Total Empregados": [r.get("AGRICULTURA",0), r.get("INDÚSTRIA",0), r.get("COMÉRCIO",0),
                                  r.get("ADMINISTRAÇÃO PÚBLICA",0), r.get("SERVIÇOS",0)]
        })
    else:
        empregos_setor_mun = pd.DataFrame({"Setor":[],"Total Empregados":[]})

    row_faixa = df_emp_faixa_sheet[df_emp_faixa_sheet["MUNICIPIO"] == municipio_escolhido]
    if not row_faixa.empty:
        r = row_faixa.fillna(0).iloc[0]
        empregos_faixa_mun = pd.DataFrame({
            "Faixa Etária": ["15-17", "18-24", "25-29", "30-39", "40-49", "50-64", "65-mais"],
            "Total Empregados": [r.get("15 A 17 ANOS",0), r.get("18 A 24 ANOS",0), r.get("25 A 29 ANOS",0),
                                  r.get("30 A 39 ANOS",0), r.get("40 A 49 ANOS",0), r.get("50 A 64 ANOS",0),
                                  r.get("65 OU MAIS",0)]
        })
    else:
        empregos_faixa_mun = pd.DataFrame({"Faixa Etária":[], "Total Empregados":[]})

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h4 style='text-align:center;'>Empregos por Setor</h4>", unsafe_allow_html=True)
        fig_setor_m = px.bar(empregos_setor_mun, x="Setor", y="Total Empregados",
                             color="Setor", text="Total Empregados")
        fig_setor_m.update_traces(textposition="outside")
        st.plotly_chart(fig_setor_m, use_container_width=True)
    with col2:
        st.markdown("<h4 style='text-align:center;'>Empregos por Faixa Etária</h4>", unsafe_allow_html=True)
        fig_faixa_m = px.bar(empregos_faixa_mun, x="Faixa Etária", y="Total Empregados",
                             color="Faixa Etária", text="Total Empregados")
        fig_faixa_m.update_traces(textposition="outside")
        st.plotly_chart(fig_faixa_m, use_container_width=True)

    # ------------------------------------------------------------------
    # EMPRESAS (municipal)
    # ------------------------------------------------------------------
    st.markdown("<h2 style='text-align:center;'>Empresas e Empreendedorismo do Município</h2>", unsafe_allow_html=True)
    row_emp = df_empresas_seg_sheet[df_empresas_seg_sheet["MUNICIPIO"] == municipio_escolhido]
    if not row_emp.empty:
        r = row_emp.fillna(0).iloc[0]
        empresas_tipo_mun = pd.DataFrame({
            "Tipo": ["ME", "MEI", "Outras", "EPP"],
            "Quantidade": [r.get("ME",0), r.get("MEI",0), r.get("OUTRAS",0), r.get("EPP",0)]
        })
    else:
        empresas_tipo_mun = pd.DataFrame({"Tipo":[], "Quantidade":[]})
    fig_empresas_m = px.pie(empresas_tipo_mun, names='Tipo', values='Quantidade', hole=0.5)
    fig_empresas_m.update_traces(textinfo='percent+label')
    st.plotly_chart(fig_empresas_m, use_container_width=True)

    # ------------------------------------------------------------------
    # EDUCAÇÃO (municipal)
    # ------------------------------------------------------------------
    st.markdown("<h2 style='text-align:center;'>Educação do Município</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    row_escola = df_inst_ens_sheet[df_inst_ens_sheet["MUNICIPIO"] == municipio_escolhido]
    if not row_escola.empty:
        r = row_escola.fillna(0).iloc[0]
        escolas_rede_mun = pd.DataFrame({
            "Rede de Ensino": ["Municipais", "Estaduais", "Particulares", "Federais"],
            "Número de Escolas": [int(r.get("MUNICIPAIS",0)), int(r.get("ESTADUAIS",0)), int(r.get("PARTICULAR",0)), int(r.get("FEDERAL",0))]
        })
    else:
        escolas_rede_mun = pd.DataFrame({"Rede de Ensino":[],"Número de Escolas":[]})
    with col1:
        fig_escolas_m = px.bar(escolas_rede_mun, x="Rede de Ensino", y="Número de Escolas",
                               color="Rede de Ensino", text="Número de Escolas")
        fig_escolas_m.update_traces(textposition="outside")
        st.plotly_chart(fig_escolas_m, use_container_width=True)

    row_ideb = df_ideb_sheet[df_ideb_sheet["MUNICIPIO"] == municipio_escolhido]
    if not row_ideb.empty:
        r = row_ideb.fillna(0).iloc[0]
        ideb_mun = pd.DataFrame({
            "Etapa de Ensino": ["Anos Iniciais", "Anos Finais", "Ensino Médio"],
            "IDEB": [r.get("ANOS INICIAS", None), r.get("ANOS FINAIS", None), r.get("MÉDIO", None)]
        })
    else:
        ideb_mun = pd.DataFrame({"Etapa de Ensino":[],"IDEB":[]})
    with col2:
        fig_ideb_m = px.bar(ideb_mun, x="Etapa de Ensino", y="IDEB",
                            color="Etapa de Ensino", text="IDEB")
        fig_ideb_m.update_traces(textposition="outside")
        st.plotly_chart(fig_ideb_m, use_container_width=True)

