import time
import uuid
from PIL import Image, ImageDraw, ImageFont
import asyncio
from telebot.async_telebot import AsyncTeleBot
from telebot import asyncio_filters
from telebot.asyncio_handler_backends import State, StatesGroup
from telebot.asyncio_storage import StateMemoryStorage

# Add your bot token here
API_TOKEN = "7184475195:AAEIWVRtadEfIcJNIDJN5sOtjEs9GQMBQz4"
bot = AsyncTeleBot(API_TOKEN)

# configuration
font_size = 110
font_color = (255, 255, 255)

# bot state storage and filter setup
state_storage = StateMemoryStorage()
bot.add_custom_filter(asyncio_filters.StateFilter(bot))


class MyStates(StatesGroup):
    name = State()


# start command handler
@bot.message_handler(commands=["start"])
async def start(message):
    chat_id = message.chat.id
    await bot.reply_to(message, f"ℹ️ Enter a name...")
    await bot.set_state(chat_id, MyStates.name, chat_id)


@bot.message_handler(state=MyStates.name)
async def put_name(message):
    text = message.text
    print(int(time.time()), text, "\n")
    text = text.replace(" ", "\n")
    fileName = uuid.uuid4()

    im = Image.open("id2.png")
    draw = ImageDraw.Draw(im)
    unicode_font = ImageFont.truetype("cairo.ttf", font_size)
    draw.text(
        (67, 190),
        text,
        font=unicode_font,
        fill=font_color,
        stroke_width=5,
        stroke_fill="#000",
    )
    im.save(f"gens/{fileName}.png")
    await bot.send_photo(message.chat.id, open(f"gens/{fileName}.png", "rb"))


async def main():
    polling_task = asyncio.create_task(bot.infinity_polling())
    await asyncio.gather(
        polling_task,
    )


if __name__ == "__main__":
    asyncio.run(main())
