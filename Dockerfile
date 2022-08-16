FROM ubuntu:latest

MAINTAINER Roman Basin basin@softbalance.ru

RUN apt-get update -qy

RUN apt-get install -qy python3.10 python3-pip python3.10-dev

WORKDIR /projects/sb_bot/project

COPY . /projects/sb_bot/project

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python3.10", "bot_telegram.py"]