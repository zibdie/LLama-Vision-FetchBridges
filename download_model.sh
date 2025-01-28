#!/bin/bash

if [ ! -f "/app/.nomodelbuild" ]; then
    echo "Downloading model during build..."
    ollama serve & (while ! ollama list | grep -q "NAME"; do sleep 1; done) && ollama pull llama3.2-vision
else
    echo "Skipping model download during build. It will be downloaded when the container runs."
fi