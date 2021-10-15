FROM alpine:3.14

RUN apk add --no-cache \
    python3~=3.9.5 \
    py3-pip~=20.3.4 \
    py3-psycopg2~=2.8.6 \
  && apk add --no-cache --virtual .build-deps \
    build-base~=0.5 \
    gcc~=10.3 \
    python3-dev~=3.9.5 \
    libffi-dev~=3.3 \
    musl-dev~=1.2.2 \
    make~=4.3 \
  && pip3 install --no-cache-dir \
    psycopg2==2.8.6 \
    loguru==0.5.3 \
  && apk del .build-deps

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

ENTRYPOINT ["/usr/bin/python3"]
CMD [ "_db_init.py"]
