FROM python:3.8.2-slim

# We need to install the following dependencies explicitly:
# - psycopg2-binary to work with a Postgres-backed backend store
RUN pip install psycopg2-binary==2.8.5 && \
    pip install mlflow[extras]==1.8.0

ENTRYPOINT ["mlflow", "server"]
