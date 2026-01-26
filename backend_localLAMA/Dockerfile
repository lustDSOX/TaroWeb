FROM python:3.10-slim

WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем только необходимые Python-файлы
COPY app.py layout.py translator.py prompts.py ./

EXPOSE 8000

# HEALTHCHECK --interval=60s --timeout=10s --start-period=40s --retries=3 \
#   CMD python -c "import requests; requests.get('http://localhost:8000/docs')"

CMD ["python", "app.py"]
