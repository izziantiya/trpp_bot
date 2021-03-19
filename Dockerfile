FROM python:3.8-slim

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    POETRY_VERSION=1.1.4

RUN apt-get update \
    && apt-get install -y dos2unix \
    && python -m pip install --upgrade pip \
    && pip install "poetry==$POETRY_VERSION" \
    && poetry config virtualenvs.in-project true

WORKDIR /bot

COPY ./scripts /scripts
COPY ./poetry.lock ./pyproject.toml /bot/

RUN chmod +x /scripts/*

RUN poetry install --no-dev
RUN dos2unix /scripts/* && apt-get --purge remove -y dos2unix && rm -rf /var/lib/apt/lists/* 

RUN useradd -ms /bin/bash bot
USER bot

ENTRYPOINT [ "/scripts/entrypoint.sh" ]

COPY . /bot