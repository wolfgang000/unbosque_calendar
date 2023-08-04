FROM python:3.11.4-alpine3.18 as requirements-stage

WORKDIR /tmp
RUN pip install poetry==1.5.1
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11.4-alpine3.18

RUN apk update \
    && apk add --no-cache \
    bash

COPY . /app
WORKDIR /app

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=:/app/src

CMD ["gunicorn", "unbosque_calendar.wsgi"]