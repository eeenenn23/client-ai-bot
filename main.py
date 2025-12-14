import os
import asyncio
import logging
import aiohttp

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_TOKEN = os.getenv("GROQ_TOKEN")

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot=bot)

SYSTEM_PROMPT = """
Ты автоответчик для клиентов.
Отвечай кратко и по делу.
Если не знаешь — уточни.
"""

@dp.message(Command("start"))
async def start(m: types.Message):
    await m.answer("👋 Здравствуйте! Напишите ваш вопрос.")

@dp.message()
async def chat(m: types.Message):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_TOKEN}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-8b-instant",
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": m.text}
                    ],
                    "max_tokens": 150
                }
            ) as r:
                data = await r.json()

        await m.answer(data["choices"][0]["message"]["content"])

    except Exception as e:
        logging.error(e)
        await m.answer("⚠️ Временно не могу ответить.")

async def main():
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
