from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher.filters import Regexp

from keyboards.inline.alluserinline import family, sud, rus, word, exel, edu, soha
from keyboards.default.phone import get_number, start, yes_no
from states.anketa import UserState

from data.config import ADMINS
from loader import dp, bot



@dp.message_handler(commands="start", user_id=ADMINS)
async def hi_admin(message: types.message):
    await message.answer(f"Assalamu hurmatli admin")
# Assalamu alaykum Asnan korxonasi hr botiga hush kelibsiz!
#
# Iltimos sizga aloqaga chiqishimiz uchun savollarning barchasiga aniq javob bering!
#
# Anketa to'ldirish uchun Boshlash tugmasini bosing

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Assalamu alaykum HR botiga hush kelibsiz!\n\n"
                         f"Iltimos sizga aloqaga chiqishimiz uchun savollarning barchasiga aniq javob bering!\n\n"
                         f"Anketa to'ldirish uchun Boshlash tugmasini bosing!"
                         ,reply_markup=start)

@dp.message_handler(text="📝 Boshlash")
async def bot_boshla(message:types.Message):
    await message.answer("To'liq ismingizni kiriting\n\nMasalan: <b>Saydullo Xaydarov</b>", reply_markup=ReplyKeyboardRemove())
    await UserState.name.set()

@dp.message_handler(state=UserState.name)
async def answer_fullname(message: types.Message, state: FSMContext):
    name = message.text
    if name.isdigit():
        await message.answer("Iltimos tekshirib qayta kiriting!")
    else:
        await state.update_data(
            {"name": name}
        )
        await message.answer("Tug'ulgan yilingizni kiriting! (1970-2010)")
        await UserState.year.set()

@dp.message_handler(state=UserState.year)
async def answer_year(message: types.Message, state: FSMContext):
   # year =int(message.text)
    try:
        year = int(message.text)
        if year >= 1970 and year <= 2010:
            await state.update_data(
                {"year": year}
                )
            await message.answer("Telefon raqam kiriting!\n\nMasalan: <b>+998XXXXXXXXX</b>")
            await UserState.phone.set()
        else:
            await message.answer("iltimos tekshirib qayta kiriting")
    except Exception:
        await message.answer("iltimos tekshirib qayta kiriting")

@dp.message_handler(state=UserState.phone)
async def answer_phone(message: types.Message, state: FSMContext):
    phone = message.text
    try:
        if phone.startswith("+998") and len(phone) == 13 and int(message.text):
            await state.update_data(
                {"phone": phone}
            )
            await message.answer("Telefon raqazmingizni kiriting\n\n<b>+998XXXXXXXXX</b>")
            await UserState.sphone.set()
        else:
            await message.answer("Iltimos tekshirib qayta kiriting")
    except Exception:
        await message.answer("Iltimos tekshirib qayta kiriting")

@dp.message_handler(state=UserState.sphone)
async def answer_sphone(message: types.Message, state:FSMContext):
    sphone = message.text
    try:
        if sphone.startswith("+998") and len(sphone) == 13 and int(message.text):
            await state.update_data(
                {"sphone": sphone}
            )
            await message.answer("Yo'nalish turini tanlang!", reply_markup=soha)
            await UserState.job.set()
        else:
            await message.answer("Iltimos tekshirib qayta kiriting")
    except Exception:
        await message.answer("Iltimos tekshirib qayta kiriting")

@dp.callback_query_handler(state=UserState.job)
async def enter_job(call: types.CallbackQuery, state: FSMContext):
    job = call.data
    await state.update_data(
        {'job': job}
    )
    await call.message.delete()
    await call.message.answer("Yashash manzilingizni kiriting!\n\nMasalan: <b>Asaka tumani, Mirzaobod MFY, 55 uy</b>")
    await UserState.region.set()

@dp.message_handler(state=UserState.region)
async def enter_region(message:types.Message, state:FSMContext):
    region = message.text
    if region.isdigit():
        await message.answer("iltimos tekshirib qayta kiriting")
    else:
        await state.update_data(
            {"region":region}
        )
        await message.answer("Viloyatingizni kiriting!\n\nMasalan: <b>Andijon</b>")
        await UserState.address.set()
@dp.message_handler(state=UserState.address)
async def enter_address(message:types.Message, state:FSMContext):
    address = message.text
    await state.update_data(
        {"address": address}
    )
    await message.answer("Millatingizni kiriting!")
    await UserState.nation.set()
