# Analisando a tabela curada

Por simplicidade, usarei somente Python e o DuckDB para as análises. Como se trata de um volume de dados pequeno, não há necessidade de distribuir o processamento usando Apache Spark. Claro que, em um ambiente produtivo, isso pode ser necessário, mas por não ter tais requisitos na requisição da demanda, optei por adotar a estratégia que atende à celeridade das análises.

Outro ponto ao considerar o DuckDB em conjunto com SQL ao invés de Python, é facilitar a análise por outras áreas que usam o SQL como meio principal para leitura dos dados, abrindo o escopo de interpretação do que foi feito para as áreas de negócio.

## Instalando e importando bibliotecas necessárias


```python
!pip install deltalake python-dotenv duckdb
```

    Requirement already satisfied: deltalake in /opt/conda/lib/python3.13/site-packages (1.6.1)
    Requirement already satisfied: python-dotenv in /opt/conda/lib/python3.13/site-packages (1.2.2)
    Requirement already satisfied: duckdb in /opt/conda/lib/python3.13/site-packages (1.5.4)
    Requirement already satisfied: arro3-core>=0.5.0 in /opt/conda/lib/python3.13/site-packages (from deltalake) (0.8.1)
    Requirement already satisfied: deprecated>=1.2.18 in /opt/conda/lib/python3.13/site-packages (from deltalake) (1.3.1)
    Requirement already satisfied: wrapt<3,>=1.10 in /opt/conda/lib/python3.13/site-packages (from deprecated>=1.2.18->deltalake) (2.2.2)



```python
import os

import duckdb
from deltalake import DeltaTable
from dotenv import load_dotenv

load_dotenv()
```




    False



## Configurando o ambiente e instanciando os serviços


