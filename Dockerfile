# Used by Azure Devops to pull from internal registry
ARG BUILDER_REGISTRY=registry.access.redhat.com
# ==============================
FROM ${BUILDER_REGISTRY}/ubi9/python-39:latest
# ==============================

WORKDIR /usr/src/app
RUN chmod g+w /usr/src/app

COPY requirements.txt ./
RUN pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

COPY manage.py ./
COPY example_backend_profile/*.py example_backend_profile/
COPY users/*.py users/
COPY users/migrations/*.py users/migrations/
COPY docker-entrypoint.sh ./

ENTRYPOINT [ "./docker-entrypoint.sh" ]
