#!/bin/bash

if [ -f "/app/.nomodelbuild" ]; then
    echo "Downloading model during runtime..."
    ollama serve & (while ! ollama list | grep -q "NAME"; do sleep 1; done) && ollama pull llama3.2-vision
fi

ollama serve & while ! ollama list | grep -q "NAME"; do sleep 1; done
python fetchbridges.py 