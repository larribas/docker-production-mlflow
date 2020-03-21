FROM python:3.8.2-slim

RUN pip install mlflow==1.7.0 && \
    pip install boto3==1.12.26  # We need to install boto3 explicitly due to this bug: https://github.com/mlflow/mlflow/issues/1970

ENTRYPOINT ["mlflow", "server"]
