FROM alpine:3.14

COPY . /app

WORKDIR /app

RUN apk add --no-cache \
    python3~=3.9.5 \
    py3-pip~=20.3.4 \
  && pip3 install --no-cache-dir -r requirements-prod.txt

RUN adduser -D fastapi && chown -R fastapi /app

USER fastapi

EXPOSE 8080

ENTRYPOINT ["/usr/bin/python3"]
CMD ["main.py" ]
