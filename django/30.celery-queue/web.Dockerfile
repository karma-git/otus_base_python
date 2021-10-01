FROM alpine:3.14

FROM alpine:3.14

ARG SU_PW

RUN apk add --no-cache \
    python3~=3.9.5 \
    py3-pip~=20.3.4

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt \
  && pip install --no-cache-dir celery==5.1.2

# RUN addgroup --gid 1000 app \
#   && adduser \
#     --uid 1000 \
#     --home /home/app \
#     --shell /bin/ash \
#     --ingroup app \
#     --disabled-password \
#     app \
#   && chmod -R 664 /home/app

COPY ./web /home/app

WORKDIR /home/app

# USER app

# Make DB schema and create superuser
RUN set -x \
  && python3 manage.py migrate \
  # KeyError exception if python doesn't find SU_PW env var
  && python3 manage.py shell -c \
    "from django.contrib.auth.models import User; import os; \
    User.objects.create_superuser('admin', 'admin@example.com', os.environ['SU_PW'])"

EXPOSE 8000

# TODO generate fake data
ENTRYPOINT ["/usr/bin/python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8080"]
