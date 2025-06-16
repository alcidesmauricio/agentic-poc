class StateMachine:
    def __init__(self):
        self.state = "idle"

    def transition(self, event: str):
        if self.state == "idle" and event == "user_input":
            self.state = "thinking"
        elif self.state == "thinking" and event == "plan_ready":
            self.state = "executing"
        elif self.state == "executing" and event == "done":
            self.state = "idle"

    def current_state(self):
        return self.state
