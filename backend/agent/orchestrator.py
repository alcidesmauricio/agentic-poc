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
        master_prompt = (
            "Você é um agente coordenador. Com base na entrada do usuário "
            "e nas descrições dos agentes disponíveis, escolha o agente mais adequado "
            "e responda apenas com o NOME do agente (exatamente como listado abaixo, sem explicações).\n"
        )
        context = f"Usuário: {user_input}\n"
        tools_description = "\n".join(
            [f"- {agent['name']}: {agent['description']}" for agent in self.child_agents]
        )
        context += f"Agentes disponíveis:\n{tools_description}\n"
        system_prompt = master_prompt + context
        user_prompt = (
            "Exemplos:\n"
            "Usuário: Quero falar sobre assuntos financeiros, com quem eu falo?\n"
            "Resposta: {\"agent\": \"finance_agent\"}\n"
            "Usuário: Preciso de ajuda jurídica\n"
            "Resposta: {\"agent\": \"legal_agent\"}\n"
            "Usuário: Não sei com quem falar\n"
            "Resposta: {\"agent\": \"none\"}\n"
            "Usuário: Com qu falo sobre finanças?\n"
            "Resposta: {\"agent\": \"finance_agent\"}\n"
            "---\n"
            f"Usuário: {user_input}\n"
            "Com base na solicitação do usuário e nos agentes disponíveis, "
            "responda apenas com o nome do agente mais adequado em JSON, sem explicações, "
            "por exemplo: {\"agent\": \"finance_agent\"}. "
            "Se não souber, responda {\"agent\": \"none\"}."
        )
        print(f"[DEBUG] system_prompt:\n{system_prompt}\n")
        print(f"[DEBUG] user_prompt:\n{user_prompt}\n")
        response = await self.llm.chat_async(system=system_prompt, user=user_prompt)
        print(f"[DEBUG] Resposta bruta do LLM: {response}")  # Log para depuração
        yield f"#bash Agente master escolheu: {response}\n"

        # Tenta extrair o nome do agente do JSON
        agent_name = None
        try:
            # Se vier uma lista vazia, json.loads vai retornar []
            parsed = json.loads(response)
            if isinstance(parsed, dict) and "agent" in parsed:
                agent_name = parsed["agent"]
            else:
                agent_name = None
        except Exception:
            # fallback: normaliza texto simples
            agent_name = str(response).strip().lower().replace(".", "").replace('"', '')
            if agent_name in ("[]", "", "none", "null"):
                agent_name = None

        selected = None
        if agent_name:
            for agent in self.child_agents:
                if agent["name"].lower() == agent_name.lower():
                    selected = agent
                    break

        if not selected:
            yield "#bash⚠️ Nenhum agente filho reconhecido foi identificado na resposta.\n"
            self.fsm.transition_to(AgentState.IDLE)
            return

        agent_prompt = selected["system_prompt"]
        child_llm = OpenAIClient()   
        child_response = await child_llm.chat_async(system=agent_prompt, user=user_input)
        yield f"#json📨 Resposta do agente {selected['name']}:\n{child_response}\n"
        self.fsm.transition_to(AgentState.IDLE)