import json

from openai import OpenAI


action_prompt = ("Ты мастер игры в ДнД, который должен отыгрывать монстров и решать, что им делать в данный момент."
          "Ты получаешь описание карты, на которой происходит сражение в формате json, и кто сейчас делает ход в поле current_turn."
          "Также ты получаешь дополнительную информацию об игре"
          "Опиши одно конкретное действия персонажа в данный момент. Если необходимо бросить кубик, придумай результат броска.")

update_prompt = ("Тебе дается json с описанием карты для битвы в ДнД и текстовое описание действия, которое произошло."
                 "Сгнерируй обновленный json с новыми параметрами, которые соответствуют описанию (обнови положение персонажей, количество их здоровья и т.д.)")

class ChatGPTAPI:
    def __init__(self) -> None:
        super().__init__()
        self.api_key = 'sk-aitunnel-8oS8YFVGcwcUIi0vdBQqstKzT9tBXh92'
        self.client = OpenAI(
            api_key=f"{self.api_key}",
            base_url='https://api.aitunnel.ru/v1/'
        )

    def refresh_token(self) -> None:
        raise Exception("Don't call refresh_token() for ChatGPT")

    def generate_action(self, query: str) -> str:

        print([
        {"role": "system", "content": action_prompt},
        {"role": "user", "content": query}
        ])
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": action_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.5
        )
        return response.choices[0].message.content

    def update_map(self, map_info: dict, action: str):
        query = str(map_info) + "\n\n" + action
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": update_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.05,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

