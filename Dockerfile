FROM python:3.13-slim
USER root
COPY src/ /app/src
COPY scripts/minio_setup.sh /app/scripts/minio_setup.sh
RUN chmod +x /app/scripts/minio_setup.sh
COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
RUN chmod +x /app/scripts/entrypoint.sh
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /app
ENTRYPOINT [ "/app/scripts/entrypoint.sh" ]
