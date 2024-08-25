FROM python:3.10.4-slim-bullseye

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get -y install python3-pip python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0
RUN pip install flask

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /usr/src/app

ENV FLASK_APP=main.py
ENV DB_URL=mongodb+srv://ppob:LVZFpLTlKf3KSwv9@cluster0.p6ysg.mongodb.net/
ENV XENDIT_BASIC_AUTH_KEY=xnd_development_6QbQbDCiqovaD4MfltQRnzDjSONUX2SvU6mF7FSVwvEu6rBtxj6dmEbVd7tJZB

EXPOSE 8080

CMD ["flask", "run", "--debug", "--host", "0.0.0.0", "--port", "8080"]