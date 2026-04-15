# Imagem base
FROM python:3.10-slim

WORKDIR /app

# Instala as dependências
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia o código da aplicação
COPY . .

# Expõe a porta
EXPOSE 8000

# Comando para iniciar o FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
