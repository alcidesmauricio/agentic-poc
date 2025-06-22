#!/bin/bash

# Caminho base do projeto
PROJ_DIR=$(pwd)

# 1. Criar venv se não existir
if [ ! -d ".venv" ]; then
  echo "Criando ambiente virtual..."
  python3 -m venv .venv
fi

# 2. Ativar o venv
echo "Ativando ambiente virtual..."
source .venv/bin/activate

# 3. Instalar dependências
echo "Instalando dependências do requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Exportar PYTHONPATH para raiz do projeto
echo "Exportando PYTHONPATH..."
export PYTHONPATH="$PROJ_DIR"

# 5. Rodar o watcher FSM com heartbeat
echo "Iniciando watcher FSM de e-mail com heartbeat..."

python -c "
import asyncio
from datetime import datetime
from backend.events.email_watcher_async import run_email_fsm

async def fsm_heartbeat():
    while True:
        print(f'FSM ativo - {datetime.now().strftime(\"%H:%M:%S\")} aguardando eventos...')
        await asyncio.sleep(60)

async def main():
    fsm_task = asyncio.create_task(run_email_fsm())
    heartbeat_task = asyncio.create_task(fsm_heartbeat())
    await asyncio.gather(fsm_task, heartbeat_task)

asyncio.run(main())
"