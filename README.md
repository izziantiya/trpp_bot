# Чат-бот Вконтакте

## Общие сведения:
Данный проект принадлежит Елизавете Абраш и Максиму Бычкову. Чат-бот для социальной сети "Вконтакте" может:
<ul>
  <li>Поиграть в виселицу
    <ul>
      <li>🇷🇺 На Русском Языке 🇷🇺</li>
      <li>🇬🇧 На Английском языке 🇬🇧</li>
    </ul>
  </li>
  <li>Показать гороскоп </li>
    <ul>
      <li>На Сегодня</li>
      <li>На Завтра</li>
      <li>На Послезавтра </li>
      <li>На Вчера</li>
   </ul>
  <li>Поиграть в 👊 Камень 👊 - ✌ Ножницы ✌ - 🖐 Бумага 🖐</li>
</ul>

## Зависимости проекта:
  * Python 3.7+
  * Pip (включены по умолчанию)
  * vk_api - Python модуль для создания скриптов для социальной сети Вконтакте
  * Uvicorn - работа с сервером

Python и pip могут быть добавлены в PATH.

## Запуск проекта:
Чтобы запустить чат-бота на локальном компьютере, нужно установить проект. Предварительно установить менеджер зависимостей poetry:

Mac и Linux

    $ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
Windows

    $ (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -
Установка через pip

    $ pip install poetry
Для запуска проекта выполнить следующие действия:
    
    $ git clone https://github.com/izziantiya/trpp_bot.git
    $ cd trpp_bot
    $ poetry config virtualenvs.in-project true
    $ poetry install
    $ poetry shell
    $ python main.py

Также необходимо разрешение на получение API-ключа чат-бота.

Для запуска в социальной сети не нужно вводить никаких команд. Бот всегда активен и доступен по ссылке: https://vk.com/club195064461
