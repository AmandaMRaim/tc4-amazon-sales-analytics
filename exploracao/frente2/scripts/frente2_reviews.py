"""
Tech Challenge Fase 4 - Frente 2 (Customer Insights)

Transforma os reviews agrupados do dataset Amazon Sales (Kaggle) em
uma linha por review, calcula o sentimento (VADER) e marca os temas
citados em cada review a partir do dicionario em dicionario_temas.csv.

Uso (a partir da raiz do repositorio):
    pip install pandas vaderSentiment
    python frente2/scripts/frente2_reviews.py data/amazon.csv

Aceita tanto o amazon.csv original quanto o amazon_sales_cleaned.csv
gerado pelo notebook: so usa product_id e as colunas de review.

Saidas em frente2/saidas/:
    fReviews.csv                 1 linha por produto x review
    fReviewTema.csv              1 linha por review x tema citado
    sentimento_por_produto.csv   1 linha por produto (entrega p/ Frente 3)
"""

import re
import sys
from pathlib import Path

import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

PASTA_FRENTE2 = Path(__file__).resolve().parents[1]
PASTA_SAIDAS = PASTA_FRENTE2 / "saidas"
ARQ_DICIONARIO = PASTA_FRENTE2 / "dicionario_temas.csv"

# Os reviews de um produto vem concatenados por virgula SEM espaco
# ("Bom produto,Chegou rapido"). Virgulas do proprio texto quase sempre
# vem seguidas de espaco ("rapido, bom"). Por isso o separador e
# "virgula seguida de algo que nao seja espaco".
SEPARADOR = re.compile(r",(?=\S)")
URL = re.compile(r"https?://\S+")

LIMIAR_POSITIVO = 0.05   # regra padrao do VADER
LIMIAR_NEGATIVO = -0.05


def dividir_alinhado(texto, n_esperado):
    """Divide o texto agrupado em n_esperado pedacos.

    Retorna (lista_de_pedacos, alinhado). Quando a divisao gera pedacos
    a mais, junta as continuacoes (pedaco que comeca com minuscula ou
    pontuacao) ao pedaco anterior ate bater a quantidade. Se mesmo assim
    nao bater, devolve alinhado=False e quem chamou decide o que fazer.
    """
    pedacos = SEPARADOR.split(str(texto))
    if len(pedacos) == n_esperado:
        return pedacos, True

    while len(pedacos) > n_esperado:
        candidatos = [
            i for i in range(1, len(pedacos))
            if not pedacos[i][:1].isupper() and not pedacos[i].startswith("http")
        ]
        if not candidatos:
            break
        # junta primeiro a continuacao mais curta, que e a mais provavel
        i = min(candidatos, key=lambda k: len(pedacos[k]))
        pedacos[i - 1] = pedacos[i - 1] + "," + pedacos[i]
        del pedacos[i]

    return pedacos, len(pedacos) == n_esperado


def explodir_reviews(df):
    linhas = []
    for _, r in df.iterrows():
        ids = str(r["review_id"]).split(",")
        users = str(r["user_id"]).split(",")
        n = len(ids)
        titulos, tit_ok = dividir_alinhado(r["review_title"], n)
        conteudos, cont_ok = dividir_alinhado(r["review_content"], n)

        for i, rid in enumerate(ids):
            titulo = titulos[i] if tit_ok else ""
            conteudo = conteudos[i] if cont_ok else ""
            linhas.append({
                "product_id": r["product_id"],
                "review_id": rid,
                "user_id": users[i] if len(users) == n else "",
                "review_title": titulo.strip(),
                "review_content": conteudo.strip(),
                "titulo_alinhado": tit_ok,
                "conteudo_alinhado": cont_ok,
            })
    out = pd.DataFrame(linhas)

    # Texto usado na analise: titulo + conteudo, sem links de imagem
    # e sem quebras de linha (evita problemas na importacao do CSV)
    texto = (out["review_title"] + ". " + out["review_content"]).str.replace(URL, " ", regex=True)
    out["texto_analise"] = texto.str.replace(r"\s+", " ", regex=True).str.strip(" .")
    for col in ["review_title", "review_content"]:
        out[col] = out[col].str.replace(r"\s+", " ", regex=True)

    out["tem_texto"] = out["texto_analise"].str.len() > 0
    out.insert(0, "review_key", out["product_id"] + "_" + out["review_id"])
    return out