```python
storage = {
    "AWS_ENDPOINT_URL": f"http://{os.environ['MINIO_ENDPOINT']}",
    "AWS_ACCESS_KEY_ID": os.environ["MINIO_ACCESS_KEY"],
    "AWS_SECRET_ACCESS_KEY": os.environ["MINIO_SECRET_KEY"],
    "AWS_REGION": "us-east-1",
    "AWS_ALLOW_HTTP": "true",
    "AWS_S3_ALLOW_UNSAFE_RENAME": "true",
}

table = DeltaTable("s3://gold/ans_data", storage_options=storage)
df = table.to_pandas()
conn = duckdb.connect()
conn.register("gold_df", df)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>DT_CARGA</th>
      <th>count_star()</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2026-05-20</td>
      <td>84175</td>
    </tr>
  </tbody>
</table>
</div>



## Analisando a composição da tabela


```python
conn.execute("SELECT DT_CARGA, COUNT(*) FROM gold_df GROUP BY DT_CARGA").df()
```


```python
conn.execute("DESCRIBE gold_df").df()
```


```python
conn.execute("SUMMARIZE gold_df").df()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>column_name</th>
      <th>column_type</th>
      <th>min</th>
      <th>max</th>
      <th>approx_unique</th>
      <th>avg</th>
      <th>std</th>
      <th>q25</th>
      <th>q50</th>
      <th>q75</th>
      <th>count</th>
      <th>null_percentage</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>ID_CMPT_MOVEL</td>
      <td>VARCHAR</td>
      <td>2025-08</td>
      <td>2025-08</td>
      <td>1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>84175</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>CD_OPERADORA</td>
      <td>BIGINT</td>
      <td>582</td>
      <td>424188</td>
      <td>402</td>
      <td>293037.79133947135</td>
      <td>121776.51429700614</td>
      <td>301949</td>
      <td>313083</td>
      <td>358399</td>
      <td>84175</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>NM_RAZAO_SOCIAL</td>
      <td>VARCHAR</td>
      <td>2CARE OPERADORA DE SAÚDE LTDA.</td>
      <td>W. DENTAL PLANOS ODONTOLÓGICOS S.A</td>
      <td>332</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>84175</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>NR_CNPJ</td>
      <td>BIGINT</td>
      <td>6037000127</td>
      <td>97388490000187</td>
      <td>374</td>
      <td>36823605523352.7</td>
      <td>29090104629737.145</td>
      <td>4313123233583</td>
      <td>37313475000148</td>
      <td>58119199000151</td>
      <td>84175</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>MODALIDADE_OPERADORA</td>
      <td>VARCHAR</td>
      <td>AUTOGESTÃO</td>
      <td>SEGURADORA ESPECIALIZADA EM SAÚDE</td>
      <td>7</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>84175</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>SG_UF</td>
      <td>VARCHAR</td>
      <td>TO</td>
      <td>TO</td>
      <td>1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>84175</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>CD_MUNICIPIO</td>
      <td>BIGINT</td>
      <td>170000</td>
      <td>172210</td>
      <td>144</td>
      <td>171300.44482328484</td>
      <td>758.5865924917722</td>
      <td>170550</td>
      <td>171560</td>
      <td>172100</td>
      <td>84175</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>7</th>
      <td>NM_MUNICIPIO</td>
      <td>VARCHAR</td>
      <td>Abreulândia</td>
      <td>Xambioá</td>
      <td>176</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>84175</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>8</th>
      <td>TP_SEXO</td>
      <td>VARCHAR</td>
      <td>F</td>
      <td>M</td>
      <td>2</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>84175</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>9</th>
      <td>DE_FAIXA_ETARIA</td>
      <td>VARCHAR</td>
      <td>1 a 4 anos</td>
      <td>Menos de 1 ano</td>
      <td>17</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>84175</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>10</th>
      <td>DE_FAIXA_ETARIA_REAJ</td>
      <td>VARCHAR</td>
      <td>0 a 18 anos</td>
      <td>59 anos ou mais</td>
      <td>10</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>84175</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>11</th>
      <td>CD_PLANO</td>
      <td>VARCHAR</td>
      <td>-1</td>
      <td>Z</td>
      <td>2727</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>84175</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>12</th>
      <td>TP_VIGENCIA_PLANO</td>
      <td>VARCHAR</td>
      <td>A</td>
      <td>P</td>
      <td>2</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>84175</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>13</th>
      <td>DE_CONTRATACAO_PLANO</td>
      <td>VARCHAR</td>
      <td>Coletivo Empresarial</td>
      <td>Não Identificado</td>
      <td>5</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>84175</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>14</th>
      <td>DE_SEGMENTACAO_PLANO</td>
      <td>VARCHAR</td>
      <td>Amb + Hosp c/s Obstetrícia</td>
      <td>Referência</td>
      <td>13</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>84175</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>15</th>
      <td>DE_ABRG_GEOGRAFICA_PLANO</td>
      <td>VARCHAR</td>
      <td>Estadual</td>
      <td>Não Identificado</td>
      <td>6</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>84175</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>16</th>
      <td>COBERTURA_ASSIST_PLAN</td>
      <td>VARCHAR</td>
      <td>Médico-hospitalar</td>
      <td>Odontológico</td>
      <td>2</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>84175</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>17</th>
      <td>TIPO_VINCULO</td>
      <td>VARCHAR</td>
      <td>Dependente</td>
      <td>Titular</td>
      <td>3</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>84175</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>18</th>
      <td>QT_BENEFICIARIO_ATIVO</td>
      <td>BIGINT</td>
      <td>0</td>
      <td>1035</td>
      <td>251</td>
      <td>3.284419364419364</td>
      <td>16.174272663876973</td>
      <td>1</td>
      <td>1</td>
      <td>2</td>
      <td>84175</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>19</th>
      <td>QT_BENEFICIARIO_ADERIDO</td>
      <td>BIGINT</td>
      <td>0</td>
      <td>34</td>
      <td>26</td>
      <td>0.07186219186219187</td>
      <td>0.5416383749125955</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>84175</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>20</th>
      <td>QT_BENEFICIARIO_CANCELADO</td>
      <td>BIGINT</td>
      <td>0</td>
      <td>19</td>
      <td>20</td>
      <td>0.06418770418770418</td>
      <td>0.38114670910951876</td>
      <td>0</td>
      <td>0</td>
      <td>0</td>
      <td>84175</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>21</th>
      <td>DT_CARGA</td>
      <td>TIMESTAMP</td>
      <td>2026-05-20 00:00:00</td>
      <td>2026-05-20 00:00:00</td>
      <td>1</td>
      <td>2026-05-20 00:00:00</td>
      <td>NaN</td>
      <td>2026-05-20 00:00:00</td>
      <td>2026-05-20 00:00:00</td>
      <td>2026-05-20 00:00:00</td>
      <td>84175</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>



