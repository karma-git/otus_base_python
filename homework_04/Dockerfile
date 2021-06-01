# How to with docker file?
# 1). Build the image via following command:
# $ docker build --tag ah:v0.01 .
# NOTE! make sure that you dont forget dot symbol at the end of line, it means that docker going to find dockerfile in current dirctory
# 2). Run the container via following command:
# $ docker run -d ah:v0.01 -p 1234:8080
# go to your webbroweser and put http://127.0.0.1:1234 into seartch bar
FROM python:3.8-slim-buster

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8080

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8080"]





