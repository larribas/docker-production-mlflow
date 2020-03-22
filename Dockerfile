FROM python:3.8.2-slim

RUN pip install boto3==1.12.26 && \           # We need to install boto3 explicitly due to this bug: https://github.com/mlflow/mlflow/issues/1970
    pip install psycopg2-binary==2.8.4 && \   # We need this dependency to work with a Postgres-backed backend store
    pip install mlflow==1.7.0

ENTRYPOINT ["mlflow", "server"]
