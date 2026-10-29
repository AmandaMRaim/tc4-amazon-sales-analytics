"""
Tratamento da base de produtos (Frente 1).

Codigo extraido do notebook notebooks/TC4fase.ipynb, sem mudanca de logica:
limpa precos, desconto, nota e quantidade de avaliacoes, separa a
categoria em niveis e remove produtos duplicados.

Saida: amazon_sales_cleaned.csv (1 linha por produto).
"""

import pandas as pd


def limpar_precos(df):
    df["discounted_price"] = (
        df["discounted_price"]
        .str.replace("₹", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    df["actual_price"] = (
        df["actual_price"]
        .str.replace("₹", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    df["discounted_price"] = pd.to_numeric(
        df["discounted_price"],
        errors="coerce"
    )

    df["actual_price"] = pd.to_numeric(
        df["actual_price"],
        errors="coerce"
    )
    return df


def limpar_desconto(df):
    df["discount_percentage"] = (
        df["discount_percentage"]
        .str.replace("%", "", regex=False)
        .str.strip()
    )

    df["discount_percentage"] = pd.to_numeric(
        df["discount_percentage"],
        errors="coerce"
    )
    return df


def limpar_avaliacoes(df):
    df["rating"] = pd.to_numeric(
        df["rating"],
        errors="coerce"
    )

    df["rating_count"] = (
        df["rating_count"]
        .str.replace(",", "", regex=False)
        .str.strip()
    )

    df["rating_count"] = pd.to_numeric(
        df["rating_count"],
        errors="coerce"
    )
    return df


def enriquecer(df):
    categorias_df = df["category"].str.split("|", expand=True)
    categorias_df.columns = [f"categoria_{i+1}" for i in range(categorias_df.shape[1])]
    df = pd.concat([df, categorias_df], axis=1)

    df["rating_count"] = df["rating_count"].fillna(0)

    df["discount_amount"] = df["actual_price"] - df["discounted_price"]

    df = df.drop_duplicates(subset=["product_id"]).reset_index(drop=True)
    return df


def executar(arq_entrada, arq_saida):
    df = pd.read_csv(arq_entrada)
    print("Linhas:", df.shape[0])
    print("Colunas:", df.shape[1])

    df = limpar_precos(df)
    df = limpar_desconto(df)
    df = limpar_avaliacoes(df)
    df = enriquecer(df)

    arq_saida.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(arq_saida, index=False)
    print(f"Arquivo '{arq_saida.name}' gerado com sucesso! Total de linhas únicas: {len(df)}")
    return df
