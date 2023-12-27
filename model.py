from openai import OpenAI
from openai import APITimeoutError, APIConnectionError, InternalServerError


class GPT(object):
    def __init__(self,
                 model,
                 max_tokens,
                 temperature,
                 api_key="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"):
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.client = OpenAI(api_key=api_key)

    @staticmethod
    def remove_empty_line(answer):
        lines = answer.split("\n")
        concise_lines = [line for line in lines if line]
        concise_answer = "\n".join(concise_lines)
        return concise_answer

    def query(self, question):
        while True:
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": question}],
                    max_tokens=self.max_tokens,
                    temperature=self.temperature
                )
                answer = response.choices[0].message.content
                answer = self.remove_empty_line(answer)
                return answer
            except APITimeoutError:
                continue
            except APIConnectionError:
                continue
            except InternalServerError:
                continue
