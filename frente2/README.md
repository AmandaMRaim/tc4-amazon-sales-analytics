# Frente 2: Customer Insights

Transforma os reviews do dataset em uma linha por review, classifica o sentimento e marca os temas citados. As saídas alimentam a página **Customer Insights** e a matriz de segmentação da Frente 3.

## Como rodar

A partir da raiz do repositório:

```bash
pip install pandas vaderSentiment
python frente2/scripts/frente2_reviews.py data/amazon.csv
```

Funciona com o `amazon.csv` original do Kaggle ou com o `amazon_sales_cleaned.csv` do notebook. O script usa só `product_id` e as colunas de review, e remove produtos duplicados com o mesmo critério do notebook (1.351 produtos).

## Arquivos de saída (`frente2/saidas/`)

### `fReviews.csv`: 1 linha por produto x review (10.598 linhas)

| Coluna | Tipo | Descrição |
|---|---|---|
| review_key | texto | Chave única da linha: `product_id_review_id` |
| product_id | texto | Liga com `amazon_sales_cleaned[product_id]` |
| review_id | texto | ID do review na Amazon |
| user_id | texto | ID do autor |
| review_title | texto | Título do review |
| review_content | texto | Texto do review (vazio quando não deu para separar, ver limitações) |
| texto_analise | texto | Título + conteúdo, sem links. É o texto que passou pelo VADER |
| tem_texto | verdadeiro/falso | Falso quando o review não tem texto (só imagem) |
| titulo_alinhado | verdadeiro/falso | Se o título foi separado com segurança |
| conteudo_alinhado | verdadeiro/falso | Se o conteúdo foi separado com segurança |
| score | decimal (-1 a 1) | Score composto do VADER |
| sentimento | texto | `Positivo` (score ≥ 0,05), `Negativo` (≤ -0,05), `Neutro` ou `Sem texto` |

### `fReviewTema.csv`: 1 linha por review x tema citado

| Coluna | Tipo | Descrição |
|---|---|---|
| review_key | texto | Liga com `fReviews[review_key]` |
| tema | texto | Um dos temas de `dicionario_temas.csv` |

Um review pode citar vários temas, ou nenhum (cerca de 1/3 não cita nenhum).

### `sentimento_por_produto.csv`: 1 linha por produto (entrega para a Frente 3)

`product_id`, `qtd_reviews_texto`, `score_medio`, `pct_positivos`, `pct_negativos`, `saldo_sentimento` (= % positivos − % negativos).

Formato de todos os arquivos: separador vírgula, textos entre aspas quando necessário, decimal com ponto, UTF-8.

## Importando no Power BI

1. **Obter dados → Texto/CSV**, escolha o arquivo.
2. No Power Query, confira na etapa **Fonte** que está `QuoteStyle=QuoteStyle.Csv`. Com `QuoteStyle.None` os textos com vírgula quebram as colunas.
3. Converta `score` e as colunas de % com **Alterar Tipo → Usando a Localidade → Número decimal / Inglês (Estados Unidos)**. Sem isso, o Power BI em pt-BR lê `0.72` como 72.
4. Relacionamentos:
   - `amazon_sales_cleaned[product_id]` 1 → * `fReviews[product_id]`
   - `fReviews[review_key]` 1 → * `fReviewTema[review_key]`
   - `amazon_sales_cleaned[product_id]` 1 → 1 `sentimento_por_produto[product_id]`

## Por que a granularidade é produto x review

A Amazon compartilha os reviews entre variações do mesmo produto (cor, tamanho). Dos 9.263 reviews únicos, 760 aparecem em mais de um produto. Manter uma linha por produto x review deixa o filtro por produto e categoria funcionando direto. Para contar reviews sem duplicar, use `DISTINCTCOUNT(fReviews[review_id])`.

## Como os reviews foram separados

No dataset, os reviews de cada produto vêm concatenados por vírgula **sem espaço** (`Bom produto,Chegou rápido`), enquanto as vírgulas do próprio texto quase sempre têm espaço depois. O script divide por "vírgula seguida de algo que não é espaço" e, quando sobram pedaços, junta ao anterior os que começam com minúscula (continuação de frase). Resultado: título alinhado em 99,5% das linhas e conteúdo em 92,1%.

## Temas

Definidos em `dicionario_temas.csv` (tema, termo). A busca ignora maiúsculas e considera palavra inteira. Para ajustar, basta editar o CSV e rodar o script de novo, sem mexer no código.

## Limitações (vale citar no vídeo)

- **O sentimento é do review inteiro, não do tema.** Um review "bonito, mas parou em 2 meses" pode sair negativo e ser marcado em Design e em Durabilidade. A leitura correta é "reviews que citam X têm Y% de sentimento negativo".
- **VADER é um modelo de léxico em inglês.** Funciona bem para textos curtos de consumidor, mas erra com ironia, gírias e mistura de idiomas (hinglish).
- **8% dos conteúdos não puderam ser separados com segurança.** Nesses casos o conteúdo fica vazio e a análise usa só o título.
- **A nota (`rating`) é média do produto**, não de cada review. Não existe nota por review no dataset.
