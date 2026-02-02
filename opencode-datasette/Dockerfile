FROM python:3.11-slim

RUN pip install --no-cache-dir \
    datasette \
    datasette-json-html \
    datasette-pretty-json

WORKDIR /data

EXPOSE 8001

CMD ["datasette", "/data/logs.db", "--host", "0.0.0.0", "--port", "8001", "--setting", "sql_time_limit_ms", "10000"]
