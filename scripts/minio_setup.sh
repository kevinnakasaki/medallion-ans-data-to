#!/bin/bash

# waiting the service beeing available
echo "Waiting for MinIO to be available..."
for i in $(seq 1 30); do
    if mc alias set minio http://minio:9000 $MINIO_ACCESS_KEY $MINIO_SECRET_KEY 2>/dev/null; then
        echo "MinIO is available"
        break
    fi
    echo "MinIO not available, retrying in 5 seconds..."
    sleep 5
done

mc mb -p minio/bronze
mc anonymous set public minio/bronze
mc mb -p minio/silver
mc anonymous set public minio/silver
mc mb -p minio/gold
mc anonymous set public minio/gold
echo "MinIO setup successfully finished"
