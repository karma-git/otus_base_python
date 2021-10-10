FROM alpine:3.14

RUN apk add --no-cache \
    python3~=3.9.5 \
    py3-pip~=20.3.4

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt \
  && pip install --no-cache-dir celery==5.1.2

RUN addgroup --gid 1000 app \
  && adduser \
    --uid 1000 \
    --home /home/app \
    --shell /bin/ash \
    --ingroup app \
    --disabled-password \
    app 

COPY ./web /home/app

WORKDIR /home/app

USER app

ENTRYPOINT ["celery"]
CMD ["--version"]
