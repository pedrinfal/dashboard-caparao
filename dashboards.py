import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Resumo Caparaó", layout="wide")

# === Leitura e tratamento dos dados ===
df = pd.read_csv("cidades.csv", sep=",", decimal=",")

# Limpando e convertendo colunas para float
df["HABITANTES (IJSN/2022)"] = df["HABITANTES (IJSN/2022)"].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float)
df["POPUL. COM IDADE ATIVA (IJSN/2022)"] = df["POPUL. COM IDADE ATIVA (IJSN/2022)"].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float)
df["POPUL. ESTIMADA (IBGE/2024)"] = df["POPUL. ESTIMADA (IBGE/2024)"].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float)
df["IDH (IBGE/2010)"] = df["IDH (IBGE/2010)"].astype(float)
df["ÍNDICE DE POPUL. OCUPADA (IBGE/2022)"] = df["ÍNDICE DE POPUL. OCUPADA (IBGE/2022)"].str.replace(",", ".").str.replace("%", "").astype(float)
df["MÉDIA DE RENDA PER CAPITA EM Nº DE SALÁRIOS MÍNIMOS (IBGE/2022)"] = df["MÉDIA DE RENDA PER CAPITA EM Nº DE SALÁRIOS MÍNIMOS (IBGE/2022)"].astype(str).str.replace(",", ".").astype(float)
df["PIB / RENDA PER CAPITA (IBGE/2021)"] = (
    df["PIB / RENDA PER CAPITA (IBGE/2021)"]
    .str.replace("R\$", "", regex=True)
    .str.replace(" ", "")
    .str.replace(",", "", regex=False)  # remove vírgula de milhar (se houver)
    .astype(float)
)

# === Cálculo dos indicadores ===
zona_urbana = 64.99
zona_rural = 35.01

idh_medio = df["IDH (IBGE/2010)"].mean()
pib_per_capita = df["PIB / RENDA PER CAPITA (IBGE/2021)"].mean()
pop_estimada = df["POPUL. ESTIMADA (IBGE/2024)"].sum()
habitantes = df["HABITANTES (IJSN/2022)"].sum()
pop_idade_ativa = df["POPUL. COM IDADE ATIVA (IJSN/2022)"].sum()
perc_pop_ocupada = df["ÍNDICE DE POPUL. OCUPADA (IBGE/2022)"].mean()
renda_per_capita_sm = df["MÉDIA DE RENDA PER CAPITA EM Nº DE SALÁRIOS MÍNIMOS (IBGE/2022)"].mean()
perc_pop_ativa = (pop_idade_ativa / habitantes) * 100

