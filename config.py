# config.py

"""
Arquivo de configuração para centralizar nomes de arquivos, abas de planilha e 
outras constantes usadas no aplicativo Streamlit.
"""

# --- Nomes dos Arquivos ---
CIDADES_FILE = "cidades.csv"
GEOJSON_FILE = "municipios_caparao.geojson"
BASE_DE_DADOS_XLSX_FILE = "base_de_dados.xlsx" # ÚNICO ARQUIVO EXCEL

# --- Nomes das Abas (Sheets) do arquivo base_de_dados.xlsx ---
SHEET_GEO = "Dados geográficos"
SHEET_EMPREGOS_SETOR = "Empregados por setor"
SHEET_EMPREGOS_FAIXA = "Empregados por faixa etária"
SHEET_EMPRESAS = "Empresas por segmento"
SHEET_INST_ENSINO = "Instituições de ensino"
SHEET_IDEB = "Índices educacionais (IDEB)"
SHEET_INSTITUICOES = "Instituições"

# --- Mapeamento de Colunas (sem alterações) ---

# Coluna principal para filtros
MUNICIPIO_COL = "Município"

# Colunas de 'cidades.csv'
IDH_COL = "IDH (IBGE/2010)"
PIB_PER_CAPITA_COL = "PIB / RENDA PER CAPITA (IBGE/2021)"
POP_ESTIMADA_COL = "POPUL. ESTIMADA (IBGE/2024)"
HABITANTES_COL = "HABITANTES (IJSN/2022)"
POP_ATIVA_COL = "POPUL. COM IDADE ATIVA (IJSN/2022)"
POP_OCUPADA_COL = "ÍNDICE DE POPUL. OCUPADA (IBGE/2022)"
RENDA_PER_CAPITA_SM_COL = "MÉDIA DE RENDA PER CAPITA EM Nº DE SALÁRIOS MÍNIMOS (IBGE/2022)"

# Colunas de 'Empregados por setor'
SETOR_COL = "Setor de Atuação"
EMPREGADOS_SETOR_VAL_COL = "Total Empregados"

# Colunas de 'Empregados por faixa etária'
FAIXA_ETARIA_COL = "Faixa Etária"
EMPREGADOS_FAIXA_ETARIA_VAL_COL = "Total Empregados"

# Colunas de 'Empresas por segmento'
PORTE_EMPRESA_COL = "Porte"
EMPRESAS_QTD_COL = "Quantidade"

# Colunas de 'Instituições de ensino'
REDE_ENSINO_COL = "Rede de Ensino"
NIVEL_ENSINO_COL = "Nível de Ensino"
INST_ENSINO_QTD_COL = "Nº de Instituições"

# Colunas de 'Índices educacionais (IDEB)'
ETAPA_ENSINO_COL = "Etapa de Ensino"
IDEB_VAL_COL = "IDEB"

# Colunas de 'Instituições'
CATEGORIA_INST_COL = "Categoria"
INST_CATEGORIA_QTD_COL = "Nº de Instituições"
SUBCATEGORIA_INST_COL = "Subcategoria" 

# Colunas de 'Dados geográficos'
ZONA_COL = "Zona"
PERCENTUAL_COL = "Percentual"