FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get clean && apt-get update && apt-get install -y --no-install-recommends curl wget

RUN curl -fsSL https://ollama.com/install.sh | sh

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x /app/download_model.sh && chmod +x /app/entrypoint.sh
RUN /app/download_model.sh

ENTRYPOINT ["/app/entrypoint.sh"]