FROM python:3.10 as base
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

FROM base as poetry
RUN pip install poetry==1.3.1
COPY ["pyproject.toml", "poetry.lock", "/app/"]
RUN poetry export -o requirements.txt

FROM base as build
COPY --from=poetry /app/requirements.txt /tmp/requirements.txt
RUN python -m venv .venv && \
    .venv/bin/pip install 'wheel==0.36.2' && \
    .venv/bin/pip install -r /tmp/requirements.txt

FROM python:3.10-alpine as runtime
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
EXPOSE 80

RUN apk update && apk upgrade

WORKDIR /app
ENV PATH=/app/.venv/bin:$PATH
COPY --from=build /app/.venv /app/.venv
COPY . /app
CMD ["uvicorn", "json_excel_api.api:app", "--host", "0.0.0.0", "--port", "80"]