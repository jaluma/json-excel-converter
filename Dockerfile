# FROM python:3.10

# EXPOSE 80

# # Configure Poetry
# ENV POETRY_VERSION=1.3.1
# ENV POETRY_HOME=/opt/poetry
# ENV POETRY_VENV=/opt/poetry-venv
# ENV POETRY_CACHE_DIR=/opt/.cache

# # Install poetry separated from system interpreter
# RUN python3 -m venv $POETRY_VENV \
#     && $POETRY_VENV/bin/pip install -U pip setuptools \
#     && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# # Add `poetry` to PATH
# ENV PATH="${PATH}:${POETRY_VENV}/bin"

# WORKDIR /app

# # Install dependencies
# COPY poetry.lock pyproject.toml ./
# RUN poetry install

# # Run your app
# COPY . /app
# CMD [ "poetry", "run", "task", "prod" ]


# FROM python:3.10 as build-stage

# # Configure Poetry
# ENV POETRY_VERSION=1.3.1
# ENV POETRY_HOME=/opt/poetry
# ENV POETRY_VENV=/venv
# ENV POETRY_CACHE_DIR=/opt/.cache

# # Install poetry separated from system interpreter
# RUN python3 -m venv $POETRY_VENV \
#     && $POETRY_VENV/bin/pip install -U pip setuptools \
#     && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# # Add `poetry` to PATH
# ENV PATH="${PATH}:${POETRY_VENV}/bin"


# WORKDIR /app
# COPY ["pyproject.toml", "poetry.lock", "/app/"]
# RUN --mount=type=secret,id=auth,target=/root/.config/pypoetry/auth.toml \
#     poetry install --no-dev --no-interaction --remove-untracked

# FROM python:3.10-slim as final

# # Configure Poetry
# ENV PYTHONUNBUFFERED=1
# ENV VIRTUAL_ENV=/venv
# ENV PATH="${PATH}:${POETRY_VENV}/bin"

# # Do not run as root in production
# RUN useradd -m appuser
# USER appuser

# WORKDIR /app

# # Copy only application dependencies contained in the virtual environment
# COPY --from=build-stage --chown=appuser $VIRTUAL_ENV $VIRTUAL_ENV
# COPY --chown=appuser [".", "/app"]

# # Run your app
# CMD [ "poetry", "run", "task", "prod" ]

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