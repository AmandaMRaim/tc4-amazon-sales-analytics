# Frente 2: Customer Insights (resumo de entrega)

Este documento reúne o que a Frente 2 fez, o que descobriu e o que cada parte do grupo precisa saber para o dashboard, a página de Recomendações e o vídeo.

**Em uma frase:** o cliente elogia o preço e a qualidade na hora da compra, mas se frustra quando o produto quebra e o pós-venda não resolve, e a nota média não mostra esse problema.

---

## 1. O que foi feito

O PDF pede que a equipe *"explore os conteúdos das avaliações dos consumidores"* para mostrar *"como os comentários podem complementar os indicadores quantitativos"*. Como o Power BI não analisa texto livre, os comentários foram transformados em dados:

1. **Separação dos reviews.** Na base, cada produto tem até 8 reviews na mesma célula. Eles foram separados em uma linha por review (9.263 reviews únicos de 1.351 produtos).
2. **Sentimento.** Cada review foi classificado como Positivo, Negativo ou Neutro com o **VADER**, uma ferramenta gratuita feita para textos curtos de consumidores. Ela dá a cada texto uma nota de -1 (muito negativo) a +1 (muito positivo).
3. **Temas.** Um dicionário de palavras-chave marca sobre o que cada review fala (13 temas, como custo-benefício, qualidade, durabilidade e entrega).
4. **Resumo por produto.** Para cada produto: % de reviews positivos e negativos e o saldo de sentimento (positivos menos negativos).

Fonte do VADER: Hutto, C.J. & Gilbert, E.E. (2014). *VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text*. ICWSM-14.

## 2. Números principais

| Indicador | Valor |
|---|---|
| Reviews analisados | 9.263 únicos |
| Positivos | 82,5% |
| Negativos | 10,0% |
| Neutros | 7,4% |
| Reviews que citam ao menos 1 tema | 66% |

## 3. Conclusões para a página Customer Insights

### Conclusão 1: o cliente valoriza preço justo, qualidade e facilidade de uso

- Nos reviews positivos, os temas mais citados são **custo-benefício (28%)** e **qualidade (21%)**.
- **Facilidade de uso** é o tema mais seguro: **91%** dos reviews que falam dele são positivos.

> *"Easy to use. Easy to clean. Easy to maintain. Good product. Value for money must recommend to everyone."*
> "Fácil de usar. Fácil de limpar. Fácil de manter. Bom produto. Vale o preço, recomendo a todos." (fritadeira elétrica)

### Conclusão 2: o maior problema aparece depois da compra

- **Durabilidade e defeitos** é o assunto nº 1 das reclamações: está em **22%** dos reviews negativos.
- **25%** dos reviews que citam durabilidade são negativos, mais que o dobro da média (10%).
- **Atendimento e garantia** vem logo atrás, com **23%** de reviews negativos.
- As reclamações de durabilidade se concentram em **controles remotos, aquecedores elétricos, power banks, liquidificadores e ferros de passar** (entre 4% e 6% dos reviews dessas subcategorias, contra 2% na média).

> *"[Didn't] work even 3 months, as well as seller is not supporting in warranty."*
> "[Não] funcionou nem 3 meses, e o vendedor não dá suporte na garantia." (aquecedor de água)

### Conclusão 3: a nota alta pode esconder problemas

- **No geral, nota e texto concordam:** produtos com as notas mais baixas (até 3,9) têm **17%** de reviews negativos, e os com as notas mais altas (acima de 4,3) têm **6%**.
- **Mas há exceções:** **99 produtos** têm nota igual ou acima da mediana (4,1) e **25% ou mais** de reviews negativos.
- Exemplo: o fone **boAt Bassheads 225** tem nota 4,1 e 273 mil avaliações, mas 3 dos seus 8 reviews são reclamações.

> *"Good buy but 1 side earphone stopped after 6-7 months."*
> "Boa compra, mas um lado do fone parou depois de 6-7 meses." (fone boAt Bassheads 225)

**Mensagem:** olhar só a nota média não basta. O texto dos reviews revela riscos que o número esconde.

## 4. Para a Frente 3 (Preços, Estratégia e Recomendações)

### Dado disponível

