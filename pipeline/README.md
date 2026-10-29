# Pipeline de dados

Versão organizada do tratamento de dados do Tech Challenge. Reúne em um só lugar o código que hoje está espalhado entre `notebooks/` e `frente2/`, **sem mudar a lógica**: as funções foram copiadas dos originais, e as saídas de reviews são idênticas byte a byte às de `frente2/saidas/`.

## Estrutura

```
pipeline/
├── run.py                      # roda tudo, na ordem
├── requirements.txt
├── src/
│   ├── config.py               # caminhos de entrada e saída
│   ├── produtos.py             # tratamento da base de produtos
│   └── reviews.py              # reviews: separação, sentimento e temas
└── data/
    ├── raw/                    # base original do Kaggle (não alterar)
    │   └── amazon.csv
    ├── reference/              # tabelas de apoio mantidas à mão
    │   └── dicionario_temas.csv
    └── processed/              # saídas tratadas, lidas pelo Power BI
        ├── amazon_sales_cleaned.csv
        ├── fReviews.csv
        ├── fReviewTema.csv
        └── sentimento_por_produto.csv
```

## Como rodar

A partir da pasta `pipeline/`:

```bash
pip install -r requirements.txt
python run.py
```

O pipeline tem duas etapas:

| Etapa | Entrada | Saída | Origem do código |
|---|---|---|---|
| 1. Produtos | `raw/amazon.csv` | `amazon_sales_cleaned.csv` | `notebooks/TC4fase.ipynb` |
| 2. Reviews | `amazon_sales_cleaned.csv` + `dicionario_temas.csv` | `fReviews.csv`, `fReviewTema.csv`, `sentimento_por_produto.csv` | `frente2/scripts/frente2_reviews.py` |

A etapa 1 limpa preços, desconto, nota e quantidade de avaliações, separa a categoria em `categoria_1…7`, calcula `discount_amount` e deixa uma linha por produto (1.351 produtos).

A etapa 2 separa os reviews em uma linha por produto × review, classifica o sentimento com o VADER e marca os temas. Detalhes da lógica, do dicionário de colunas e das limitações estão em [frente2/README.md](../frente2/README.md).

## Para ajustar

- **Temas:** edite `data/reference/dicionario_temas.csv` e rode `python run.py` de novo.
- **Caminhos:** ficam todos em `src/config.py`.

## O que mudou em relação aos originais

- O notebook `TC4fase.ipynb` baixava a base pelo `kagglehub`. Aqui ela é lida de `data/raw/amazon.csv`, que é o mesmo arquivo já versionado no repositório.
- Os caminhos fixos foram trocados por parâmetros, definidos em `src/config.py`.
- A etapa de reviews lê o `amazon_sales_cleaned.csv` em vez do `amazon.csv`. O script original aceita os dois, e o resultado é o mesmo.
- Os arquivos originais (`notebooks/`, `frente2/`, `data/`) continuam onde estavam.
