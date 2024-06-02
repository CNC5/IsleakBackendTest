FROM python:3.11
RUN pip install sqlalchemy flask elasticsearch pyparsing psycopg2 pytest gunicorn
COPY . /app

WORKDIR /app
ENTRYPOINT ["/usr/local/bin/gunicorn", "server:app", "--bind", "0.0.0.0:5000"]