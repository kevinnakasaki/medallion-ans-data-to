import duckdb


def get_connection(minio_config: dict) -> duckdb.DuckDBPyConnection:
    conn = duckdb.connect()
    conn.execute("INSTALL httpfs")
    conn.execute("LOAD httpfs")
    conn.execute(f"SET s3_region = '{minio_config['region']}'")
    conn.execute(f"SET s3_endpoint = '{minio_config['endpoint']}'")
    conn.execute(f"SET s3_access_key_id = '{minio_config['access_key']}'")
    conn.execute(f"SET s3_secret_access_key = '{minio_config['secret_key']}'")
    conn.execute(f"SET s3_use_ssl = {'true' if minio_config['use_ssl'] else 'false'}")
    conn.execute("SET s3_url_style = 'path'")

    conn.execute("INSTALL delta")
    conn.execute("LOAD delta")
    conn.execute(f"""
        CREATE OR REPLACE SECRET minio_secret (
            TYPE S3,
            KEY_ID '{minio_config["access_key"]}',
            SECRET '{minio_config["secret_key"]}',
            ENDPOINT '{minio_config["endpoint"]}',
            URL_STYLE 'path',
            REGION '{minio_config["region"]}',
            USE_SSL false
        )
    """)
    return conn
