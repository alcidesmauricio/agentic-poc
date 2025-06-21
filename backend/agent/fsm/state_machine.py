from enum import Enum, auto

class AgentState(Enum):
    IDLE = auto()
    PLANNING = auto()
    EXECUTING = auto()
    WAITING = auto()
    ERROR = auto()

class StateMachine:
    def __init__(self):
        self.state = AgentState.IDLE

    def transition_to(self, new_state: AgentState):
        print(f"[FSM] Transição: {self.state.name} → {new_state.name}")
        self.state = new_state

    def get_state(self):
        return self.state
