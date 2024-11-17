import httpx
from openai import AsyncOpenAI

from config import OPENAI, PROXIES


class AsyncOpenAIChatAgent(object):
    """Агент для чатов с OpenAI."""

    def __init__(self, api_key, proxies=None, img_model=None, text_model=None, img_size='1024x1024', img_quality='standard'):
        """Инициализация агента для чатов с OpenAI.

        Args:
            api_key (str): API ключ для OpenAI.
            model (str): model.
            organization (str): Название организации.
        """

        self.api_key = api_key
        self.proxies = dict(proxies)
        self.endpoint = 'https://api.openai.com/v1/chat/completions'
        self.text_model = text_model
        self.img_model = img_model
        self.img_size = img_size
        self.img_quality = img_quality

    async def chat(self, messages, model=None, dev=False):
        """Чат с OpenAI GPT.

        Args:
            messages (list): Список сообщений.
            model: GPT-model.

        Returns:
            str: Ответ OpenAI.

        Raises:
            Exception: Если запрос к OpenAI не удался.
        """

        if dev: print(self.proxies)

        client = AsyncOpenAI(
            api_key=self.api_key,
            http_client=httpx.AsyncClient(proxies=self.proxies),
        )

        if isinstance(messages, str):
            messages = [{'role': 'user', 'content': messages}]

        if not model:
            model = self.text_model

        if not model:
            model = 'gpt-3.5-turbo'

        if dev: print(messages)
        completion = await client.chat.completions.create(
            model=model,
            messages=messages
        )

        return completion.choices[0].message.content


gpt = AsyncOpenAIChatAgent(OPENAI, proxies=PROXIES)