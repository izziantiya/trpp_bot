import os
import json
import random
import string
import urllib.request as url
import xml.etree.ElementTree as ET

import uvicorn
import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll
from vk_api.utils import get_random_id


{"command": "start"}

vk_session = vk_api.VkApi(
    token=os.getenv("TOKEN")
)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()


def get_button(label, color, payload=""):
    return {
        "action": {"type": "text", "payload": json.dumps(payload), "label": label},
        "color": color,
    }


keyboard = {
    "one_time": True,
    "buttons": [
        [get_button(label="Виселица", color="primary")],
        [get_button(label="Гороскоп", color="primary")],
        [get_button(label="Камень-Ножницы-Бумага", color="primary")],
    ],
}


keyboard_hangman = {
    "one_time": True,
    "buttons": [
        [
            get_button(label="🇷🇺", color="positive"),
            get_button(label="🇬🇧", color="negative"),
        ]
    ],
}


keyboard_horoscope = {
    "one_time": True,
    "buttons": [
        [
            get_button(label="Вчера", color="primary"),
            get_button(label="Сегодня", color="primary"),
            get_button(label="Завтра", color="primary"),
            get_button(label="Послезавтра", color="primary"),
        ]
    ],
}

keyboard_play_2 = {
    "one_time": True,
    "buttons": [
        [
            get_button(label="Камень", color="primary"),
            get_button(label="Ножницы", color="primary"),
            get_button(label="Бумага", color="primary"),
        ]
    ],
}


def get_valid_word(words):
    word = random.choice(words)  # случайным образом выбирает что-то из списка
    while "-" in word or " " in word:
        word = random.choice(words)

    return word.upper()


def hangman():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            if event.text == "🇷🇺":
                words = [
                    "машина",
                    "самолёт",
                    "яблоко",
                    "банан",
                    "вишня",
                    "автострада",
                    "бензин",
                    "инопланетянин",
                    "самолет",
                    "библиотека",
                    "шайба",
                    "олимпиада",
                    "зима",
                    "океан",
                ]
                alphabet = {
                    "А",
                    "Б",
                    "В",
                    "Г",
                    "Д",
                    "Е",
                    "Ё",
                    "Ж",
                    "З",
                    "И",
                    "Й",
                    "К",
                    "Л",
                    "М",
                    "Н",
                    "О",
                    "П",
                    "Р",
                    "С",
                    "Т",
                    "У",
                    "Ф",
                    "Х",
                    "Ц",
                    "Ч",
                    "Ш",
                    "Щ",
                    "Ъ",
                    "Ы",
                    "Ь",
                    "Э",
                    "Ю",
                    "Я",
                }
            else:
                words = ["aback", "abaft", "abandoned", "abashed"]
                alphabet = set(string.ascii_uppercase)  # Алфавит (Англ)
            word = get_valid_word(words)
            word_letters = set(word)  # буквы в слове
            used_letters = set()  # Использованные
            lives = 6
            word_list = [letter if letter in used_letters else "-" for letter in word]
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message="Текущий прогресс: "
                + " ".join(word_list)
                + "\nВведите букву или слово:",
            )
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                    user_letter = event.text.upper()

                    if user_letter in alphabet - used_letters:
                        used_letters.add(user_letter)
                        if user_letter in word_letters:
                            word_letters.remove(user_letter)
                            print("")
                        else:
                            lives = lives - 1  # Вычет жизни при ошибке
                            vk.messages.send(
                                user_id=event.user_id,
                                random_id=get_random_id(),
                                message="\nУвы, буквы "
                                + user_letter
                                + " нет в этом слове.",
                            )
                    elif user_letter in used_letters:
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message="\nВы уже использовали эту букву. Попробуйте другую.",
                        )
                    elif user_letter == word:
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            keyboard=json.dumps(keyboard, ensure_ascii=True),
                            message="УРА! Вы угадали слово " + word + "!!!",
                        )
                        return
                    else:
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message="\nЭто не буква.",
                        )
                    if lives == 0:
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            keyboard=json.dumps(keyboard, ensure_ascii=True),
                            message="Вы умерли, извините. Слово было " + word,
                        )
                        return
                    else:
                        word_list = [
                            letter if letter in used_letters else "-" for letter in word
                        ]
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message="У тебя осталось "
                            + str(lives)
                            + " жизней. Использованные буквы: "
                            + " ".join(used_letters),
                        )
                        # текущее слово (например Х - О С Т)
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message="Текущий прогресс: "
                            + " ".join(word_list)
                            + "\nВведите букву или слово:",
                        )


