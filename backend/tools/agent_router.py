from backend.tools.registry import register_tool
from backend.agent.orchestrator import Orchestrator
from typing import List

@register_tool("agent_router")
async def agent_router_tool(input_text: str, master_agent: str = None, child_agents: List[str] = None) -> str:
    """
    Roteia a entrada para o agente adequado com base no contexto.
    """
    orchestrator = Orchestrator(mode="default", master_agent=master_agent, child_agents=child_agents)
    
    output = []
    async for step in orchestrator.run(input_text):
        output.append(step)

    return "\n".join(output)