import asyncio
import os
from backend.events.email_decision import analyze_and_decide
from backend.agent.orchestrator import Orchestrator
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    from backend.events.email_watcher_async import EmailWatcherAsync

    watcher = EmailWatcherAsync()
    try:
        asyncio.run(watcher.start())
    except KeyboardInterrupt:
        print("\nWatcher interrompido pelo usuário.", flush=True)

class EmailWatcherAsync:
    def __init__(self):
        self.running = True

    async def start(self):
        while self.running:
            await self.check()
            await asyncio.sleep(20)

    async def check(self):
        print("\nVerificando novos e-mails...", flush=True)
        from backend.utils.email_reader import fetch_unread_emails

        emails = fetch_unread_emails()

        for email_data in emails:
            print(f"E-mail recebido: {email_data}", flush=True)

            print("Analisando conteúdo com IA...", flush=True)
            decision_output = analyze_and_decide(email_data)

            if decision_output["decision"] == "ignore":
                print("E-mail ignorado.\n", flush=True)
                continue

            destination = os.getenv("EMAIL_WORK_DEST") if decision_output["decision"] == "work" else os.getenv("EMAIL_PERSONAL_DEST")
            
            input_for_planner = f"""
            Resumo: {decision_output["summary"]}
            Destinatário: {destination}
            Envie esse resumo por e-mail.
            """

            print("[🛠] Orquestrando decisão com Planner...", flush=True)
            orchestrator = Orchestrator(mode="llm")
            async for step in orchestrator.run(input_for_planner):
                print(f"{step}", flush=True)
