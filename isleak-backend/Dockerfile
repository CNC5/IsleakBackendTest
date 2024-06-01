FROM python:3.11
RUN pip install sqlalchemy flask elasticsearch pyparsing psycopg2 pytest
COPY . /app

WORKDIR /app
ENTRYPOINT ["/usr/local/bin/python", "server.py"]