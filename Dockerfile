FROM python:3.12.3

ENV PYTHONIOENCODING UTF-8

RUN python -m pip install --upgrade pip

WORKDIR /app

COPY ./rumbos_app .

RUN --mount=type=cache,target=/root/.cache pip install -r requirements.txt

# RUN pyside6-deploy  --output dist rumbos_app/rumbos_generator.py
