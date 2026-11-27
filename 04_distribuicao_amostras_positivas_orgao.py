# Dados ilustrativos – substituir pelas contagens reais
'''Função gerada com auxílio do Google Gemini (modelo 4 Neon) em nov/2026
Prompt base: Preciso gerar com o Python um gráfico de barras horizontais em alta resolução para um relatório científico (padrão ABNT, fonte Times New Roman) mostrando a distribuição das amostras positivas para Helicobacter spp. de acordo com o órgão ou tecido de origem.
Não precisa ler nenhuma planilha, os dados vão diretamente no código:
Estômago (não especificado): 5
Esôfago: 2
Estômago 1 (Anterior): 3
Estômago 2 (Principal): 8
Rim: 5
Estômago 3 (Pilórico): 1
Fígado: 3
Língua: 3
Linfonodo mesentérico: 2
O código precisa gerar um gráfico com:
Barras horizontais ordenadas do maior valor (no topo) para o menor (embaixo), em um tom de azul marinho sóbrio com contorno mais escuro
Rótulos de dados: ao final de cada barra, mostrar a quantidade e a porcentagem calculada sobre o total, no formato n (%)
Layout limpo: sem título interno (porque vou colocar a legenda/título no word conforme a ABNT), sem as linhas de borda de cima e da direita, com uma grade tracejada bem suave atrás das barras apenas no eixo horizontal e o nome "Número de Amostras Positivas (n)" no eixo X
Por favor, gere o código completo pronto para copiar e colar, me diga o que preciso instalar para rodar e salve o gráfico como uma imagem PNG em alta qualidade pronta para colar no Word.'''


import matplotlib.pyplot as plt

# ==============================================================================
# 1. CONFIGURAÇÃO TIPOGRÁFICA E ESTÉTICA ABNT (Times New Roman)
# ==============================================================================
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

# ==============================================================================
# 2. DADOS DAS AMOSTRAS POSITIVAS
# ==============================================================================
# Dados ilustrativos — substituir pelas contagens reais da pesquisa
dados = [
    ("Estômago (não especificado)", 5),
    ("Esôfago", 2),
    ("Estômago 1 (Anterior)", 3),
    ("Estômago 2 (Principal)", 8),
    ("Rim", 5),
    ("Estômago 3 (Pilórico)", 1),
    ("Fígado", 3),
    ("Língua", 3),
    ("Linfonodo mesentérico", 2)
]

total = sum(v for _, v in dados)

# Ordena do menor para o maior (no barh, o último item fica no topo do gráfico)
dados_ordenados = sorted(dados, key=lambda item: item[1])
orgaos = [item[0] for item in dados_ordenados]
valores = [item[1] for item in dados_ordenados]

# ==============================================================================
# 3. CRIAÇÃO DA FIGURA (300 DPI)
# ==============================================================================
fig, ax = plt.subplots(figsize=(8, 4.8), dpi=300)

bars = ax.barh(orgaos, valores, color='#2b5c8f', edgecolor='#1a3857', height=0.62)

# Adiciona rótulos de contagem e porcentagem ao final de cada barra
deslocamento = max(valores) * 0.02
for bar in bars:
    w = bar.get_width()
    pct = (w / total) * 100
    ax.text(
        w + deslocamento,
        bar.get_y() + bar.get_height() / 2,
        f'{int(w)} ({pct:.1f}%)',
        va='center',
        ha='left',
        fontsize=10,
        color='#111111'
    )

# ==============================================================================
# 4. AJUSTES DE EIXOS E FORMATAÇÃO LIMPA (ABNT)
# ==============================================================================
ax.set_xlim(0, max(valores) * 1.25)
ax.set_xlabel('Número de Amostras Positivas (n)', fontsize=11, labelpad=8)
ax.tick_params(axis='both', which='major', labelsize=10)

ax.xaxis.grid(True, linestyle='--', alpha=0.45, color='#cccccc')
ax.set_axisbelow(True)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# ==============================================================================
# 5. EXPORTAÇÃO EM ALTA RESOLUÇÃO
# ==============================================================================
plt.tight_layout()
plt.savefig('distribuicao_orgaos_positivos.png', dpi=300, bbox_inches='tight')
plt.show()
