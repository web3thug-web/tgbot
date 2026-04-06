import json
from aiogram import Router
from aiogram.types import Message
from minimax import get_response
from database import save_dialog

router = Router()

# Загружаем датасет один раз при запуске
with open("intents.json", encoding="utf-8") as f:
    intents_data = json.load(f)

# Словарь для хранения истории диалога каждого пользователя
dialog_history = {}

def detect_intent(text: str):
    """Ищем совпадение фразы с датасетом"""
    text_lower = text.lower()
    for intent in intents_data["intents"]:
        for pattern in intent["patterns"]:
            if pattern.lower() in text_lower:
                # Нашли совпадение — возвращаем тег и готовый ответ
                return intent["tag"], intent["response"]
    # Совпадений нет — передаём в MiniMax
    return "unknown", ""

@router.message()
async def handle_message(message: Message):
    user_id = message.from_user.id
    user_text = message.text

    # Проверяем что сообщение не пустое
    if not user_text:
        await message.answer("Пожалуйста, отправьте текстовое сообщение.")
        return

    # Определяем интент
    intent_tag, intent_response = detect_intent(user_text)

    # Случай 1: пользователь просит оператора
    if intent_tag == "transfer_operator":
        response = intent_response
        await message.answer(response)
        save_dialog(user_id, user_text, response, intent_tag)
        return

    # Случай 2: интент найден в датасете
    if intent_tag != "unknown":
        response = intent_response

    # Случай 3: интент не найден — спрашиваем у MiniMax
    else:
        history = dialog_history.get(user_id, [])
        response = get_response(user_text, history)

        # Сохраняем в историю для следующих сообщений
        dialog_history.setdefault(user_id, []).append(
            {"role": "user", "content": user_text}
        )
        dialog_history[user_id].append(
            {"role": "assistant", "content": response}
        )

    await message.answer(response)
    save_dialog(user_id, user_text, response, intent_tag)