@dp.message_handler(state=UserState.nation)
async def enter_nation(message:types.Message, state:FSMContext):
    nation = message.text
    await state.update_data(
        {"nation":nation}
    )
    await message.answer("Oilaviy holatingiz", reply_markup=family)
    await UserState.family.set()

@dp.callback_query_handler(state=UserState.family)
async def enter_family(call: types.CallbackQuery, state: FSMContext):
    family = call.data
    await state.update_data(
        {'family': family}
    )
    await call.message.delete()
    await call.message.answer("Ish tajribangiz bormi ?")
    await UserState.jobexperience.set()

@dp.message_handler(state=UserState.jobexperience)
async def enter_jobex(message:types.Message, state:FSMContext):
    jobexperience = message.text
    await state.update_data(
        {"jobexperience":jobexperience}
    )
    await message.answer("Oldin qayerda ishlagansiz ?")
    await UserState.oldjob.set()

@dp.message_handler(state=UserState.oldjob)
async def enter_oldjob(message:types.Message, state:FSMContext):
    oldjob = message.text
    await state.update_data(
        {"oldjob":oldjob}
    )
    await message.answer("Malumotingiz qanday ?", reply_markup=edu)
    await UserState.edu.set()

@dp.callback_query_handler(state=UserState.edu)
async def enter_edu(call:types.CallbackQuery, state: FSMContext):
    edu = call.data
    await state.update_data(
        {'edu': edu}
    )
    await call.message.delete()
    await call.message.answer("Ushbu vakansiyadan qancha maosh kutyapsiz ?\n\nMasalan: <b>2'000'000 so'm</b>")
    await UserState.salary.set()

@dp.message_handler(state=UserState.salary)
async def enter_salary(message:types.Message, state:FSMContext):
    salary = message.text
    await state.update_data(
        {"salary":salary}
    )
    await message.answer("Qancha vaqt ishlamoqchisiz ?")
    await UserState.time.set()

@dp.message_handler(state=UserState.time)
async def enter_time(message:types.Message, state:FSMContext):
    time = message.text
    await state.update_data(
        {"time": time}
    )
    await message.answer("Sudlanganmisiz ?", reply_markup=sud)
    await UserState.sud.set()

@dp.callback_query_handler(state=UserState.sud)
async def enter_sud(call:types.CallbackQuery, state: FSMContext):
    sud = call.data
    await state.update_data(
        {'sud': sud}
    )
    await call.message.delete()
    await call.message.answer("<b>Rus tili</b>dan darajangiz qanday ?", reply_markup=rus)
    await UserState.rus.set()

@dp.callback_query_handler(state=UserState.rus)
async def enter_rus(call:types.CallbackQuery, state:FSMContext):
    rus = call.data
    await state.update_data(
        {"rus":rus}
    )
    await call.message.delete()
    await call.message.answer("<b>Word</b> dasturida ishlay olish darajangiz.", reply_markup=word)
    await UserState.word.set()

@dp.callback_query_handler(state=UserState.word)
async def enter_word(call:types.CallbackQuery, state:FSMContext):
    word = call.data
    await state.update_data(
        {"word":word}
    )
    await call.message.delete()
    await call.message.answer("<b>Exel</b> dasturida ishlay olish darajangiz.", reply_markup=exel)
    await UserState.exel.set()

@dp.callback_query_handler(state=UserState.exel)
async def enter_exel(call:types.CallbackQuery, state:FSMContext):
    exel = call.data
    await state.update_data(
        {"exel":exel}
    )
    await call.message.delete()
    await call.message.answer("Biz haqimizda qayerdan eshitdingiz ?")
    await UserState.find.set()

@dp.message_handler(state=UserState.find)
async def enter_find(message:types.Message, state:FSMContext):
    find = message.text
    await state.update_data(
        {"find":find}
    )
    await message.answer("Iltimos arizani yakunlash uchun rasm yuboring!")
    await UserState.photo.set()

