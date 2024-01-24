FROM python:3.11.7-alpine3.19 as builder

RUN apk add --no-cache libffi-dev gcc python3-dev musl-dev

RUN pip install poetry==1.7.1

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

FROM python:3.11.7-alpine3.19 as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    TZ="UTC"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY blockchain_fee_logger ./blockchain_fee_logger

ENTRYPOINT ["python", "-m", "blockchain_fee_logger.main"]
