# config.py

"""
ARQUIVO DE CONFIGURAÇÃO

Este arquivo centraliza todos os nomes de arquivos, abas de planilha e 
nomes de colunas para facilitar a organização e manutenção do código.
Se algum nome de coluna na sua planilha mudar, basta alterá-lo aqui.
"""

# --- Nomes dos Arquivos de Dados ---
CIDADES_FILE = "cidades.csv"
GEOJSON_FILE = "municipios_caparao.geojson"
BASE_DE_DADOS_XLSX_FILE = "base_de_dados.xlsx" # Onde estão os dados principais

# --- Nomes das Abas (Sheets) do arquivo base_de_dados.xlsx ---
# Verifique se estes nomes correspondem exatamente às suas abas no Excel
SHEET_GEO = "Dados geográficos"
SHEET_EMPREGOS_SETOR = "Empregados por setor"
SHEET_EMPREGOS_FAIXA = "Empregados por faixa etária"
SHEET_EMPRESAS = "Empresas por segmento"
SHEET_INST_ENSINO = "Instituições de ensino"
SHEET_IDEB = "Índices educacionais (IDEB)"
SHEET_INSTITUICOES = "Instituições"

# --- Mapeamento de Nomes de Colunas ---
# O nome da coluna como está no seu arquivo -> A variável que o código usa

# Coluna principal para filtros, presente em quase todas as planilhas
MUNICIPIO_COL = "Município"

# Colunas do arquivo cidades.csv
IDH_COL = "IDH (IBGE/2010)"
PIB_PER_CAPITA_COL = "PIB / RENDA PER CAPITA (IBGE/2021)"
POP_ESTIMADA_COL = "POPUL. ESTIMADA (IBGE/2024)"
HABITANTES_COL = "HABITANTES (IJSN/2022)"
POP_ATIVA_COL = "POPUL. COM IDADE ATIVA (IJSN/2022)"
POP_OCUPADA_COL = "ÍNDICE DE POPUL. OCUPADA (IBGE/2022)"
RENDA_PER_CAPITA_SM_COL = "MÉDIA DE RENDA PER CAPITA EM Nº DE SALÁRIOS MÍNIMOS (IBGE/2022)"

# Colunas da aba 'Empregados por setor'
SETOR_COL = "Setor de Atuação" # Corrigido com base na sua imagem
EMPREGADOS_SETOR_VAL_COL = "Total Empregados"

# Colunas da aba 'Empregados por faixa etária'
FAIXA_ETARIA_COL = "Faixa Etária"
EMPREGADOS_FAIXA_ETARIA_VAL_COL = "Total Empregados"

# Colunas da aba 'Empresas por segmento'
PORTE_EMPRESA_COL = "Porte"
EMPRESAS_QTD_COL = "Quantidade"

# Colunas da aba 'Instituições de ensino'
REDE_ENSINO_COL = "Rede de Ensino"
NIVEL_ENSINO_COL = "Nível de Ensino"
INST_ENSINO_QTD_COL = "Nº de Instituições"

# Colunas da aba 'Índices educacionais (IDEB)'
ETAPA_ENSINO_COL = "Etapa de Ensino"
IDEB_VAL_COL = "IDEB"

# Colunas da aba 'Instituições'
CATEGORIA_INST_COL = "Categoria"
INST_CATEGORIA_QTD_COL = "Nº de Instituições"
SUBCATEGORIA_INST_COL = "Subcategoria" # Usado para os cards.

# Colunas da aba 'Dados geográficos'
ZONA_COL = "Zona"
PERCENTUAL_COL = "Percentual"