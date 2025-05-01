import os
from typing import List
from libs.rag_lib.interfaces import ChatProvider
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
from app.config import settings


class OpenAIChatProvider(ChatProvider):
    def __init__(
        self,
        model_name: str = "gpt-4o-mini",
        api_key: str = None,
        temperature: float = 0.0,
    ):
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key or settings.OPENAI_API_KEY
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
        )

    def chat(self, prompt: str, context: List[str]) -> str:
        # HumanMessage와 context 조합
        messages = [HumanMessage(content=ctx) for ctx in context]
        messages.append(HumanMessage(content=prompt))
        response = self.llm(messages)
        return response.content
