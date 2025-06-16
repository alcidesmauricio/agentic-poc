import openai
import json
from backend.agentic_core.tools import tool_specs, tool_implementations

class OpenAIClient:
    def __init__(self):
        self.model = "gpt-4o"

    def get_completion(self, prompt):
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return str(e)

    def get_completion_with_tools(self, prompt):
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                tools=tool_specs,
                tool_choice="auto"
            )

            message = response.choices[0].message

            if message.get("tool_calls"):
                results = []
                for call in message["tool_calls"]:
                    name = call["function"]["name"]
                    args = json.loads(call["function"]["arguments"])
                    result = tool_implementations[name](**args)
                    results.append(f"📎 {name}: \n{result}")
                return "\n\n".join(results)
            else:
                return message.get("content", "[🤖] Sem resposta.")
        except Exception as e:
            return f"[Erro Tool-Calling]: {str(e)}"
