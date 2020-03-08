FROM python:3.8.2-slim

ARG version 

# Install the specific version of MLFlow, or the latest one
RUN pip install mlflow==$version || pip install mlflow

ENTRYPOINT ["mlflow", "server"]
