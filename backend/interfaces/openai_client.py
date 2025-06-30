import os
import openai
import json
import asyncio
from dotenv import load_dotenv
from backend.interfaces.llm_interface import LLMInterface
from backend.tools.registry import get_registered_tools, call_tool_by_name

load_dotenv()

class OpenAIClient(LLMInterface):
    def __init__(self, model: str = "gpt-4o"):
        self.model = model
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def complete(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[Erro OpenAI]: {e}"

    def complete_with_tools(self, user_input: str) -> str:
        try:
            tools = get_registered_tools()
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": user_input}],
                tools=tools,
                tool_choice="auto"
            )
            message = response.choices[0].message

            # message.tool_calls agora é um atributo, não um dict
            if hasattr(message, "tool_calls") and message.tool_calls:
                results = []
                for call in message.tool_calls:
                    name = call.function.name
                    args = json.loads(call.function.arguments)
                    result = call_tool_by_name(name, args)
                    results.append(f"[🔧 {name}]\n{result}")
                return "\n\n".join(results)
            else:
                # message.content pode ser None
                return message.content or "[🤖] Sem resposta."
        except Exception as e:
            return f"[Erro Tool-Calling]: {str(e)}"
        
    def chat(self, system: str, user: str):
            """
            Método usado pelo LLMPlanner para gerar plano de ação (tool-calling).
            """
            tools = get_registered_tools()

            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system},
                        {"role": "user", "content": user}
                    ],
                    tools=tools,
                    tool_choice="auto"
                )
                message = response.choices[0].message

                if hasattr(message, "tool_calls") and message.tool_calls:
                    plan = []
                    for call in message.tool_calls:
                        name = call.function.name
                        args = json.loads(call.function.arguments)
                        plan.append({"tool": name, "args": args})
                    return plan
                else:
                    return []
            except Exception as e:
                return f"[Erro no planner com tool-calling]: {e}"  

    async def chat_async(self, system: str, user: str):
        return await asyncio.to_thread(self.chat, system, user)                  