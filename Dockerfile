FROM ubuntu:20.04
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y
RUN apt-get install -y git
RUN apt-get install -y python3-pip
RUN apt-get install -y ffmpeg

RUN pip3 install --upgrade pip

WORKDIR /app
COPY . .

RUN pip3 install -r requirements.txt

CMD ./start.sh