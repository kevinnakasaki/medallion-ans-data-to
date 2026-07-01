# Arquitetura Medalhão com dados abertos da ANS

## Arquitetura

```mermaid
graph TB
  subgraph Docker_Compose["Docker Compose"]
    direction TB
    MinIO[MinIO<br/>:9000 / :9001]
    PrefectDB[(Prefect DB<br/>PostgreSQL)]
    PrefectServer[Prefect Server<br/>:4200]
    Worker[Worker / Python<br/>Prefect Agent]
  end

  subgraph Pipeline["Medallion Pipeline"]
    direction TB
    Bronze[download_to_bronze<br/>URL -> Bronze Delta]
    Silver[bronze_to_silver<br/>Clean -> Silver Delta]
    Gold[silver_to_gold<br/>Aggregate -> Gold Delta]
  end

  subgraph Buckets["MinIOBuckets"]
    B1[(bronze)]
    S1[(silver)]
    G1[(gold)]
  end

  PrefectServer --> |orchestrates| Worker
  Worker --> Bronze --> B1
  B1 --> Silver --> S1
  S1 --> Gold --> G1
  MinIO --> B1 & S1 & G1
```

## Stack

- **MinIO**: Object storage
- **DuckDB**: Processamento SQL (OLAP)
- **Pandas**: Manipulação de dados
- **Prefect**: Orquestração de pipelines de maneira leve e declarativa
- **Delta Lake**: Armazenamento de dados com transações ACID no MinIO

## Pré-requisitos

- Docker + Docker Compose

## Estrutura do Projeto
```
src/
├── flows/
│   ├── bronze.py               # coleta
│   ├── silver.py               # limpeza e transformações
│   └── gold.py                 # agregações
└── pipelines/
│   └── medallion_pipeline.py   # flow do Prefect
└── utils/
    ├── config.py               # configurações do projeto  
    ├── duckdb_helpers.py       # conexão do DuckDB + S3
    └── minio_client.py         # cliente boto3 para MinIO
```

## Setup rápido

```bash
# 1. Configurar o ambiente
cp .env.example .env
# Editar DATA_URL no .env com a URL dos dados a serem processados
# 2. Subir a infra
# 2.1 Na primeira vez, execute:
make init # sobe uma combinação de comandos: setup + build + up

# 2.2 Ou individualmente:
make setup # cria buckets no MinIO
make build # builda os containers
make up # inicia os containers

# 3. Executar a pipeline
make run-flow
```

### Comandos úteis
- `make setup`: configura o ambiente
- `make build`: builda os containers
- `make up`: inicia os containers
- `make down`: para os containers
- `make logs`: exibe os logs dos container
- `make shell`: abre um shell interativo no container
- `make run-flow`: executa a pipeline existente
- `make clean`: remove os containers e volumes
- `make init`: executa `setup`, `build` e `up` em sequência

## Variáveis de ambiente
| Variável | Padrão | Descrição |
|----------|-----------|-----------|
| POSTGRES_USER | - | Usuário do PostgreSQL |
| POSTGRES_PASSWORD | - | Senha do PostgreSQL ||
| MINIO_ENDPOINT | `minio:9000` | Endpoint interno do MinIO |
| MINIO_ACCESS_KEY | - | Access key do MinIO |
| MINIO_SECRET_KEY | - | Secret key do MinIO |
| DATA_SAMPLE_URL | - | URL do arquivo (.zip) a ser processado |
| PREFECT_API_URL | `http://prefect-server:4200/api` | URL da API do Prefect |
| PREFECT_API_DATABASE_CONNECTION_URL | `postgresql+asyncpg://prefect:prefect@prefect-db:5432/prefect` | URL de conexão com o banco de dados do Prefect |
