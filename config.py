# config.py

"""
ARQUIVO DE CONFIGURAÇÃO FINAL E VALIDADO

Este arquivo centraliza todos os nomes de arquivos, abas de planilha e 
nomes de colunas. Os nomes abaixo foram validados com as imagens enviadas
e correspondem exatamente aos seus arquivos Excel.
"""

# --- Nomes dos Arquivos ---
CIDADES_FILE = "cidades.csv"
GEOJSON_FILE = "municipios_caparao.geojson"
BASE_DE_DADOS_XLSX_FILE = "base_de_dados.xlsx"

# --- Nomes das Abas (Sheets) ---
SHEET_GEO = "Dados geográficos"
SHEET_EMPREGOS_SETOR = "Empregados por setor"
SHEET_EMPREGOS_FAIXA = "Empregados por faixa etária"
SHEET_EMPRESAS = "Empresas por segmento"
SHEET_INST_ENSINO = "Instituições de ensino"
SHEET_IDEB = "Índices educacionais (IDEB)"
SHEET_INSTITUICOES = "Instituições"

# --- Mapeamento de Colunas (VALIDADO) ---

MUNICIPIO_COL = "Município"

# Aba 'Dados geográficos'
ZONA_COL = "Zona"
PERCENTUAL_COL = "Percentual"

# Aba 'Empregados por setor'
SETOR_COL = "Setor de Atuação"
EMPREGADOS_SETOR_VAL_COL = "Total Empregados"

# Aba 'Empregados por faixa etária'
FAIXA_ETARIA_COL = "Faixa Etária"
EMPREGADOS_FAIXA_ETARIA_VAL_COL = "Total Empregados"

# Aba 'Empresas por segmento'
PORTE_EMPRESA_COL = "Porte"
EMPRESAS_QTD_COL = "Quantidade"

# Aba 'Instituições de ensino'
REDE_ENSINO_COL = "Rede de Ensino"
NIVEL_ENSINO_COL = "Nível de Ensino"
INST_ENSINO_QTD_COL = "Nº de Instituições" # Nome da coluna gerada pelo código

# Aba 'Índices educacionais (IDEB)'
ETAPA_ENSINO_COL = "Etapa de Ensino"
IDEB_VAL_COL = "IDEB"

# Aba 'Instituições'
CATEGORIA_INST_COL = "Categoria"
INST_CATEGORIA_QTD_COL = "Nº de Instituições" # Nome da coluna gerada pelo código
SUBCATEGORIA_INST_COL = "Subcategoria"

# Colunas do arquivo cidades.csv (Estas não precisam de alteração)
IDH_COL = "IDH (IBGE/2010)"
PIB_PER_CAPITA_COL = "PIB / RENDA PER CAPITA (IBGE/2021)"
POP_ESTIMADA_COL = "POPUL. ESTIMADA (IBGE/2024)"
HABITANTES_COL = "HABITANTES (IJSN/2022)"
POP_ATIVA_COL = "POPUL. COM IDADE ATIVA (IJSN/2022)"
POP_OCUPADA_COL = "ÍNDICE DE POPUL. OCUPADA (IBGE/2022)"
RENDA_PER_CAPITA_SM_COL = "MÉDIA DE RENDA PER CAPITA EM Nº DE SALÁRIOS MÍNIMOS (IBGE/2022)"