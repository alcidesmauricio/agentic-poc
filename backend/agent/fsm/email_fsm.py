from enum import Enum, auto

class EmailFSMState(Enum):
    IDLE = auto()
    READING = auto()
    DECIDING = auto()
    FORWARDING = auto()
    DONE = auto()

class EmailStateMachine:
    def __init__(self):
        self.state = EmailFSMState.IDLE

    def transition(self, new_state):
        print(f"[FSM] {self.state.name} -> {new_state.name}")
        self.state = new_state
