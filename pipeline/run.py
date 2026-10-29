"""
Executa o pipeline completo, na ordem:

    1. produtos: data/raw/amazon.csv -> data/processed/amazon_sales_cleaned.csv
    2. reviews:  amazon_sales_cleaned.csv -> fReviews, fReviewTema, sentimento_por_produto

Uso (a partir da pasta pipeline/):
    pip install -r requirements.txt
    python run.py
"""

from src import config, produtos, reviews


def main():
    print("== Etapa 1: produtos")
    produtos.executar(config.ARQ_AMAZON_RAW, config.ARQ_PRODUTOS)

    print("\n== Etapa 2: reviews")
    reviews.executar(
        config.ARQ_PRODUTOS,
        config.ARQ_DICIONARIO_TEMAS,
        config.ARQ_REVIEWS,
        config.ARQ_REVIEW_TEMA,
        config.ARQ_SENTIMENTO_PRODUTO,
    )


if __name__ == "__main__":
    main()
