import json
import logging
from openai import AsyncClient
from openai.types.chat_model import ChatModel

from configs import constants


class AIClient(AsyncClient):
    def __init__(self, model: ChatModel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model

    async def rate_messages(self, history: list[str], new_messages: list[str]) -> list[int]:
        if not history or new_messages:
            return []

        ai_messages = [
            {
                "role": "system",
                "content": constants.IS_DUPLICATE_PROMPT,
            },
            {
                "role": "user",
                "content": json.dumps({"history": history, "new_messages": new_messages}),
            },
        ]

        chat = await self.chat.completions.create(
            messages=ai_messages, model=self.model,
        )

        try:
            resp = json.loads(chat.choices[0].message.content.replace(
                "```json", "").replace("```", ""))
        except json.JSONDecodeError:
            logging.error(f"json can't decode '{chat.choices[0].message.content}'")

        return resp