Запуск проекта
==================

Чтобы запустить чат-бота на локальном компьютере, нужно установить проект. Предварительно установить менеджер зависимостей poetry:

* Mac и Linux

.. code-block:: bash

    $ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -

* Windows


.. code-block:: bash

    $ (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -

* Установка через pip


.. code-block:: bash

    $ pip install poetry

Для запуска проекта выполнить следующие действия:

.. code-block:: bash
    
    $ git clone https://github.com/izziantiya/trpp_bot.git
    $ cd trpp_bot
    $ poetry config virtualenvs.in-project true
    $ poetry install
    $ poetry shell
    $ python main.py

Также необходимо разрешение на получение API-ключа чат-бота.

Для запуска в социальной сети не нужно вводить никаких команд. Бот всегда активен и доступен по ссылке: https://vk.com/club195064461