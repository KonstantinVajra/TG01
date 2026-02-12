import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config import TOKEN, WEATHER_API_KEY
import requests
from config import WEATHER_API_KEY

bot = Bot(token=TOKEN)
dp = Dispatcher()

CITY = "Varadero"


def get_weather():
    url = "https://api.weatherapi.com/v1/current.json"
    params = {
        "key": WEATHER_API_KEY,
        "q": CITY,
        "lang": "ru"
    }

    r = requests.get(url, params=params, timeout=10)
    data = r.json()

    # если пришла ошибка — вернём понятный текст
    if "error" in data:
        return None, None, f"Ошибка WeatherAPI: {data['error'].get('message', 'unknown error')}"

    # если почему-то нет current — тоже не падаем
    if "current" not in data:
        return None, None, f"Неожиданный ответ API: {data}"

    temp = data["current"]["temp_c"]
    feels = data["current"]["feelslike_c"]
    desc = data["current"]["condition"]["text"]

    return temp, feels, desc



#  start
# start
@dp.message(CommandStart())
async def start(message: Message):

    await message.answer(
        "🌴 Добро пожаловать!\n\n"
        "Я бот прогноза погоды для Варадеро (Куба) ☀️\n\n"
        "С моей помощью ты можешь узнать текущую погоду.\n\n"
        "Доступные команды:\n"
        "🌡 /weather — узнать погоду\n"
        "ℹ️ /help — помощь"
    )


#  help
# help
@dp.message(Command("help"))
async def help(message: Message):

    await message.answer(
        "ℹ️ Список команд:\n\n"
        "🌴 /start — приветствие\n"
        "🌡 /weather — текущая погода в Варадеро\n"
        "ℹ️ /help — показать список команд\n\n"
        "Просто нажми /weather, чтобы узнать погоду."
    )


#  weather
# weather
@dp.message(Command("weather"))
async def weather(message: Message):

    temp, feels, desc = get_weather()

    if temp is None:
        await message.answer(desc)
        return

    await message.answer(
        f"🌴 Погода в Варадеро:\n\n"
        f"🌡 Температура: {temp}°C\n"
        f"🤔 Ощущается как: {feels}°C\n"
        f"☁️ Описание: {desc}"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
