# config.py

"""
Arquivo de configuração para centralizar nomes de arquivos, colunas e 
outras constantes usadas no aplicativo Streamlit.
"""

# --- Nomes dos Arquivos de Dados ---
CIDADES_FILE = "cidades.csv"
EMPREGADOS_SETOR_FILE = "base_de_dados.xlsx - Empregados por setor.csv"
EMPREGADOS_FAIXA_ETARIA_FILE = "base_de_dados.xlsx - Empregados por faixa etária.csv"
EMPRESAS_SEGMENTO_FILE = "base_de_dados.xlsx - Empresas por segmento.csv"
INSTITUICOES_ENSINO_FILE = "base_de_dados.xlsx - Instituições de ensino.csv"
IDEB_FILE = "base_de_dados.xlsx - Índices educacionais (IDEB).csv"
INSTITUICOES_FILE = "base_de_dados.xlsx - Instituições.csv"
GEOJSON_FILE = "municipios_caparao.geojson"
DADOS_GEOGRAFICOS_FILE = "base_de_dados.xlsx - Dados geográficos.csv"

# --- Mapeamento de Colunas ---

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

# Colunas de 'Empregados por setor.csv'
SETOR_COL = "Setor"
EMPREGADOS_SETOR_VAL_COL = "Total Empregados"

# Colunas de 'Empregados por faixa etária.csv'
FAIXA_ETARIA_COL = "Faixa Etária"
EMPREGADOS_FAIXA_ETARIA_VAL_COL = "Total Empregados"

# Colunas de 'Empresas por segmento.csv'
PORTE_EMPRESA_COL = "Porte"
EMPRESAS_QTD_COL = "Quantidade"

# Colunas de 'Instituições de ensino.csv'
REDE_ENSINO_COL = "Rede de Ensino"
NIVEL_ENSINO_COL = "Nível de Ensino"
INST_ENSINO_QTD_COL = "Nº de Instituições"

# Colunas de 'Índices educacionais (IDEB).csv'
ETAPA_ENSINO_COL = "Etapa de Ensino"
IDEB_VAL_COL = "IDEB"

# Colunas de 'Instituições.csv'
CATEGORIA_INST_COL = "Categoria"
INST_CATEGORIA_QTD_COL = "Nº de Instituições"
SUBCATEGORIA_INST_COL = "Subcategoria" # Usado para os cards de Aceleradora, etc.

# Colunas de 'Dados geográficos.csv'
ZONA_COL = "Zona"
PERCENTUAL_COL = "Percentual"