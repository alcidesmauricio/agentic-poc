import asyncio

class EmailWatcherAsync:
    def __init__(self, check_function, interval=30):
        self.check_function = check_function
        self.interval = interval
        self.running = False

    async def start(self):
        self.running = True
        print("[EmailWatcherAsync] Iniciado")
        while self.running:
            await self.check_function()
            await asyncio.sleep(self.interval)

    def stop(self):
        self.running = False

# 👇 Adicione isso ao final do arquivo
async def run_email_fsm():
    from backend.events.email_agent_flow import run_email_flow  # sua função que processa e-mails

    watcher = EmailWatcherAsync(check_function=lambda: run_email_flow(), interval=30)
    await watcher.start()

if __name__ == "__main__":
    asyncio.run(run_email_fsm())