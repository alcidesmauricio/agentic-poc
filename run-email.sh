#!/bin/bash

# Caminho base do projeto
PROJ_DIR=$(pwd)

# 1. Criar venv se não existir
if [ ! -d ".venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv .venv
fi

# 2. Ativar venv
echo "Ativando ambiente virtual..."
source .venv/bin/activate

# 3. Atualizar pip e instalar dependências
echo "Instalando dependências..."
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4. Exportar variáveis do .env + definir PYTHONPATH
echo "Exportando variáveis de ambiente..."
export PYTHONPATH=$PROJ_DIR
export $(grep -v '^#' .env | xargs)

# 5. Rodar FSM + Planner + Replanner com log ao vivo
echo "Rodando watcher async com FSM + Planner + Replanner (Gmail)..."
mkdir -p logs
python backend/events/email_watcher_async.py 2>&1 | tee logs/email_flow.log