def classificar_sentimento(out):
    vader = SentimentIntensityAnalyzer()
    out["score"] = [
        round(vader.polarity_scores(t)["compound"], 4) if t else None
        for t in out["texto_analise"]
    ]

    def rotulo(s):
        if pd.isna(s):
            return "Sem texto"
        if s >= LIMIAR_POSITIVO:
            return "Positivo"
        if s <= LIMIAR_NEGATIVO:
            return "Negativo"
        return "Neutro"

    out["sentimento"] = out["score"].apply(rotulo)
    return out


def marcar_temas(out):
    dic = pd.read_csv(ARQ_DICIONARIO)
    padroes = {
        tema: re.compile(r"\b(" + "|".join(re.escape(p.strip().lower()) for p in grupo["termo"]) + r")\b")
        for tema, grupo in dic.groupby("tema")
    }
    linhas = []
    textos = out["texto_analise"].str.lower()
    for chave, texto in zip(out["review_key"], textos):
        for tema, padrao in padroes.items():
            if padrao.search(texto):
                linhas.append({"review_key": chave, "tema": tema})
    return pd.DataFrame(linhas, columns=["review_key", "tema"])


def resumo_por_produto(out):
    com_texto = out[out["tem_texto"]]
    g = com_texto.groupby("product_id")
    res = pd.DataFrame({
        "qtd_reviews_texto": g.size(),
        "score_medio": g["score"].mean().round(4),
        "pct_positivos": g["sentimento"].apply(lambda s: (s == "Positivo").mean()).round(4),
        "pct_negativos": g["sentimento"].apply(lambda s: (s == "Negativo").mean()).round(4),
    })
    res["saldo_sentimento"] = (res["pct_positivos"] - res["pct_negativos"]).round(4)
    return res.reset_index()


def main():
    if len(sys.argv) < 2:
        sys.exit("Informe o caminho do CSV. Ex.: python frente2/scripts/frente2_reviews.py data/amazon.csv")

    df = pd.read_csv(sys.argv[1])
    # mesmo criterio do notebook do grupo: 1 linha por produto
    df = df.drop_duplicates(subset=["product_id"]).reset_index(drop=True)

    out = classificar_sentimento(explodir_reviews(df))
    temas = marcar_temas(out)
    produto = resumo_por_produto(out)

    PASTA_SAIDAS.mkdir(parents=True, exist_ok=True)
    colunas = ["review_key", "product_id", "review_id", "user_id", "review_title",
               "review_content", "texto_analise", "tem_texto", "titulo_alinhado",
               "conteudo_alinhado", "score", "sentimento"]
    out[colunas].to_csv(PASTA_SAIDAS / "fReviews.csv", index=False, encoding="utf-8")
    temas.to_csv(PASTA_SAIDAS / "fReviewTema.csv", index=False, encoding="utf-8")
    produto.to_csv(PASTA_SAIDAS / "sentimento_por_produto.csv", index=False, encoding="utf-8")

    # Resumo no terminal para conferencia
    print(f"Produtos: {df['product_id'].nunique()}")
    print(f"Linhas produto x review: {len(out)} | reviews unicos: {out['review_id'].nunique()}")
    print(f"Titulo alinhado: {out['titulo_alinhado'].mean():.1%} | conteudo alinhado: {out['conteudo_alinhado'].mean():.1%}")
    print(f"Sem texto para analisar: {(~out['tem_texto']).sum()}")
    print("\nSentimento (reviews unicos):")
    print(out.drop_duplicates("review_id")["sentimento"].value_counts(normalize=True).round(3))
    print(f"\nMarcacoes de tema: {len(temas)} | reviews com ao menos 1 tema: "
          f"{temas['review_key'].nunique() / len(out):.1%}")
    print(temas["tema"].value_counts())


if __name__ == "__main__":
    main()
