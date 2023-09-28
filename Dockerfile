FROM python:3.11.4-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONPATH='/'

COPY ./poetry.lock /
COPY ./pyproject.toml /
COPY ./src /src

RUN apt-get update -y && apt-get install curl -y \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry config virtualenvs.create false \
    && poetry install 


WORKDIR /src

CMD [ "flask", "run", "--host", "0.0.0.0", "--debug" ]
