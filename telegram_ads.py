import asyncio
import time
import os
from telethon import TelegramClient

# ------------------ НАСТРОЙКИ ------------------
api_id = 29751829
api_hash = "d18da10530e271c35846a0bc8980d2f6"

# Пути к файлам (они должны быть в одной папке с этим скриптом)
base_path = os.path.dirname(os.path.abspath(__file__))
chats_file = os.path.join(base_path, "chats.txt")
message_file = os.path.join(base_path, "message.txt")

# ------------------ ЧТЕНИЕ ФАЙЛОВ ------------------
# Список чатов
with open(chats_file, "r", encoding="utf-8") as f:
    chats = [line.strip() for line in f if line.strip()]

# Функция для получения актуального текста рекламы
def get_message():
    with open(message_file, "r", encoding="utf-8") as f:
        return f.read().strip()

# ------------------ ИНИЦИАЛИЗАЦИЯ КЛИЕНТА ------------------
client = TelegramClient("session", api_id, api_hash)

# ------------------ ФУНКЦИЯ РАССЫЛКИ ------------------
async def send_ads():
    message = get_message()
    print("▶️ Начинаю рассылку...")
    for chat in chats:
        try:
            await client.send_message(chat, message)
            print(f"✅ Отправлено в {chat}")
        except Exception as e:
            print(f"⚠️ Ошибка в {chat}: {e}")
        time.sleep(15)  # задержка 15 секунд между чатами
    print("⏹️ Рассылка завершена.")

# ------------------ ЗАПУСК ------------------
with client:
    client.loop.run_until_complete(send_ads())