## Consultas solicitadas

### a) Quais são as **5 operadoras** com **maior número de beneficiários ativos**?


```python
conn.execute("""
    SELECT 
        CD_OPERADORA,
        NM_RAZAO_SOCIAL,
        CAST(SUM(QT_BENEFICIARIO_ATIVO) AS INT) AS QT_TOTAL_BENEFICIARIOS_ATIVOS
    FROM gold_df
    GROUP BY 1, 2 ORDER BY 3 DESC
    LIMIT 5
""").df()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>CD_OPERADORA</th>
      <th>NM_RAZAO_SOCIAL</th>
      <th>QT_TOTAL_BENEFICIARIOS</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>374440</td>
      <td>PREVIDENT ASSISTÊNCIA ODONTOLÓGICA S.A</td>
      <td>67430</td>
    </tr>
    <tr>
      <th>1</th>
      <td>301949</td>
      <td>ODONTOPREV S/A</td>
      <td>52832</td>
    </tr>
    <tr>
      <th>2</th>
      <td>309907</td>
      <td>UNIMED PALMAS COOPERATIVA DE TRABALHO MÉDICO</td>
      <td>29356</td>
    </tr>
    <tr>
      <th>3</th>
      <td>5711</td>
      <td>BRADESCO SAÚDE S.A.</td>
      <td>16280</td>
    </tr>
    <tr>
      <th>4</th>
      <td>313084</td>
      <td>COOPERATIVA DE TRABALHO MEDICO DE ARAGUAÍNA - ...</td>
      <td>14355</td>
    </tr>
  </tbody>
</table>
</div>



### b) Qual é a **faixa etária com mais beneficiários** e **quantos** são?

A pergunta ficou um pouco ambígua com relação à qualificação dos beneficiários, podendo ser: ativos OU a soma de ativos e aderidos. Seguem abaixo as análises em ambos os casos:

#### b1) Considerando somente beneficiários ativos:


```python
conn.execute("""
    SELECT
        DE_FAIXA_ETARIA, 
        DE_FAIXA_ETARIA_REAJ, 
        CAST(SUM(QT_BENEFICIARIO_ATIVO) AS INT) AS QT_TOTAL_BENEFICIARIOS_ATIVOS
    FROM gold_df
    GROUP BY 1, 2 ORDER BY 3 DESC
    LIMIT 1
""").df()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>DE_FAIXA_ETARIA</th>
      <th>DE_FAIXA_ETARIA_REAJ</th>
      <th>QT_TOTAL_BENEFICIARIOS_ATIVOS</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>35 a 39 anos</td>
      <td>34 a 38 anos</td>
      <td>21967</td>
    </tr>
  </tbody>
</table>
</div>



#### b2) Considerando a soma de ativos e aderidos:


