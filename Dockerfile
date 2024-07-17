FROM python:3.12

ENV LANG=C.UTF-8

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD python manage.py makemigrations && \
    python manage.py migrate