from backend.tools.registry import register_tool
from backend.tools.dynamic_agents_loader import list_all_agents
from backend.interfaces.openai_client import OpenAIClient
import json

@register_tool("agent_router")
async def agent_router_tool(input_text: str, master_agent: str = None, child_agents: list = None) -> str:
    if not child_agents:
        return '{"agent": "none"}'
    all_agents = list_all_agents()
    master_obj = next((a for a in all_agents if a["name"] == master_agent), None)
    child_objs = [a for a in all_agents if a["name"] in child_agents]
    master_prompt = master_obj["system_prompt"] if master_obj else ""
    prompt = f"""{master_prompt}
Como agente master '{master_agent}', sua tarefa é escolher o melhor agente filho para responder ao usuário.
Usuário: {input_text}
Agentes filhos disponíveis:
{chr(10).join([f"- {a['name']}: {a['description']}" for a in child_objs])}
Responda apenas com o nome do agente filho em JSON, por exemplo: {{"agent": "qa_agent"}}.
Se não souber, responda {{"agent": "none"}}.
"""
    llm = OpenAIClient()
    import asyncio
    result = await asyncio.to_thread(llm.complete, prompt)
    print("Prompt enviado ao LLM:", prompt)
    print("Resposta bruta do LLM:", result)
    try:
        agent = json.loads(result).get("agent", "none")
    except Exception:
        agent = "none"
    return json.dumps({"agent": agent})