@dp.message_handler(state=UserState, content_types=types.ContentType.PHOTO)
async def enter_photo(message:types.Message, state:FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(
        {"photo":photo}
    )

    data = await state.get_data()
    photo = f"{data['photo']}"
    msg = "<b>Quyidagi ma'lumotlar qabul qilindi</b>\n\n"
    msg += f"1. Ismingiz ➖ {data['name']}\n\n"
    msg += f"2. Yilingiz ➖ {data['year']}\n\n"
    msg += f"3. Telefon ➖ {data['phone']}\n\n"
    msg += f"4. Qo'shimcha tel➖ {data['sphone']}\n\n"
    msg += f"5. Tanlagan ishingiz ➖ {data['job']}\n\n"
    msg += f"6. Viloyati ➖ {data['region']}\n\n"
    msg += f"7. Manzilingiz ➖ {data['address']}\n\n"
    msg += f"8. Millatingiz ➖ {data['nation']}\n\n"
    msg += f"9. Holatingiz ➖ {data['family']}\n\n"
    msg += f"10. Tajribangiz ➖ {data['jobexperience']}\n\n"
    msg += f"11. Oldingi ishingiz ➖ {data['oldjob']}\n\n"
    msg += f"12. Ma'lumotingiz ➖ {data['edu']}\n\n"
    msg += f"13. Maosh ➖ {data['salary']}\n\n"
    msg += f"14. Ishlash vaqti ➖ {data['time']}\n\n"
    msg += f"15. Sudlanganmisiz ➖ {data['sud']}\n\n"
    msg += f"16. Rus tili darajangiz ➖ {data['rus']}\n\n"
    msg += f"17. Word dasturi ➖ {data['word']}\n\n"
    msg += f"18. Exel dasturi ➖ {data['exel']}\n\n"
    msg += f"19. Qanday topdingiz ➖ {data['find']}\n\n"

    await message.answer_photo(photo= photo, caption=msg)
    await message.answer(f"Sizning anketangiz muvaffaqiyatli to'ldirildi va yuborishga tayyor, Anketangizni tasdiqlaysizmi?\n<b>Ha tugmasini bosing</b>\n", reply_markup=yes_no)
    await UserState.check.set()

@dp.message_handler(state = UserState.check)
async def fiveteen(message: types.Message, state: FSMContext):
    matn = message.text
    if matn == "✅ Ha":

        data = await state.get_data()
        photo = f"{data['photo']}"
        msg = "<b>Quyidagi ma'lumotlar qabul qilindi</b>\n\n"
        msg += f"1. Ismi ➖ {data['name']}\n\n"
        msg += f"2. Yili ➖ {data['year']}\n\n"
        msg += f"3. Telefon ➖ {data['phone']}\n\n"
        msg += f"4. Qo'shimcha tel ➖ {data['sphone']}\n\n"
        msg += f"5. Tanlagan ish turi ➖ {data['job']}\n\n"
        msg += f"6. Viloyati ➖ {data['region']}\n\n"
        msg += f"7. Manzili➖ {data['address']}\n\n"
        msg += f"8. Millati ➖ {data['nation']}\n\n"
        msg += f"9. Holati ➖ {data['family']}\n\n"
        msg += f"10. Tajribasi ➖ {data['jobexperience']}\n\n"
        msg += f"11. Oldingi ish joyi ➖ {data['oldjob']}\n\n"
        msg += f"12. Ma'lumoti ➖ {data['edu']}\n\n"
        msg += f"13. Maosh ➖ {data['salary']}\n\n"
        msg += f"14. Ishlash vaqti ➖ {data['time']}\n\n"
        msg += f"15. Sudlanganmi ➖ {data['sud']}\n\n"
        msg += f"16. Rus tili darajasi ➖ {data['rus']}\n\n"
        msg += f"17. Word dasturi ➖ {data['word']}\n\n"
        msg += f"18. Exel dasturi ➖ {data['exel']}\n\n"
        msg += f"19. Qanday topdi ➖ {data['find']}\n\n"
        msg += f"20. Username ➖ @{message.from_user.username}"
        await bot.send_photo(chat_id=-897662757, photo=photo, caption=msg)
        await message.answer("<b>Anketangiz muvaffaqiyatli yuborildi</b>\n\nBiz anketangizni ko'rib chiqamiz va bizga mos kelsangiz siz bilan bog'lanamiz!\n\n"
                             "Bizga mos kelsangiz 20 ish kunida bog'lanamiz\n20 ish kunida bog'lanmasak boshqa ish qidirishingiz mumkin!", reply_markup=start)
    elif matn == "❌ Yo'q":
        await message.answer("Elon bekor qilindi\n\nBoshqatdan boshlashingiz mumkin!", reply_markup=start)


