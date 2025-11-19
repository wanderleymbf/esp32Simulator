# Usar uma imagem base mais completa do Python
FROM python:3.9-buster

# Atualizar repositórios e instalar as dependências necessárias
RUN apt-get update && apt-get install -y \
    tk \
    libjpeg62-turbo-dev \ 
    libfreetype6-dev \
    libx11-dev \
    libxext6 \
    libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar os arquivos do projeto para o container
COPY . /app

# Instalar as dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta que a aplicação irá rodar
EXPOSE 8888

# Comando para rodar o script Python
CMD ["python", "mqtt_simulator.py"]
