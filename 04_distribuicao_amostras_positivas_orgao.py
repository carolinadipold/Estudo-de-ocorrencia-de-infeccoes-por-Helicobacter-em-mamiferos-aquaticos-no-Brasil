import matplotlib.pyplot as plt

# 1. Configuração tipográfica e estética ABNT (Times New Roman)
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

# Se estiver rodando no Google Colab e quiser garantir a fonte exata:
# !apt-get install -y fonts-liberation
# Ou instale msttcorefonts se estiver em ambiente Linux local.

# 2. Dados das amostras positivas
dados = [
    ("Estômago (não especificado)", 9),
    ("Esôfago", 7),
    ("Estômago 1 (Anterior)", 6),
    ("Estômago 2 (Principal)", 5),
    ("Rim", 3),
    ("Estômago 3 (Pilórico)", 3),
    ("Fígado", 1),
    ("Língua", 1),
    ("Linfonodo mesentérico", 1)
]

total = sum(v for _, v in dados)

# Inverte a ordem para que o maior valor apareça no topo
orgaos = [item[0] for item in dados][::-1]
valores = [item[1] for item in dados][::-1]

# 3. Criação da figura (300 DPI para impressão de alta qualidade)
fig, ax = plt.subplots(figsize=(8, 4.8), dpi=300)

# Barras horizontais com cor acadêmica sóbria (azul marinho clássico)
bars = ax.barh(orgaos, valores, color='#2b5c8f', edgecolor='#1a3857', height=0.62)

# Adiciona os rótulos de contagem e porcentagem ao final de cada barra
for bar in bars:
    w = bar.get_width()
    pct = (w / total) * 100
    ax.text(
        w + 0.2, 
        bar.get_y() + bar.get_height() / 2, 
        f'{int(w)} ({pct:.1f}%)', 
        va='center', 
        ha='left', 
        fontsize=10, 
        color='#111111'
    )

# 4. Ajustes de eixos e formatação limpa
ax.set_xlim(0, max(valores) + 2.5)
ax.set_xlabel('Número de Amostras Positivas (n)', fontsize=11, labelpad=8)
ax.tick_params(axis='both', which='major', labelsize=10)

# Grade sutil apenas no eixo horizontal para guiar o olhar
ax.xaxis.grid(True, linestyle='--', alpha=0.45, color='#cccccc')
ax.set_axisbelow(True)

# Remove as bordas superior e direita (estilo acadêmico limpo)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# 5. Exportação em alta resolução
plt.tight_layout()
plt.savefig('distribuicao_orgaos_positivos.png', dpi=300, bbox_inches='tight')
plt.show()
