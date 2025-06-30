import json
import os
from backend.tools.registry import register_tool

AGENTS_JSON_PATH = os.path.join(os.path.dirname(__file__), "agents_config.json")

def load_dynamic_agents():
    if not os.path.exists(AGENTS_JSON_PATH):
        print(f"[⚠️] Arquivo agents_config.json não encontrado em {AGENTS_JSON_PATH}")
        return

    with open(AGENTS_JSON_PATH, "r", encoding="utf-8") as file:
        agents = json.load(file)

    for agent in agents:
        tool_name = agent["name"]
        description = agent["description"]
        system_prompt = agent["system_prompt"]

        def make_tool(prompt):
            @register_tool(
                name=tool_name,
                description=description,
                parameters={
                    "type": "object",
                    "properties": {
                        "input": {
                            "type": "string",
                            "description": "Entrada do usuário para o agente"
                        }
                    },
                    "required": ["input"]
                }
            )
            def dynamic_agent(input: str):
                from backend.interfaces.openai_client import OpenAIClient
                llm = OpenAIClient(system_prompt=prompt)
                return llm.chat(input)
            return dynamic_agent

        make_tool(system_prompt)