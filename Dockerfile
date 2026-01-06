# Multi-stage Dockerfile
#
# derived from:
# - https://github.com/astral-sh/uv-docker-example/blob/main/multistage.Dockerfile
# - https://docs.astral.sh/uv/guides/integration/docker/#installing-uv


# build image
FROM python:3.13-slim-trixie AS builder

# install uv (package manager)
COPY --from=ghcr.io/astral-sh/uv:0.9.21 /uv /uvx /bin/

# copy the project into the image
COPY . /app

# sync the project into a new environment, asserting the lockfile is up to date
WORKDIR /app
# disable development dependencies
ENV UV_NO_DEV=1
RUN uv sync --locked


# final runtime image
FROM python:3.13-slim-trixie

# setup a nonroot user
RUN groupadd --gid 1001 nonroot \
    && useradd --no-log-init --gid 1001 --uid 1001 nonroot

# copy the app to the image
# (we copy the app at the end to take advantage from the build cache)
COPY --from=builder --chown=nonroot:nonroot /app /app

# place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

USER nonroot

CMD ["python", "python_template/main.py"]
