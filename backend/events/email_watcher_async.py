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
