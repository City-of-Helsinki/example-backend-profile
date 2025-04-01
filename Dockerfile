# ==============================
FROM registry.access.redhat.com/ubi9/python-39 AS appbase
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
