from openai import OpenAI

class Chat:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
    
    def chat_completion(
        self,
        messages: list,
        model: str,
        temperature: float = 0.70,
        top_p: float = 0.70,
        frequency_penalty: float = 0.00,
        presence_penalty: float = 0.00):
        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            top_p=top_p,
            frequency_penalty=frequency_penalty,
            presence_penalty=presence_penalty,
            stream=True
        )
        return response
    
    def reason_completion(self, messages: list):
        client = OpenAI(api_key=self.api_key, base_url=self.base_url)
        response = client.chat.completions.create(
            model="deepseek-reasoner",
            messages=messages,
            stream=True
        )
        return response
