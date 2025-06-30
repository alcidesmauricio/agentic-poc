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
            result = call_tool_by_name(tool_name, args)
            previous_result = result.get("message", result) if isinstance(result, dict) else result

            yield f"#json✅ Resultado de {tool_name}: {previous_result}\n"

            if self.replanning_enabled:
                self.fsm.transition_to(AgentState.PLANNING)
                plan = planner.generate_plan(previous_result, history)
                yield f"#json📝 Novo plano gerado após replanning: {plan}\n"

        self.fsm.transition_to(AgentState.IDLE)

    async def run_with_agents(self, user_input: str):
        self.fsm.transition_to(AgentState.EXECUTING)
        context = ""
        master_prompt = (
            "Você é um agente coordenador. Com base na entrada do usuário "
            "e nas descrições dos agentes disponíveis, escolha o agente mais adequado, "
            "envie a solicitação e devolva a resposta formatada para o usuário.\n"
        )

        context += f"Usuário: {user_input}\n"

        tools_description = "\n".join([
            f"- {agent['name']}: {agent['description']}"
            for agent in self.child_agents
        ])
        context += f"Agentes disponíveis:\n{tools_description}\n"

        full_prompt = f"{master_prompt}{context}\nQual agente deve ser chamado?"

        response = await self.llm.chat(full_prompt)
        yield f"#bash🧖 Agente master escolheu: {response}\n"

        # Localiza agente correspondente
        selected = None
        for agent in self.child_agents:
            if agent["name"] in response:
                selected = agent
                break

        if not selected:
            yield "#bash⚠️ Nenhum agente filho reconhecido foi identificado na resposta.\n"
            return

        agent_prompt = selected["system_prompt"]
        child_llm = OpenAIClient(system_prompt=agent_prompt)
        child_response = await child_llm.chat(user_input)

        yield f"#json📨 Resposta do agente {selected['name']}:\n{child_response}\n"
        self.fsm.transition_to(AgentState.IDLE)