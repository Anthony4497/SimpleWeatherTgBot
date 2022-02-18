import requests
import datetime
from confiG import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши мне название города и я пришлю сводку погоды!")


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Морось \U00002614",
        "Thunderstorm": "Гром и молнии \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric")
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        min_temp = data["main"]["temp_min"]
        max_temp = data["main"]["temp_max"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

        coord_lat = data["coord"]["lat"]
        coord_lon = data["coord"]["lon"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])

        await message.reply(f"Дата/время: {datetime.datetime.now().strftime('%d-%m-%Y %H:%M')} \n"
              f"Координаты: широта {coord_lat}, долгота: {coord_lon}\n"
              f"Погода в городе: {city}\nТемпература: {cur_weather}C°. Чувствуется как {feels_like} {wd}\n"
              f"Минимальная температура в городе: {min_temp}.\nМаксимальная температура: {max_temp}\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
              f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\n"
              f"Продолжительность дня: {length_of_the_day}\n"
              )

    except:
        await message.reply("\U00002620 Название города введено не корректно \U00002620")


if __name__ == '__main__':
    executor.start_polling(dp)