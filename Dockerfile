FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN apt-get update && apt-get install -y build-essential libpq-dev \
    && pip3 install --upgrade pip \
    && pip3 install -r requirements.txt \
    && apt-get remove -y build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/

CMD ["gunicorn", "metro_ticket_system.wsgi:application", "--bind", "0.0.0.0:8000"]