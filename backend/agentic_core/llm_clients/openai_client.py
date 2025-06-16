import openai

class OpenAIClient:
    def __init__(self):
        self.model = "gpt-4o"

    def get_completion(self, prompt):
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return str(e)
