FROM python:3.9-slim

# Установка зависимостей для Pillow
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt Pillow

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "transit_point.wsgi:application"]