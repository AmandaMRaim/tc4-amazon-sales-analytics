# tc4-amazon-sales-analytics

Tech Challenge da Fase 4 (POSTECH FIAP, DTAT): análise de vendas da Amazon em Power BI.

## Estrutura

```
tc4-amazon-sales-analytics/
├── pipeline/       # tratamento dos dados; gera os CSVs lidos pelo Power BI
│   └── data/processed/
├── dashboard/      # arquivo do Power BI
└── exploracao/     # trabalho original que deu origem ao pipeline (mantido sem alteração)
    ├── data/       # base original do Kaggle
    ├── notebooks/  # notebooks de tratamento e análise
    └── frente2/    # script e saídas da análise de reviews
```

## Como usar

1. Gerar os dados: na pasta `pipeline/`, `pip install -r requirements.txt` e `python run.py`.
   Detalhes em [pipeline/README.md](pipeline/README.md).
2. Abrir o dashboard em `dashboard/` e, em Transformar dados > Gerenciar Parâmetros, apontar o parâmetro
   `PastaDados` para a pasta `pipeline\data\processed\` do seu clone (com a barra no final).
