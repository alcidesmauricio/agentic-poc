#!/bin/bash

echo "Instalando dependências do backend AI DevAgentic..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "Ambiente pronto."
echo "Iniciando backend com Uvicorn..."
uvicorn backend.main:app --reload
