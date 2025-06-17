from abc import ABC, abstractmethod
from typing import List, Dict

class PlannerBase(ABC):
    @abstractmethod
    def generate_plan(self, user_input: str, history: List[Dict] = []) -> List[Dict]:
        pass