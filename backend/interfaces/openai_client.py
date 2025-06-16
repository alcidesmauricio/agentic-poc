import openai
import json
from backend.interfaces.llm_interface import LLMInterface
from backend.tools.registry import get_registered_tools, call_tool_by_name

class OpenAIClient(LLMInterface):
    def __init__(self, model: str = "gpt-4o"):
        self.model = model

    def complete(self, prompt: str) -> str:
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"[Erro OpenAI]: {e}"

    def complete_with_tools(self, user_input: str) -> str:
        try:
            tools = get_registered_tools()

            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": user_input}],
                tools=tools,
                tool_choice="auto"
            )

            message = response.choices[0].message

            if message.get("tool_calls"):
                results = []
                for call in message["tool_calls"]:
                    name = call["function"]["name"]
                    args = json.loads(call["function"]["arguments"])
                    result = call_tool_by_name(name, args)
                    results.append(f"[🔧 {name}]\n{result}")
                return "\n\n".join(results)
            else:
                return message.get("content", "[🤖] Sem resposta.")
        except Exception as e:
            return f"[Erro Tool-Calling]: {str(e)}"
