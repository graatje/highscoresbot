FROM python:3.11

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY ./ /app/

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE ${APP_PORT}

ENTRYPOINT ["sh", "-c", "python manage.py runserver 0.0.0.0:${APP_PORT}"]
