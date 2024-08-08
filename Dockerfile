###############################################################################
## Builder
###############################################################################
FROM alpine:3.20 as builder

ENV RYE_INSTALL_OPTION="--yes"
RUN echo "**** install Python ****" && \
    apk add --update --no-cache --virtual \
            .build-deps \
            musl-dev~=1.2 \
            python3-dev~=3.12 \
            python3~=3.12 \
            py3-pip~=24.0 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.lock ./
RUN python -m venv /app/.venv && \
    source /app/.venv/bin/activate && \
    pip install --upgrade pip && \
    PYTHONDONTWRITEBYTECODE=1 pip install --no-cache-dir -r /app/requirements.lock

COPY src .

###############################################################################
## Final image
###############################################################################
FROM alpine:3.20

LABEL maintainer="Lorenzo Carbonell <a.k.a. atareao> lorenzo.carbonell.cerezo@gmail.com"

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONIOENCODING=utf-8 \
    PYTHONUNBUFFERED=1 \
    USER=app \
    UID=10001

RUN echo "**** install Python ****" && \
    apk add --update --no-cache \
            tzdata~=2024 \
            python3~=3.12 && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY run.sh /app/

RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/${USER}" \
    --shell "/sbin/nologin" \
    --uid "${UID}" \
    "${USER}" && \
    chown -R app:app /app


WORKDIR /app
USER app

CMD ["/bin/sh", "/app/run.sh"]
