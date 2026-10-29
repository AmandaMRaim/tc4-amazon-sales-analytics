"""Caminhos usados pelo pipeline. Todos relativos a pasta pipeline/."""

from pathlib import Path

PASTA_PIPELINE = Path(__file__).resolve().parents[1]
PASTA_DADOS = PASTA_PIPELINE / "data"

# raw: base original do Kaggle, nunca alterada
ARQ_AMAZON_RAW = PASTA_DADOS / "raw" / "amazon.csv"

# reference: tabelas de apoio mantidas a mao
ARQ_DICIONARIO_TEMAS = PASTA_DADOS / "reference" / "dicionario_temas.csv"

# processed: saidas tratadas, consumidas pelo Power BI
PASTA_PROCESSED = PASTA_DADOS / "processed"
ARQ_PRODUTOS = PASTA_PROCESSED / "amazon_sales_cleaned.csv"
ARQ_REVIEWS = PASTA_PROCESSED / "fReviews.csv"
ARQ_REVIEW_TEMA = PASTA_PROCESSED / "fReviewTema.csv"
ARQ_SENTIMENTO_PRODUTO = PASTA_PROCESSED / "sentimento_por_produto.csv"
