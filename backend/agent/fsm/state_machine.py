from enum import Enum

class AgentState(str, Enum):
    IDLE = "idle"
    PLANNING = "planning"
    EXECUTING = "executing_step"
    REPLANNING = "replanning"
    END = "end"

class StateMachine:
    def __init__(self):
        self.state = AgentState.IDLE

    def transition_to(self, new_state):
        print(f"[FSM] Transição de estado: {self.state} -> {new_state}")
        self.state = new_state

    def transition(self, new_state):
        self.transition_to(new_state)
