FROM python:3.10-slim

# Need to make Docker image smaller
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y curl wget && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://ollama.com/install.sh | sh

# Ollama takes time to start, wait for it then pull
# This will technically use llama3.2-vision@latest, modify it to use whatever model you want
RUN ollama serve & (while ! ollama list | grep -q "NAME"; do sleep 1; done) &&  ollama pull llama3.2-vision@latest

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD /bin/sh -c "ollama serve & while ! ollama list | grep -q 'NAME'; do sleep 1; done; python fetchbridges.py"
