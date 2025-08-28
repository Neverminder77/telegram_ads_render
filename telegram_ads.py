import asyncio
import os
import time
from telethon import TelegramClient
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# ------------------ НАСТРОЙКИ ------------------
api_id = 29751829
api_hash = "d18da10530e271c35846a0bc8980d2f6"

# Пути к файлам
base_path = os.path.dirname(os.path.abspath(__file__))
chats_file = os.path.join(base_path, "chats.txt")
message_file = os.path.join(base_path, "message.txt")
session_file = os.path.join(base_path, "session.session")  # обязательно файл сессии

# ------------------ ЧТЕНИЕ ЧАТОВ ------------------
with open(chats_file, "r", encoding="utf-8") as f:
    chats = [line.strip() for line in f if line.strip()]

# ------------------ ФУНКЦИЯ ДЛЯ ТЕКСТА ------------------
def get_message():
    with open(message_file, "r", encoding="utf-8") as f:
        return f.read().strip()

# ------------------ ИНИЦИАЛИЗАЦИЯ КЛИЕНТА ------------------
# Важно: не используем input(), используем только файл сессии
client = TelegramClient(session_file, api_id, api_hash)

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

# ------------------ АВТОМАТИЧЕСКИЙ ЗАПУСК ------------------
async def main():
    await client.start()  # Telethon использует файл сессии, не спрашивая телефон
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_ads, "interval", hours=1)  # запуск каждый час
    scheduler.start()
    print("⏳ Скрипт запущен. Рассылка будет раз в час.")
    await asyncio.Event().wait()  # держим скрипт в работе

# ------------------ ЗАПУСК ------------------
if __name__ == "__main__":
    asyncio.run(main())
