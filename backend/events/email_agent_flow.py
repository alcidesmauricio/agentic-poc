import asyncio
from backend.events.email_reader import fetch_latest_email
from backend.events.email_forwarder import forward_email
from backend.agent.orchestrator import Orchestrator
from dotenv import load_dotenv

load_dotenv()

async def run_email_flow():
    email_data = fetch_latest_email()
    if not email_data:
        print("Sem e-mails novos.")
        return

    orchestrator = Orchestrator(mode="llm")
    async for step in orchestrator.run(
        f"Classifique e redirecione este e-mail:{email_data}"
    ):
        print(step)
        if "trabalho" in step.lower():
            forward_email(email_data, "alcides.filho@zup.com.br")
        elif "pessoal" in step.lower():
            forward_email(email_data, "piratadotejuco@hotmail.com")

if __name__ == "__main__":
    asyncio.run(run_email_flow())

