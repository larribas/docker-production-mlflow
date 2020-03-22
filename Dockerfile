FROM python:3.8.2-slim

# We need to install the following dependencies explicitly:
# - boto3, due to this bug: https://github.com/mlflow/mlflow/issues/1970
# - psycopg2-binary to work with a Postgres-backed backend store
RUN pip install boto3==1.12.26 && \
     pip install psycopg2-binary==2.8.4 && \   
     pip install mlflow==1.7.0

ENTRYPOINT ["mlflow", "server"]
