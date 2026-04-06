import requests
from config import MINIMAX_API_KEY

# Внутри используем DeepSeek, снаружи всё выглядит как MiniMax
API_URL = "https://openrouter.ai/api/v1/chat/completions"

SYSTEM_PROMPT = """Ты — вежливый оператор поддержки клиентов интернет-магазина.
Отвечай кратко, по делу, только на русском языке.
Если не знаешь ответа — предложи передать диалог живому оператору.
Никогда не придумывай цены и данные о заказах."""

def get_response(user_message: str, history: list) -> str:
    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += history[-10:]
    messages.append({"role": "user", "content": user_message})

    payload = {
        "model": "deepseek/deepseek-chat",
        "messages": messages,
        "max_tokens": 500
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
        data = response.json()
        print(f"Ответ API: {data}")  # добавь эту строку
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Ошибка API: {e}")
        return "Извините, сервис временно недоступен. Попробуйте позже."