FROM python:3.9-alpine as builder
RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev musl-dev openssl-dev
RUN pip install --upgrade pip
RUN pip install poetry

ADD pyproject.toml /build/pyproject.toml
ADD realdebridmanager /build/realdebridmanager
WORKDIR /build
RUN poetry build -f wheel

FROM python:3.9-alpine
RUN mkdir /app
COPY --from=builder /build/dist/*.whl /app
RUN pip install /app/*.whl
RUN mkdir /watch
RUN mkdir /config
WORKDIR /app
ADD startscript.sh /app
RUN chmod a+x startscript.sh
ENTRYPOINT [ "/bin/sh", "startscript.sh" ]
