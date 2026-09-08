# ==============================
FROM registry.access.redhat.com/ubi9/python-312 AS appbase
# ==============================

# Install uv, see https://docs.astral.sh/uv/guides/integration/docker/#installing-uv
COPY --from=ghcr.io/astral-sh/uv:0.12.10@sha256:2bb3ebca0a796a155094a27773d290c4b074572e6107f171d88d086682fd2500 /uv /uvx /usr/local/bin/

USER root
# UBI image defaults to /opt/app-root/src
WORKDIR /opt/app-root/src

ENV UV_PROJECT_ENVIRONMENT=/opt/app-root \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_NO_CACHE=1 \
    UV_PYTHON_DOWNLOADS=never
ENV PATH="/opt/app-root/bin:$PATH"

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --group prod

COPY manage.py ./
COPY example_backend_profile/*.py example_backend_profile/
COPY users/*.py users/
COPY users/migrations/*.py users/migrations/
COPY docker-entrypoint.sh ./

ENTRYPOINT [ "./docker-entrypoint.sh" ]
USER default