def horoscope():
    response = url.urlopen("https://ignio.com/r/export/win/xml/daily/com.xml")
    tree = ET.parse(response)
    root = tree.getroot()

    horoscope = {}
    day = ""

    for zodiak in root:
        result = {}
        for day in zodiak:
            result.update({day.tag: day.text})
        horoscope.update({zodiak.tag: result})

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            event.text = event.text.lower()
            if event.text == "вчера":
                day = "yesterday"
            elif event.text == "сегодня":
                day = "today"
            elif event.text == "завтра":
                day = "tomorrow"
            elif event.text == "послезавтра":
                day = "tomorrow02"
            else:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=json.dumps(keyboard_horoscope, ensure_ascii=True),
                    message="К сожалению, на эту дату еще нет гороскопа😨\nПроверьте, правильно ли вы ввели команду",
                )
                continue
            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                message="Напишите интересующий вас знак зодиака",
            )
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
                    event.text = event.text.lower()
                    if event.text == "овен":
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            keyboard=json.dumps(keyboard, ensure_ascii=True),
                            message=horoscope.get("aries").get(day),
                        )
                        return
                    elif event.text == "телец":
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            keyboard=json.dumps(keyboard, ensure_ascii=True),
                            message=horoscope.get("taurus").get(day),
                        )
                        return
                    elif event.text == "близнецы":
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            keyboard=json.dumps(keyboard, ensure_ascii=True),
                            message=horoscope.get("gemini").get(day),
                        )
                        return
                    elif event.text == "рак":
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            keyboard=json.dumps(keyboard, ensure_ascii=True),
                            message=horoscope.get("cancer").get(day),
                        )
                        return
                    elif event.text == "лев":
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            keyboard=json.dumps(keyboard, ensure_ascii=True),
                            message=horoscope.get("leo").get(day),
                        )
                        return
                    elif event.text == "дева":
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            keyboard=json.dumps(keyboard, ensure_ascii=True),
                            message=horoscope.get("virgo").get(day),
                        )
                        return
                    elif event.text == "весы":
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            keyboard=json.dumps(keyboard, ensure_ascii=True),
                            message=horoscope.get("libra").get(day),
                        )
                        return
                    elif event.text == "скорпион":
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            keyboard=json.dumps(keyboard, ensure_ascii=True),
                            message=horoscope.get("scorpio").get(day),
                        )
                        return
                    elif event.text == "стрелец":
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            keyboard=json.dumps(keyboard, ensure_ascii=True),
                            message=horoscope.get("sagittarius").get(day),
                        )
                        return
                    elif event.text == "козерог":
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            keyboard=json.dumps(keyboard, ensure_ascii=True),
                            message=horoscope.get("capricorn").get(day),
                        )
                        return
                    elif event.text == "водолей":
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            keyboard=json.dumps(keyboard, ensure_ascii=True),
                            message=horoscope.get("aquarius").get(day),
                        )
                        return
                    elif event.text == "рыбы":
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            keyboard=json.dumps(keyboard, ensure_ascii=True),
                            message=horoscope.get("pisces").get(day),
                        )
                        return
                    else:
                        vk.messages.send(
                            user_id=event.user_id,
                            random_id=get_random_id(),
                            message="Звезды не сошлись, такого знака зодиака нет",
                        )
                        continue


def is_win(player, opponent):
    # return true если игрок победил
    if (
        (player == "К" and opponent == "Н")
        or (player == "Н" and opponent == "Б")
        or (player == "Б" and opponent == "К")
    ):
        return True


def play_2():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            event.text = event.text.upper()
            event.text = event.text[:1]
            computer = random.choice(["К", "Н", "Б"])
            if event.text == computer:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=json.dumps(keyboard, ensure_ascii=True),
                    message="О как. Я не мог такого предположить,но... Наши мысли сходятся",
                )
                return
            if is_win(event.text, computer):
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=json.dumps(keyboard, ensure_ascii=True),
                    message="Невозможно... Ты победил",
                )
                return

            vk.messages.send(
                user_id=event.user_id,
                random_id=get_random_id(),
                keyboard=json.dumps(keyboard, ensure_ascii=True),
                message="Это было просто. Я оказался сильнее, как всегда.",
            )
            return


async def main():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            event.text = event.text.lower()
            print("New from {}, text = {}".format(event.user_id, event.text))

            if (
                event.text == "начать" or event.text == "привет"
            ):  # Если написали заданную фразу
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=json.dumps(keyboard, ensure_ascii=True),
                    message="😀Привет❤, "
                    + vk.users.get(user_id=event.user_id)[0]["first_name"]
                    + ", я чат-бот, который тебе поможет."
                    + " Я могу:\n1) Поиграть с тобой в виселицу\n2) Показать гороскоп\n3)Поиграть в Камень-Ножницы-Бумага\n"
                    + "\nБот принимает любой регистр сообщений",
                )
            elif event.text == "помощь":
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=json.dumps(keyboard, ensure_ascii=True),
                    message=" Я могу:\n1) Поиграть с тобой в виселицу\n2) Показать гороскоп\n"
                    + "\nБот принимает любой регистр сообщений",
                )
            elif event.text == "виселица":
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=json.dumps(keyboard_hangman, ensure_ascii=True),
                    message="Выберите, какие слова хотите угадывать",
                )
                hangman()
            elif event.text == "гороскоп":
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=json.dumps(keyboard_horoscope, ensure_ascii=True),
                    message="Выберите дату",
                )
                horoscope()
            elif event.text == "камень-ножницы-бумага":
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=json.dumps(keyboard_play_2, ensure_ascii=True),
                    message="Какой ваш выбор? "
                    "К"
                    " - Камень, "
                    "Н"
                    " - Ножницы, "
                    "Б"
                    " - Бумага\n",
                )
                play_2()
            else:
                vk.messages.send(
                    user_id=event.user_id,
                    random_id=get_random_id(),
                    keyboard=json.dumps(keyboard, ensure_ascii=True),
                    message='😨Неизвестная команда😰.\nНапиши "Помощь"',
                )

                
async def app(scope, receive, send):
    assert scope['type'] == 'http'

    
    await send({
        'type': 'http.response.start',
        'status': 200,
        'headers': [
            [b'content-type', b'text/plain'],
        ],
    })
    
    await send({
        'type': 'http.response.body',
        'body': b'Hello, world!',
    })
    
    await main()
    
    