`pipeline/data/processed/sentimento_por_produto.csv`: uma linha por produto, com `pct_positivos`, `pct_negativos` e `saldo_sentimento` (de -1 a +1). Liga com a tabela de produtos pelo `product_id`.

### Conclusão 4: desconto maior não traz cliente mais satisfeito

| Faixa de desconto | Produtos | Saldo de sentimento | % negativos |
|---|---|---|---|
| 0% a 20% | 176 | 0,75 | 8,6% |
| 21% a 40% | 329 | 0,73 | 10,0% |
| 41% a 60% | 469 | 0,71 | 10,7% |
| Acima de 60% | 376 | 0,75 | 9,3% |

O sentimento é praticamente o mesmo em todas as faixas (correlação entre desconto e saldo de sentimento: -0,02, ou seja, nenhuma relação).

### Sugestões de recomendação

1. **Revisar fornecedores e políticas de garantia** nas subcategorias com mais reclamações de durabilidade (controles remotos, aquecedores, power banks, liquidificadores e ferros de passar).
2. **Usar o sentimento dos reviews como alerta precoce:** monitorar produtos com nota boa e muitas reclamações antes que a nota caia.
3. **Fortalecer o pós-venda:** atendimento e garantia têm mais que o dobro de reclamações da média.
4. **Não usar desconto como alavanca de satisfação:** ele não muda a percepção do cliente sobre o produto.

## 5. Para a página Customer Insights no Power BI

A página já cobre as conclusões 1 a 3. Dois ajustes sugeridos:

- **Subcategoria mais detalhada.** O visual "Sentimento por subcategoria" usa `categoria_2`, um nível amplo. Para mostrar onde estão os problemas de durabilidade, crie esta coluna calculada na tabela `amazon_sales_cleaned` e use-a no eixo:

  ```
  Subcategoria = PATHITEM(amazon_sales_cleaned[category], PATHLENGTH(amazon_sales_cleaned[category]))
  ```

  Ela pega o último nível da categoria (ex.: de `Home&Kitchen|Heating|ElectricHeaters`, devolve `ElectricHeaters`).

- **Caixas de texto** com as três conclusões e os três trechos acima.

## 6. Validação e limitações

### Validação

Uma amostra de 30 reviews (10 de cada classificação) foi conferida manualmente:

| Classificação do VADER | Acertos |
|---|---|
| Positivo | 10 de 10 (100%) |
| Negativo | 9 de 10 (90%) |
| Neutro | 4 de 10 (40%) |

Os erros se concentram nos neutros: reviews sem palavras de emoção, como "fast charge" (elogio) ou "não recebi o cartão de garantia" (reclamação). Como os neutros são só 7% da base, a taxa de acerto estimada para a base toda fica em torno de 94%.

O dicionário de temas também foi revisado: duas palavras que geravam marcações erradas ("range", de "price range", e "power", de "suction power") foram corrigidas.

### Limitações

- **No máximo 8 reviews por produto.** Os números por produto são indicativos. Os números gerais são mais sólidos.
- **O sentimento é do review inteiro, não do tema.** Um review "bonito, mas quebrou" conta para os dois temas. A leitura correta é "reviews que citam X têm Y% de negativos".
- **VADER erra quando não há palavras de emoção**, e também com ironia e mistura de idiomas.
- **8% dos textos não puderam ser separados com segurança.** Nesses casos, a análise usa só o título do review.
- **A nota (`rating`) é a média do produto.** Não existe nota por review na base.

## 7. Frase para o vídeo

> "Validamos manualmente uma amostra de 30 reviews. A ferramenta acertou 100% dos positivos e 90% dos negativos. Os erros se concentram nos neutros, que são apenas 7% da base."

## 8. Onde estão os arquivos

| O quê | Onde |
|---|---|
| Código que gera os dados de reviews | `pipeline/src/reviews.py` |
| Dicionário de temas | `pipeline/data/reference/dicionario_temas.csv` |
| Dados usados pelo Power BI | `pipeline/data/processed/` (`fReviews.csv`, `fReviewTema.csv`, `sentimento_por_produto.csv`) |
| Trabalho original e notebook didático | `exploracao/frente2/` e `exploracao/notebooks/frente2_reviews.ipynb` |
