FROM python:3.11-slim

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

# Dependências de sistema necessárias
RUN apt-get update && apt-get install -y \
    build-essential \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Instala pacotes Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código e dados
COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]
