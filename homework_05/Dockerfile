FROM alpine:3.14

RUN apk add --no-cache \
    python3~=3.9.5 \
    py3-pip~=20.3.4

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

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

USER app

EXPOSE 8080

ENTRYPOINT ["flask"]
CMD [ "run", "--host=0.0.0.0", "--port=8080"]
