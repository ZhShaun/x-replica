FROM mcr.microsoft.com/devcontainers/python:3.12

RUN apt-get update && \
    apt-get install -y sqlite3 && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
