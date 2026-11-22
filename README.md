# Estudo-de-ocorrencia-de-infeccoes-por-Helicobacter-em-mamiferos-aquaticos-no-Brasil
## Sobre o Projeto

* **Autora:** Carolina Carvalho Dipold
* **Orientação:** Profa. Dra. Lara Borges Keid
* **Instituição:** Faculdade de Zootecnia e Engenharia de Alimentos – Universidade de São Paulo (FZEA/USP)
* **Laboratório:** Laboratório de Soroepidemiologia Veterinária (FZEA/USP)
* **Financiamento:** Fundação de Amparo à Pesquisa do Estado de São Paulo (FAPESP) – Processo nº 2025/21466-5

---

## Estrutura dos Scripts

Todos os scripts utilizam como arquivo de entrada a base consolidada `dados_geograficos_com_PCR.csv`, contendo as colunas `Latitude`, `Longitude`, `Data da ocorrência`, `Ordem` e `PCR_Positivo` (`1` = positivo; `0` = negativo).

| Script | Descrição | Arquivos Gerados |
| :--- | :--- | :--- |
| `01_mapa_distribuicao_espacial.py` | Gera o mapa de distribuição espacial dos indivíduos avaliados (negativos vs. positivos) destacando os 6 estados amostrados (`BA`, `CE`, `RJ`, `SC`, `SP`, `SE`) a partir da API oficial do IBGE (`EPSG:4674`). | `mapa_distribuicao_helicobacter_brasil_ABNT.png` |
| `02_sazonalidade_por_ordem.py` | Classifica as ocorrências nas estações astronômicas do Hemisfério Sul e gera o painel comparativo estratificado entre **Cetáceos (*Cetartiodactyla*)** e **Pinípedes (*Carnivora*)**. | `sazonalidade_estratificada_por_ordem.csv`<br>`grafico_sazonalidade_cetaceos_vs_pinipedes_ABNT.png` |
| `03_sazonalidade_mensal_estacao.py` | Agrupa os registros por estação do ano e por mês (Jan–Dez) e gera o painel duplo de barras empilhadas com taxas de positividade. | `resumo_sazonal_estacoes.csv`<br>`resumo_sazonal_meses.csv`<br>`painel_sazonalidade_helicobacter_ABNT.png` |

---

## Pré-requisitos e Instalação

Os códigos foram desenvolvidos em **Python 3.15.2**. Antes de executar os scripts, instale as bibliotecas necessárias via terminal:

```bash
pip install pandas numpy matplotlib geopandas shapely


Declaração de Uso de Inteligência Artificial (IA)
Em conformidade com as boas práticas de integridade científica e transparência na pesquisa:

Ferramenta utilizada: Google Gemini (Versão 4 Neon).

Finalidade de uso: Os scripts em Python contidos neste repositório foram gerados e refinados com o auxílio de Inteligência Artificial generativa para estruturação de código, limpeza de dados tabulares, integração com a API do IBGE e formatação gráfica em padrão ABNT.

Supervisão e responsabilidade: Todo o delineamento metodológico, definição das variáveis epidemiológicas, curadoria dos dados biológicos/geográficos, validação dos cálculos e conferência integral dos resultados (tabelas e figuras geradas) foram realizados e verificados pela autora, que assume total responsabilidade pela precisão científica do conteúdo apresentado.

Disponibilidade dos Dados
Os dados brutos utilizados nas análises (dados_geograficos_com_PCR.csv) não estão disponibilizados publicamente neste repositório por conterem registros vinculados ao projeto em andamento e/ou convênios de monitoramento, podendo ser solicitados mediante contato com a autora.

Licença
Este projeto está licenciado sob a licença [MIT] — consulte o arquivo LICENSE para mais detalhes.

Contato
Para dúvidas ou solicitações relacionadas aos scripts e análises, entre em contato pelo e-mail: [carolinacdipold@usp.br].
