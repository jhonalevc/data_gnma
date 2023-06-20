FROM python:3

RUN apt-get update && apt-get -y install cron vim tzdata

RUN apt-get --assume-yes install freetds-dev freetds-bin 

RUN apt-get --assume-yes install python-dev

WORKDIR /app

EXPOSE 8525

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    libpq-dev gcc \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip3 install -r requirements.txt

ENTRYPOINT ["streamlit", "run", "APP.py","--server.port=8525"]