FROM python:3.11-slim

WORKDIR /app

COPY app/app.py /app/app.py

RUN pip install fastapi uvicorn pika

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
