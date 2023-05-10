from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


get_number = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Telefon raqamni jo'natish", request_contact=True)
        ]
    ],
    resize_keyboard=True
)


start = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📝 Boshlash")
        ]
    ],
    resize_keyboard=True
)

yes_no = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="✅ Ha"),
            KeyboardButton(text="❌ Yo'q")
        ]
    ],
    resize_keyboard=True
)

