import threading
import time

class EmailWatcherScheduled:
    def __init__(self, check_function, interval=30):
        self.check_function = check_function
        self.interval = interval
        self.running = False
        self.thread = threading.Thread(target=self.run, daemon=True)

    def run(self):
        self.running = True
        print("[📬 EmailWatcherScheduled] Iniciado")
        while self.running:
            self.check_function()
            time.sleep(self.interval)

    def start(self):
        self.thread.start()

    def stop(self):
        self.running = False
