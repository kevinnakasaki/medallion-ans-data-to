#!/bin/bash
set -e

echo "Aguardando MinIO em http://${MINIO_ENDPOINT}"
until python -c "
import boto3, os
s3 = boto3.client('s3',
    endpoint_url='http://' + os.environ['MINIO_ENDPOINT'],
    aws_access_key_id=os.environ['MINIO_ACCESS_KEY'],
    aws_secret_access_key=os.environ['MINIO_SECRET_KEY'],
    region_name='us-east-1')
s3.list_buckets()
" 2>/dev/null; do
    sleep 2
done
echo "MinIO pronto!"

echo "Aguardando Prefect Server..."
until python -c "
import httpx, os
r = httpx.get(os.environ['PREFECT_API_URL'] + '/health', timeout=5)
assert r.status_code == 200
" 2>/dev/null; do
    sleep 2
done
echo "Prefect Server pronto!"

echo "Iniciando Prefect worker..."
exec prefect worker start --pool default
