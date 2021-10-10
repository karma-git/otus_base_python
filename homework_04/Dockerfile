# How to with docker file?
# 1). Build the image via the following command:
# $ docker build --tag hw:0.0.1 .
# 2). Run the container via following command:
# $ docker run -d -p 8080:8080 hw:v0.0.1a
# go to http://127.0.0.1:8080/

FROM python:3.8-slim-buster

COPY ./requirements.txt ./requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

RUN addgroup --gid 10001 app \
  && adduser \
    --uid 10001 \
    --home /home/app \
    --shell /bin/ash \
    --ingroup app \
    --disabled-password \
    app

COPY ./ /home/app

WORKDIR /home/app

USER 10001

EXPOSE 8080

ENTRYPOINT [ "flask" ]
CMD [ "run", "--host=0.0.0.0", "--port=8080"]
