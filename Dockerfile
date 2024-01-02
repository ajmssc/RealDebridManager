FROM python:3.9-alpine as builder
RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev musl-dev openssl-dev cargo
RUN pip install --upgrade pip
RUN pip install poetry

ADD pyproject.toml /build/pyproject.toml
ADD realdebridmanager /build/realdebridmanager
WORKDIR /build
RUN poetry build -f wheel


FROM python:3.9-alpine

RUN mkdir /app /config /watch
RUN addgroup abc
RUN adduser abc -G abc -D -h /app

ENV TZ="America/Los_Angeles"

COPY --from=builder /build/dist/*.whl /app
RUN pip install /app/*.whl
WORKDIR /app
ADD startscript.sh /app
RUN chmod a+x startscript.sh
RUN chown -R abc:abc /app /watch /config

ENTRYPOINT [ "/bin/sh", "startscript.sh" ]
