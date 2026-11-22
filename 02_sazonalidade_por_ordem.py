'''Função gerada com auxílio do Google Gemini (modelo 4 Neon) em nov/2026
Prompt base: Não sei programar em Python, mas preciso criar um painel comparativo de gráficos de sazonalidade em alta resolução para um relatório científico (padrão ABNT, fonte Times New Roman) a partir da minha planilha (dados_geograficos_com_PCR.csv).
A planilha tem as colunas:
Data da ocorrência (no formato brasileiro dia/mês/ano);
Ordem (com registros de Cetáceos/Cetartiodactyla e Pinípedes/Carnivora);
PCR_Positivo (1 para positivo e 0 para negativo).
O código precisa fazer duas coisas:
Classificar as datas nas 4 estações do ano do Hemisfério Sul (Verão, Outono, Inverno e Primavera, nessa ordem) e salvar uma tabela resumo em CSV mostrando, para cada grupo e estação, o total avaliado, quantos foram positivos, quantos foram negativos e a porcentagem de positivos.
Gerar  dois gráficos de barras empilhadas lado a lado (um para Cetáceos (Cetartiodactyla) e outro para Pinípedes (Carnivora)), com as seguintes características:
Mesma escala no eixo vertical (Y) nos dois gráficos para facilitar a comparação.
Barras em azul claro para Negativos (embaixo) e vermelho para Positivos (em cima), com o rótulo positivos/total e a porcentagem (%) escritos no topo de cada barra.
Visual limpo (sem as linhas de borda de cima e da direita), título geral no topo ("Distribuição sazonal de mamíferos aquáticos avaliados e positividade para Helicobacter spp. por Ordem"), nomes nos eixos ("Estação do ano" e "Número de indivíduos (n)") e legenda no canto superior direito.
Gere o código completo pronto para copiar e colar, me explique o que instalar para rodar e salve o gráfico como uma imagem PNG pronta para o Word.'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ==============================================================================
# 1. CONFIGURAÇÃO TIPOGRÁFICA ABNT (Times New Roman)
# ==============================================================================
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

# ==============================================================================
# 2. CARREGAR DADOS E PREPARAR GRUPOS TAXONÔMICOS E ESTAÇÕES
# ==============================================================================
arquivo = 'dados_geograficos_com_PCR.csv'

try:
    df = pd.read_csv(arquivo, sep=None, engine='python', encoding='utf-8-sig')
except UnicodeDecodeError:
    df = pd.read_csv(arquivo, sep=None, engine='python', encoding='latin1')

df.columns = df.columns.str.strip()

# Padroniza o grupo taxonômico a partir da coluna 'Ordem'
def classificar_grupo(ordem):
    if pd.isna(ordem):
        return 'Não informado'
    o = str(ordem).strip().lower()
    if 'cetacea' in o or 'cetartiodactyla' in o:
        return 'Cetáceos (Cetartiodactyla)'
    elif 'carnivora' in o or 'pinnipedia' in o:
        return 'Pinípedes (Carnivora)'
    else:
        return str(ordem).strip()

df['Grupo_Taxonomico'] = df['Ordem'].apply(classificar_grupo)

# Converte a data e classifica as estações (Hemisfério Sul)
df['Data_dt'] = pd.to_datetime(df['Data da ocorrência'], dayfirst=True, errors='coerce')

def classificar_estacao_sul(data):
    if pd.isna(data):
        return 'Não informado'
    mes, dia = data.month, data.day
    if (mes == 3 and dia >= 20) or (mes in [4, 5]) or (mes == 6 and dia < 21):
        return 'Outono'
    elif (mes == 6 and dia >= 21) or (mes in [7, 8]) or (mes == 9 and dia < 23):
        return 'Inverno'
    elif (mes == 9 and dia >= 23) or (mes in [10, 11]) or (mes == 12 and dia < 21):
        return 'Primavera'
    else:
        return 'Verão'

df['Estacao'] = df['Data_dt'].apply(classificar_estacao_sul)
df_valido = df[df['Estacao'] != 'Não informado'].copy()

# ==============================================================================
# 3. TABELA CRUZADA: GRUPO TAXONÔMICO x ESTAÇÃO DO ANO
# ==============================================================================
ordem_estacoes = ['Verão', 'Outono', 'Inverno', 'Primavera']
grupos = ['Cetáceos (Cetartiodactyla)', 'Pinípedes (Carnivora)']

tab_estratificada = (
    df_valido.groupby(['Grupo_Taxonomico', 'Estacao'])
    .agg(
        Total_Avaliados=('PCR_Positivo', 'count'),
        Positivos_n=('PCR_Positivo', 'sum')
    )
    .reset_index()
)

tab_estratificada['Negativos_n'] = tab_estratificada['Total_Avaliados'] - tab_estratificada['Positivos_n']
tab_estratificada['Positivos (%)'] = np.where(
    tab_estratificada['Total_Avaliados'] > 0,
    (tab_estratificada['Positivos_n'] / tab_estratificada['Total_Avaliados'] * 100).round(1),
    0.0
)

# Ordena de forma limpa e exporta CSV
tab_estratificada['Estacao'] = pd.Categorical(tab_estratificada['Estacao'], categories=ordem_estacoes, ordered=True)
tab_estratificada = tab_estratificada.sort_values(['Grupo_Taxonomico', 'Estacao'])
tab_estratificada.to_csv('sazonalidade_estratificada_por_ordem.csv', index=False, sep=';', encoding='utf-8-sig')

print("--- SAZONALIDADE ESTRATIFICADA POR GRUPO TAXONÔMICO ---")
print(tab_estratificada.to_string(index=False))

# ==============================================================================
# 4. GRÁFICO COMPARATIVO LADO A LADO (COM TÍTULO E EIXOS COMPLETOS)
# ==============================================================================
fig, axes = plt.subplots(1, 2, figsize=(12, 5.2), dpi=300)

# Título geral do gráfico
fig.suptitle(
    'Distribuição sazonal de mamíferos aquáticos avaliados e positividade para Helicobacter spp. por Ordem',
    fontsize=12, fontweight='bold', y=0.98
)

max_y = tab_estratificada['Total_Avaliados'].max() * 1.25

for idx, grupo in enumerate(grupos):
    ax = axes[idx]
    sub = tab_estratificada[tab_estratificada['Grupo_Taxonomico'] == grupo].set_index('Estacao').reindex(ordem_estacoes).fillna(0)
    
    x = np.arange(len(ordem_estacoes))
    ax.bar(x, sub['Negativos_n'], color='#a6bddb', edgecolor='#333333', linewidth=0.6, label='Negativo')
    ax.bar(x, sub['Positivos_n'], bottom=sub['Negativos_n'], color='#d92b2b', edgecolor='#333333', linewidth=0.6, label='Positivo')
    
    for i, est in enumerate(ordem_estacoes):
        tot = int(sub.loc[est, 'Total_Avaliados'])
        pos = int(sub.loc[est, 'Positivos_n'])
        pct = sub.loc[est, 'Positivos (%)']
        if tot > 0:
            ax.text(i, tot + 0.4, f"{pos}/{tot}\n({pct:.1f}%)", ha='center', va='bottom', fontsize=8.5)
            
    ax.set_title(grupo, fontsize=11, fontweight='bold', pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(ordem_estacoes, fontsize=10)
    ax.set_xlabel('Estação do ano', fontsize=10.5, labelpad=6)
    ax.set_ylabel('Número de indivíduos (n)', fontsize=10.5, labelpad=6)
    ax.set_ylim(0, max_y)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    if idx == 1:
        ax.legend(frameon=False, fontsize=9.5, loc='upper right')

plt.tight_layout(rect=[0, 0, 1, 0.93])
plt.savefig('grafico_sazonalidade_cetaceos_vs_pinipedes_ABNT.png', dpi=300, bbox_inches='tight')
plt.show()
print("✅ Arquivos salvos: 'sazonalidade_estratificada_por_ordem.csv' e 'grafico_sazonalidade_cetaceos_vs_pinipedes_ABNT.png'")
