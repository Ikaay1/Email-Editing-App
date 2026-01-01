from typing import Optional
from generate import GenerateEmail

class EmailService:
    def __init__(self, model: str):
        self.model = model
        self.client = GenerateEmail(model)

    def generate(
        self,
        action: str,
        content: str,
        tone: Optional[str] = None
    ):
        return self.client.generate(action, content, tone)

    def judge(self, original: str, generated: str):
        return self.client.generate("judge", original, None, generated)