# === Layout ===
st.markdown("<h1 style='text-align:center; color: ##0dcaf0;'>Dashboard Gênesis Caparaó</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align:center;'>Resumo da Região do Caparaó</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("<h3 style='text-align:center;'>Concentração Geográfica</h3>", unsafe_allow_html=True)
    geo_df = pd.DataFrame({
        'Zona': ['Urbana', 'Rural'],
        'Valor': [zona_urbana, zona_rural]
    })
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

# === Função para criar cards de KPI ===
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

# === Linha 1 KPIs ===
col1, col2, col3, col4 = st.columns(4)
with col1:
    kpi_card("IDH MÉDIO", f"{idh_medio:.3f}", "📈", "#FFA500")
with col2:
    kpi_card("PIB PER CAPITA", f"R$ {pib_per_capita:,.2f}", "💰", "#28a745")
with col3:
    kpi_card("POP. ESTIMADA 2024", f"{pop_estimada:,.0f}", "👥", "#007bff")
with col4:
    kpi_card("HABITANTES (CENSO)", f"{habitantes:,.0f}", "🏡", "#6f42c1")

# === Linha 2 KPIs ===
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

# === Dados fictícios simulando os da imagem ===
# Você pode substituir pelos dados reais da sua planilha futuramente

# Dados de empregos por setor
empregos_setor = pd.DataFrame({
    "Setor": ["Agricultura", "Industria", "Comercio", "AdministracaoPublica", "Servicos"],
    "Total Empregados": [1100, 2800, 7200, 5400, 6900]
})

# Dados de empregos por faixa etária
empregos_faixa_etaria = pd.DataFrame({
    "Faixa Etária": ["15-17", "18-24", "25-29", "30-39", "40-49", "50-64", "65-mais"],
    "Total Empregados": [100, 4900, 4700, 7900, 6000, 3800, 300]
})

# === Gráficos ===
st.markdown("<h2 style='text-align:center;'>Economia e Mercado de Trabalho Regional</h2>", unsafe_allow_html=True)

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


# === EMPREENDEDORISMO E EMPRESAS ===

st.markdown("<h2 style='text-align:center;'>Empresas e Empreendedorismo Regional</h2>", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

# Dados fictícios baseados na imagem enviada
empresas_tipo = pd.DataFrame({
    "Tipo": ["ME", "MEI", "Outras", "EPP"],
    "Quantidade": [775, 182, 33, 10]
})

with col1:
    st.markdown("<h4 style='text-align:center; padding: 0em 2em 0em 0em; margin: 0em 2em 0em 0em;'>Empresas por Tipo</h4>", unsafe_allow_html=True)
    fig_empresas = px.pie(empresas_tipo, names='Tipo', values='Quantidade', hole=0.5,
                          color_discrete_sequence=['#fdae6b', '#fdd0a2', '#d9d0ec', '#80cdc1'])
    fig_empresas.update_traces(textinfo='percent+label')
    fig_empresas.update_layout(margin=dict(t=20, b=20))
    st.plotly_chart(fig_empresas, use_container_width=True)

with col2:
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

# === EDUCAÇÃO REGIONAL ===

st.markdown("<h2 style='text-align:center;'>Educação Regional</h2>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

# Dados fictícios simulando os da imagem enviada
escolas_rede = pd.DataFrame({
    "Rede de Ensino": ["Municipais", "Estaduais", "Particulares", "Federais"],
    "Número de Escolas": [143, 28, 17, 3]
})

ideb_medio = pd.DataFrame({
    "Etapa de Ensino": ["Anos Iniciais", "Anos Finais", "Ensino Médio"],
    "IDEB": [6.1, 5.5, 4.9]
})

instituicoes_nivel = pd.DataFrame({
    "Nível de Ensino": ["Fundamental", "Infantil", "Medio", "Superior", "Tecnica"],
    "Nº de Instituições": [122, 115, 34, 55, 32]
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

# === INSTITUIÇÕES REGIONAIS ===

st.markdown("<h2 style='text-align:center; color: ##0dcaf0;'>INSTITUIÇÕES REGIONAIS</h2>", unsafe_allow_html=True)

st.markdown("<h4 style='text-align:center;'>Instituições por Categoria</h4>", unsafe_allow_html=True)

# Dados fictícios simulando o gráfico da imagem
instituicoes_categoria = pd.DataFrame({
    "Categoria": ["ASSOCIACAO", "ECONOMIA", "EDUCACAO", "EMPREENDEDORISMO", "FOMENTO", "GOVERNO", "SINDICATO"],
    "Nº de Instituições": [22, 130, 357, 9, 40, 132, 33]
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



import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(page_title="Resumo Caparaó", layout="wide")

# === Leitura e tratamento dos dados ===
df = pd.read_csv("cidades.csv", sep=",", decimal=",")

df["HABITANTES (IJSN/2022)"] = df["HABITANTES (IJSN/2022)"].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float)
df["POPUL. COM IDADE ATIVA (IJSN/2022)"] = df["POPUL. COM IDADE ATIVA (IJSN/2022)"].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float)
df["POPUL. ESTIMADA (IBGE/2024)"] = df["POPUL. ESTIMADA (IBGE/2024)"].astype(str).str.replace(".", "", regex=False).str.replace(",", ".", regex=False).astype(float)
df["IDH (IBGE/2010)"] = df["IDH (IBGE/2010)"].astype(float)
df["ÍNDICE DE POPUL. OCUPADA (IBGE/2022)"] = df["ÍNDICE DE POPUL. OCUPADA (IBGE/2022)"].str.replace(",", ".").str.replace("%", "").astype(float)
df["MÉDIA DE RENDA PER CAPITA EM Nº DE SALÁRIOS MÍNIMOS (IBGE/2022)"] = df["MÉDIA DE RENDA PER CAPITA EM Nº DE SALÁRIOS MÍNIMOS (IBGE/2022)"].astype(str).str.replace(",", ".").astype(float)
df["PIB / RENDA PER CAPITA (IBGE/2021)"] = (
    df["PIB / RENDA PER CAPITA (IBGE/2021)"]
    .str.replace("R\$", "", regex=True)
    .str.replace(" ", "")
    .str.replace(",", "", regex=False)
    .astype(float)
)

# Leitura do GeoJSON local
with open("municipios_caparao.geojson", "r", encoding="utf-8") as f:
    geojson_data = json.load(f)

# === Mapa Interativo ===
st.markdown("<h2 style='text-align:center;'>Mapa Interativo dos Municípios</h2>", unsafe_allow_html=True)

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
    hover_data={
        "MUNICIPIO": True,
        "IDH (IBGE/2010)": True,
        "PIB / RENDA PER CAPITA (IBGE/2021)": True
    }
)
fig_mapa.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig_mapa, use_container_width=True)

# === Filtro por município ===
municipio_escolhido = st.selectbox(
    "Selecione o município para filtrar os dados:",
    options=df["MUNICIPIO"].unique()
)

df_filtrado = df[df["MUNICIPIO"] == municipio_escolhido]

if not df_filtrado.empty:
    habitantes = df_filtrado["HABITANTES (IJSN/2022)"].sum()

    # === EMPREGOS ===
    st.markdown("<h2 style='text-align:center;'>Economia e Mercado de Trabalho do Município</h2>", unsafe_allow_html=True)

    empregos_setor = pd.DataFrame({
        "Setor": ["Agricultura", "Industria", "Comercio", "AdministracaoPublica", "Servicos"],
        "Total Empregados": [int(habitantes * 0.05), int(habitantes * 0.1),
                             int(habitantes * 0.25), int(habitantes * 0.15),
                             int(habitantes * 0.2)]
    })

    empregos_faixa_etaria = pd.DataFrame({
        "Faixa Etária": ["15-17", "18-24", "25-29", "30-39", "40-49", "50-64", "65-mais"],
        "Total Empregados": [int(habitantes * 0.01), int(habitantes * 0.08),
                             int(habitantes * 0.07), int(habitantes * 0.12),
                             int(habitantes * 0.1), int(habitantes * 0.05),
                             int(habitantes * 0.01)]
    })

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<h4 style='text-align:center;'>Empregos por Setor</h4>", unsafe_allow_html=True)
        fig_setor = px.bar(empregos_setor, x="Setor", y="Total Empregados",
                           color="Setor", text="Total Empregados")
        fig_setor.update_traces(textposition="outside")
        st.plotly_chart(fig_setor, use_container_width=True)

    with col2:
        st.markdown("<h4 style='text-align:center;'>Empregos por Faixa Etária</h4>", unsafe_allow_html=True)
        fig_faixa = px.bar(empregos_faixa_etaria, x="Faixa Etária", y="Total Empregados",
                           color="Faixa Etária", text="Total Empregados")
        fig_faixa.update_traces(textposition="outside")
        st.plotly_chart(fig_faixa, use_container_width=True)

    # === EMPRESAS ===
    st.markdown("<h2 style='text-align:center;'>Empresas e Empreendedorismo do Município</h2>", unsafe_allow_html=True)
    empresas_tipo = pd.DataFrame({
        "Tipo": ["ME", "MEI", "Outras", "EPP"],
        "Quantidade": [int(habitantes * 0.01), int(habitantes * 0.02),
                       int(habitantes * 0.005), int(habitantes * 0.003)]
    })
    fig_empresas = px.pie(empresas_tipo, names='Tipo', values='Quantidade', hole=0.5)
    fig_empresas.update_traces(textinfo='percent+label')
    st.plotly_chart(fig_empresas, use_container_width=True)

    # === EDUCAÇÃO ===
    st.markdown("<h2 style='text-align:center;'>Educação do Município</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    escolas_rede = pd.DataFrame({
        "Rede de Ensino": ["Municipais", "Estaduais", "Particulares", "Federais"],
        "Número de Escolas": [int(habitantes * 0.002), int(habitantes * 0.001),
                              int(habitantes * 0.0005), int(habitantes * 0.0002)]
    })
    with col1:
        fig_escolas = px.bar(escolas_rede, x="Rede de Ensino", y="Número de Escolas",
                             color="Rede de Ensino", text="Número de Escolas")
        fig_escolas.update_traces(textposition="outside")
        st.plotly_chart(fig_escolas, use_container_width=True)

    ideb_medio = pd.DataFrame({
        "Etapa de Ensino": ["Anos Iniciais", "Anos Finais", "Ensino Médio"],
        "IDEB": [5.5, 5.0, 4.5]
    })
    with col2:
        fig_ideb = px.bar(ideb_medio, x="Etapa de Ensino", y="IDEB",
                          color="Etapa de Ensino", text="IDEB")
        fig_ideb.update_traces(textposition="outside")
        st.plotly_chart(fig_ideb, use_container_width=True)

    # === INSTITUIÇÕES ===
    st.markdown("<h2 style='text-align:center;'>Instituições do Município</h2>", unsafe_allow_html=True)
    instituicoes_categoria = pd.DataFrame({
        "Categoria": ["ASSOCIACAO", "ECONOMIA", "EDUCACAO", "EMPREENDEDORISMO", "FOMENTO", "GOVERNO", "SINDICATO"],
        "Nº de Instituições": [int(habitantes * 0.0005), int(habitantes * 0.001),
                               int(habitantes * 0.002), int(habitantes * 0.0003),
                               int(habitantes * 0.0004), int(habitantes * 0.001),
                               int(habitantes * 0.0003)]
    })
    fig_inst_cat = px.bar(instituicoes_categoria, x="Categoria", y="Nº de Instituições",
                          color="Categoria", text="Nº de Instituições")
    fig_inst_cat.update_traces(textposition="outside")
    st.plotly_chart(fig_inst_cat, use_container_width=True)

else:
    st.warning("Município selecionado sem dados disponíveis.")