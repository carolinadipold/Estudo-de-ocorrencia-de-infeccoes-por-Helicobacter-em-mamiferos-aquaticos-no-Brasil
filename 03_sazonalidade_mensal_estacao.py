'''Função gerada com auxílio do Google Gemini (modelo 4 Neon) em nov/2026
Prompt base: Preciso criar com o Python um painel com dois gráficos de sazonalidade lado a lado em alta resolução para um relatório científico (padrão ABNT, fonte Times New Roman) usando os dados da minha planilha (dados_geograficos_com_PCR.csv).
A planilha tem as colunas:
Data da ocorrência (no formato brasileiro dia/mês/ano);
PCR_Positivo (1 para positivo e 0 para negativo).
O código precisa fazer duas coisas:
Extrair o mês e classifique as datas nas 4 estações do ano do Hemisfério Sul (usando as datas astronômicas exatas, na ordem Verão, Outono, Inverno e Primavera) e salvar duas tabelas resumo em CSV - uma por estação do ano e outra com todos os 12 meses (de Jan a Dez, mesmo se algum mês tiver zero amostras) - contendo o total avaliado, positivos, negativos e a porcentagem de positivos.
Gerar dois gráficos de barras empilhadas lado a lado (Painel A: por Estação do Ano; Painel B: por Mês):
Barras em azul claro para Negativos (embaixo) e vermelho para Positivos (em cima).
No gráfico de Estações do Ano, escreva positivos/total e a porcentagem (%) no topo de cada barra, com a legenda no canto superior direito.
No gráfico Mensal, mostre os 12 meses abreviados (Jan a Dez) e destaque apenas o número de positivos em vermelho escuro e negrito no topo das barras que tiverem casos positivos.
Visual limpo (sem as linhas de borda de cima e da direita), título geral no topo ("Distribuição sazonal de mamíferos aquáticos avaliados e positividade para Helicobacter spp."), nomes nos eixos ("Estação do ano" e "Número de indivíduos (n)") e legenda no canto superior direito.
Por favor, gere o código completo pronto para copiar e colar, me diga o que preciso instalar para rodar e salve o painel como uma imagem PNG pronta para colar no Word.'''

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
plt.rcParams['mathtext.fontset'] = 'custom'
plt.rcParams['mathtext.rm'] = 'Times New Roman'
plt.rcParams['mathtext.it'] = 'Times New Roman:italic'
plt.rcParams['mathtext.bfit'] = 'Times New Roman:italic:bold'

# ==============================================================================
# 2. CARREGAR A PLANILHA E CONVERTER AS DATAS
# ==============================================================================
arquivo = 'dados_geograficos_com_PCR.csv'

# Detecta automaticamente o separador (vírgula ou ponto e vírgula) e a codificação
try:
    df = pd.read_csv(arquivo, sep=None, engine='python', encoding='utf-8-sig')
except UnicodeDecodeError:
    df = pd.read_csv(arquivo, sep=None, engine='python', encoding='latin1')

df.columns = df.columns.str.strip()

# Garante que PCR_Positivo seja numérico (1 = Positivo, 0 = Negativo)
df['PCR_Positivo'] = pd.to_numeric(df['PCR_Positivo'], errors='coerce').fillna(0).astype(int)

# Converte a data no formato brasileiro (dia/mês/ano)
df['Data_dt'] = pd.to_datetime(df['Data da ocorrência'], dayfirst=True, errors='coerce')

print(f"Total de registros lidos: {len(df)} | Datas válidas: {df['Data_dt'].notna().sum()}")

# ==============================================================================
# 3. EXTRAIR MÊS E CLASSIFICAR ESTAÇÕES DO ANO (HEMISFÉRIO SUL - ASTRONÔMICO)
# ==============================================================================
df['Mes_Num'] = df['Data_dt'].dt.month

nomes_meses = {
    1: 'Jan', 2: 'Fev', 3: 'Mar', 4: 'Abr', 5: 'Mai', 6: 'Jun',
    7: 'Jul', 8: 'Ago', 9: 'Set', 10: 'Out', 11: 'Nov', 12: 'Dez'
}
df['Mes'] = df['Mes_Num'].map(nomes_meses)

def classificar_estacao_sul(data):
    if pd.isna(data):
        return 'Não informado'
    mes = data.month
    dia = data.day

    # Datas astronômicas exatas para o Hemisfério Sul:
    # Outono: 20/mar a 20/jun | Inverno: 21/jun a 22/set
    # Primavera: 23/set a 20/dez | Verão: 21/dez a 19/mar
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
# 4. GERAR E SALVAR AS TABELAS RESUMO EM CSV
# ==============================================================================
ordem_estacoes = ['Verão', 'Outono', 'Inverno', 'Primavera']

# --- Tabela 1: Por Estação do Ano ---
tab_estacao = (
    df_valido.groupby('Estacao')
    .agg(
        Total_Avaliados=('PCR_Positivo', 'count'),
        Positivos_n=('PCR_Positivo', 'sum')
    )
    .reindex(ordem_estacoes)
    .fillna(0)
    .astype(int)
    .reset_index()
)
tab_estacao['Negativos_n'] = tab_estacao['Total_Avaliados'] - tab_estacao['Positivos_n']
tab_estacao['Positivos (%)'] = np.where(
    tab_estacao['Total_Avaliados'] > 0,
    (tab_estacao['Positivos_n'] / tab_estacao['Total_Avaliados'] * 100).round(1),
    0.0
)

