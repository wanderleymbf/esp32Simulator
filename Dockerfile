FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY esp32_simulador.py .

CMD ["python", "-u", "esp32_simulador.py"]
