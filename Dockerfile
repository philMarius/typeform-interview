FROM python:3.9.13-slim-buster

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD ["python3", "yaes/main.py"]