# --- Tabela 2: Por Mês (garantindo todos os 12 meses) ---
tab_mes_raw = (
    df_valido.groupby(['Mes_Num', 'Mes'])
    .agg(
        Total_Avaliados=('PCR_Positivo', 'count'),
        Positivos_n=('PCR_Positivo', 'sum')
    )
    .reset_index()
)
todos_meses = pd.DataFrame({
    'Mes_Num': range(1, 13),
    'Mes': [nomes_meses[m] for m in range(1, 13)]
})
tab_mes = todos_meses.merge(tab_mes_raw, on=['Mes_Num', 'Mes'], how='left').fillna(0)
tab_mes[['Total_Avaliados', 'Positivos_n']] = tab_mes[['Total_Avaliados', 'Positivos_n']].astype(int)
tab_mes['Negativos_n'] = tab_mes['Total_Avaliados'] - tab_mes['Positivos_n']
tab_mes['Positivos (%)'] = np.where(
    tab_mes['Total_Avaliados'] > 0,
    (tab_mes['Positivos_n'] / tab_mes['Total_Avaliados'] * 100).round(1),
    0.0
)

# Salva as duas tabelas (com ponto e vírgula para abrir certinho no Excel em português)
tab_estacao.to_csv('resumo_sazonal_estacoes.csv', index=False, sep=';', encoding='utf-8-sig')
tab_mes.to_csv('resumo_sazonal_meses.csv', index=False, sep=';', encoding='utf-8-sig')

print("\n--- RESUMO POR ESTAÇÃO DO ANO ---")
print(tab_estacao.to_string(index=False))

# ==============================================================================
# 5. GERAR O PAINEL DE GRÁFICOS (ABNT - 300 DPI)
# ==============================================================================
fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.2), dpi=300)

# Título geral no topo (com Helicobacter em itálico)
fig.suptitle(
    'Distribuição sazonal de mamíferos aquáticos avaliados e positividade para $\\mathbfit{Helicobacter}$ spp.',
    fontsize=12, fontweight='bold', y=0.98
)

# --- Painel A: Estações do Ano ---
ax1 = axes[0]
x1 = np.arange(len(tab_estacao))

ax1.bar(x1, tab_estacao['Negativos_n'], color='#a6bddb', edgecolor='#333333', linewidth=0.6, label='Negativo')
ax1.bar(x1, tab_estacao['Positivos_n'], bottom=tab_estacao['Negativos_n'], color='#d92b2b', edgecolor='#333333', linewidth=0.6, label='Positivo')

for i, row in tab_estacao.iterrows():
    if row['Total_Avaliados'] > 0:
        ax1.text(
            i, row['Total_Avaliados'] + 0.5,
            f"{row['Positivos_n']}/{row['Total_Avaliados']}\n({row['Positivos (%)']}%)",
            ha='center', va='bottom', fontsize=8.5
        )

ax1.set_title('A) Por Estação do Ano', fontsize=11, fontweight='bold', loc='left', pad=10)
ax1.set_xticks(x1)
ax1.set_xticklabels(tab_estacao['Estacao'], fontsize=10)
ax1.set_xlabel('Estação do ano', fontsize=10.5, labelpad=6)
ax1.set_ylabel('Número de indivíduos (n)', fontsize=10.5, labelpad=6)
ax1.set_ylim(0, tab_estacao['Total_Avaliados'].max() * 1.25)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.legend(frameon=False, fontsize=9.5, loc='upper right')

# --- Painel B: Distribuição Mensal ---
ax2 = axes[1]
x2 = np.arange(len(tab_mes))

ax2.bar(x2, tab_mes['Negativos_n'], color='#a6bddb', edgecolor='#333333', linewidth=0.6, label='Negativo')
ax2.bar(x2, tab_mes['Positivos_n'], bottom=tab_mes['Negativos_n'], color='#d92b2b', edgecolor='#333333', linewidth=0.6, label='Positivo')

for i, row in tab_mes.iterrows():
    if row['Positivos_n'] > 0:
        ax2.text(
            i, row['Total_Avaliados'] + 0.3,
            f"{row['Positivos_n']}",
            ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#990000'
        )

ax2.set_title('B) Por Mês', fontsize=11, fontweight='bold', loc='left', pad=10)
ax2.set_xticks(x2)
ax2.set_xticklabels(tab_mes['Mes'], fontsize=9.5)
ax2.set_xlabel('Mês da ocorrência', fontsize=10.5, labelpad=6)
ax2.set_ylabel('Número de indivíduos (n)', fontsize=10.5, labelpad=6)
ax2.set_ylim(0, tab_mes['Total_Avaliados'].max() * 1.18)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

# Ajusta o espaçamento e salva a imagem em alta resolução (300 DPI)
plt.tight_layout(rect=[0, 0, 1, 0.93])
plt.savefig('painel_sazonalidade_helicobacter_ABNT.png', dpi=300, bbox_inches='tight')
plt.show()

print("\n✅ Arquivos gerados na sua pasta:")
print("1. resumo_sazonal_estacoes.csv")
print("2. resumo_sazonal_meses.csv")
print("3. painel_sazonalidade_helicobacter_ABNT.png")
