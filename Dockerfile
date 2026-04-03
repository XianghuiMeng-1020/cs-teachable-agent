FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV PYTHONPATH=/app
ENV PORT=10000

RUN mkdir -p /app/data

# Verify imports at build time
RUN python -c "from src.api.main import app; print('BUILD CHECK: app import OK')"

EXPOSE 10000
CMD ["python", "start.py"]
