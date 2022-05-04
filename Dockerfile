FROM python:3.8-buster

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

WORKDIR /app
COPY . .

# AWS X-Ray deamon
RUN mkdir xray
RUN curl https://s3.dualstack.ap-northeast-1.amazonaws.com/aws-xray-assets.ap-northeast-1/xray-daemon/aws-xray-daemon-3.x.deb -o ./xray/aws-xray-daemon-3.x.deb
RUN dpkg -i ./xray/aws-xray-daemon-3.x.deb

# SQL DB Driver
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/10/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql18
RUN apt-get install -y unixodbc-dev

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry update

RUN chmod 744 ./startup.sh

ENTRYPOINT ["./startup.sh"]