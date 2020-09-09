FROM python:3.8

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY manage.py ./
COPY example_backend_profile/*.py example_backend_profile/

RUN ./manage.py migrate --noinput

CMD [ "./manage.py", "runserver", "0.0.0.0:8000" ]
