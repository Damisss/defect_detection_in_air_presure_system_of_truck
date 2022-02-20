FROM python:3.7
WORKDIR /app
RUN pip install mlflow 
EXPOSE 1234
CMD mlflow server --backend-store-uri sqlite:///mlflow.db \
--default-artifact-root ./artifacts \
--host 0.0.0.0 \
--port 1234