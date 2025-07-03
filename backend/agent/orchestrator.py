import re
2
import json
from backend.tools.registry import call_tool_by_name
from backend.interfaces.openai_client import OpenAIClient
from backend.planner.llm_planner import LLMPlanner
from backend.planner.rule_based import RuleBasedPlanner
from backend.agent.fsm.state_machine import StateMachine, AgentState

class Orchestrator:
    def __init__(self, mode="rule", master_agent=None, child_agents=None):
        self.mode = mode
        self.master_agent = master_agent
        self.child_agents = child_agents or []
        self.replanning_enabled = True
        self.llm = OpenAIClient()
        self.fsm = StateMachine()

    async def run(self, user_input: str):
        if self.master_agent and self.child_agents:
            async for step in self.run_with_agents(user_input):
                yield step
        else:
            async for step in self.run_with_planner(user_input):
                yield step

    async def run_with_planner(self, user_input: str):
        planner = LLMPlanner() if self.mode == "llm" else RuleBasedPlanner()
        history = []
        self.fsm.transition_to(AgentState.PLANNING)
        plan = planner.generate_plan(user_input, history)
        yield f"#json📝 Plano gerado:\n{plan}\n"
        previous_result = None

        for step in plan:
            tool_name = step["tool"]
            args = step.get("args", {})
            if "__previous__" in args.values():
                for k, v in args.items():
                    if v == "__previous__":
                        args[k] = previous_result

            self.fsm.transition_to(AgentState.EXECUTING)
            result = await call_tool_by_name(tool_name, args)
            previous_result = result.get("message", result) if isinstance(result, dict) else result

            yield f"#json✅ Resultado de {tool_name}: {previous_result}\n"

            if self.replanning_enabled:
                self.fsm.transition_to(AgentState.PLANNING)
                safe_input = previous_result
                if not isinstance(safe_input, str):
                    safe_input = json.dumps(safe_input, ensure_ascii=False)
                plan = planner.generate_plan(safe_input, history)
                yield f"#json📝 Novo plano gerado após replanning: {plan}\n"

        self.fsm.transition_to(AgentState.IDLE)

    async def run_with_agents(self, user_input: str):
        self.fsm.transition_to(AgentState.EXECUTING)
        args = {
            "input_text": user_input,
            "master_agent": self.master_agent["name"] if self.master_agent else None,
            "child_agents": [agent["name"] for agent in self.child_agents]
        }
        router_result = await call_tool_by_name("agent_router", args)
        print(f"router_result:{router_result}")
        cleaned = re.sub(r"```(?:json)?", "", router_result).replace("```", "").strip()

        try:
            agent_name = json.loads(cleaned).get("agent")
        except Exception:
            agent_name = None

        if not agent_name or agent_name == "none":
            yield "#bash Nenhum agente filho reconhecido foi identificado na resposta.\n"
            self.fsm.transition_to(AgentState.IDLE)
            return

        # Chama a tool dinâmica do agent escolhido
        agent_tool_args = {"input": user_input}
        agent_result = await call_tool_by_name(agent_name, agent_tool_args)
        yield f"#json Resposta do agente {agent_name}:\n{agent_result}\n"
        self.fsm.transition_to(AgentState.IDLE)