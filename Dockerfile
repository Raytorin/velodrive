FROM python:3.12

ENV LANG=C.UTF-8

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --no-input

EXPOSE 8000

CMD python manage.py makemigrations && \
    python manage.py migrate && \
    ["python", "manage.py", "runserver", "0.0.0.0:8000"]