```python
conn.execute("""
    SELECT
        DE_FAIXA_ETARIA, 
        DE_FAIXA_ETARIA_REAJ, 
        CAST(SUM(QT_BENEFICIARIO_ATIVO) AS INT)
        + CAST(SUM(QT_BENEFICIARIO_ADERIDO) AS INT) AS QT_TOTAL_BENEFICIARIOS
    FROM gold_df
    GROUP BY 1, 2 ORDER BY 3 DESC
    LIMIT 1
""").df()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>DE_FAIXA_ETARIA</th>
      <th>DE_FAIXA_ETARIA_REAJ</th>
      <th>QT_TOTAL_BENEFICIARIOS</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>35 a 39 anos</td>
      <td>34 a 38 anos</td>
      <td>22434</td>
    </tr>
  </tbody>
</table>
</div>



### c) Liste, de forma **decrescente**, a **quantidade de beneficiários por município**.

Seguindo o mesmo problema de ambiguidade da questão acima, podemos ter a quantidade total considerando somente ativos OU a soma de ativos e aderidos aos planos.

#### c1) Considerando somente beneficiários ativos:


```python
conn.execute("""
    SELECT
        NM_MUNICIPIO,
        SG_UF,
        CAST(SUM(QT_BENEFICIARIO_ATIVO) AS INT) AS QT_TOTAL_BENEFICIARIOS_ATIVOS
    FROM gold_df
    GROUP BY 1, 2 ORDER BY 3 DESC
""").df()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>NM_MUNICIPIO</th>
      <th>SG_UF</th>
      <th>QT_TOTAL_BENEFICIARIOS_ATIVOS</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Palmas</td>
      <td>TO</td>
      <td>127812</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Araguaína</td>
      <td>TO</td>
      <td>37846</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Gurupi</td>
      <td>TO</td>
      <td>18251</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Porto Nacional</td>
      <td>TO</td>
      <td>15821</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Paraíso do Tocantins</td>
      <td>TO</td>
      <td>7542</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>135</th>
      <td>Ipueiras</td>
      <td>TO</td>
      <td>38</td>
    </tr>
    <tr>
      <th>136</th>
      <td>Monte Santo do Tocantins</td>
      <td>TO</td>
      <td>37</td>
    </tr>
    <tr>
      <th>137</th>
      <td>Santa Rita do Tocantins</td>
      <td>TO</td>
      <td>35</td>
    </tr>
    <tr>
      <th>138</th>
      <td>Chapada de Areia</td>
      <td>TO</td>
      <td>26</td>
    </tr>
    <tr>
      <th>139</th>
      <td>Município ignorado - TO</td>
      <td>TO</td>
      <td>8</td>
    </tr>
  </tbody>
</table>
<p>140 rows × 3 columns</p>
</div>



#### c2) Considerando a soma de ativos e aderidos:


```python
conn.execute("""
    SELECT
        NM_MUNICIPIO,
        SG_UF,
        CAST(SUM(QT_BENEFICIARIO_ATIVO) AS INT)
        + CAST(SUM(QT_BENEFICIARIO_ADERIDO) AS INT) AS QT_TOTAL_BENEFICIARIOS
    FROM gold_df
    GROUP BY 1, 2 ORDER BY 3 DESC
""").df()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>NM_MUNICIPIO</th>
      <th>SG_UF</th>
      <th>QT_TOTAL_BENEFICIARIOS</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Palmas</td>
      <td>TO</td>
      <td>130810</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Araguaína</td>
      <td>TO</td>
      <td>38682</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Gurupi</td>
      <td>TO</td>
      <td>18604</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Porto Nacional</td>
      <td>TO</td>
      <td>16340</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Paraíso do Tocantins</td>
      <td>TO</td>
      <td>7721</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>135</th>
      <td>Monte Santo do Tocantins</td>
      <td>TO</td>
      <td>38</td>
    </tr>
    <tr>
      <th>136</th>
      <td>Ipueiras</td>
      <td>TO</td>
      <td>38</td>
    </tr>
    <tr>
      <th>137</th>
      <td>Santa Rita do Tocantins</td>
      <td>TO</td>
      <td>35</td>
    </tr>
    <tr>
      <th>138</th>
      <td>Chapada de Areia</td>
      <td>TO</td>
      <td>27</td>
    </tr>
    <tr>
      <th>139</th>
      <td>Município ignorado - TO</td>
      <td>TO</td>
      <td>8</td>
    </tr>
  </tbody>
</table>
<p>140 rows × 3 columns</p>
</div>


