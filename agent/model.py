from typing import Tuple
from openai import OpenAI


prompt = ("Ты мастер игры в ДнД, который должен отыгрывать монстров и решать, что им делать в данный момент."
          "Ты получаешь описание карты, на которой происходит сражение в формате json, и кто сейчас делает ход в поле current_turn."
          "Также ты получаешь дополнительную информацию об игре"
          "Опиши одно конкретное действия персонажа в данный момент. Если необходимо бросить кубик, придумай результат броска.")

class ChatGPTAPI:
    def __init__(self) -> None:
        super().__init__()
        self.api_key = 'sk-aitunnel-8oS8YFVGcwcUIi0vdBQqstKzT9tBXh92' #"sk-cYNYKOlRJsocapn7PJDqUpBUlhWbZwdm" #os.environ['CHATGPT_API_KEY']
        self.client = OpenAI(
            api_key=f"{self.api_key}",
            base_url='https://api.aitunnel.ru/v1/'#"https://api.proxyapi.ru/openai/v1",
        )

    def refresh_token(self) -> None:
        raise Exception("Don't call refresh_token() for ChatGPT")

    def call_api(self, query: str) -> Tuple[str, str]:
        print("Call api")
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.5
        )
        return response.choices[0].message.content