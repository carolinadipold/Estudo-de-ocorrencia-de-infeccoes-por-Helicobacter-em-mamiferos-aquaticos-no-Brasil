'''Função gerada com auxílio do Google Gemini (modelo 4 Neon) em nov/2026
Prompt base: Não sei programar em Python, mas preciso gerar um mapa em alta resolução para um relatório científico (padrão ABNT, fonte Times New Roman) usando os dados da minha planilha (dados_geograficos_com_PCR.csv).
A minha planilha tem coordenadas geográficas nas colunas Latitude e Longitude (em formato decimal, mas pode ter vírgula no lugar de ponto) e uma coluna chamada PCR_Positivo (onde 1 é positivo e 0 é negativo).
Quero que o mapa tenha:
O contorno oficial dos estados do Brasil, com foco na faixa costeira onde estão os meus pontos (de SC até o CE).
Oceano em azul bem claro, estados sem coleta em cinza claro e os 6 estados com coleta (BA, CE, RJ, SC, SP e SE) destacados em outra cor suave, com a sigla escrita dentro de cada um.
Todos os pontos plotados: negativos em azul e positivos em vermelho (ficando por cima dos azuis para dar destaque), mostrando a quantidade (n) de cada grupo na legenda.
Grade de coordenadas, nomes dos eixos (Latitude e Longitude), seta indicando o Norte, legenda limpa e o título: "Distribuição espacial de mamíferos aquáticos avaliados e positividade para Helicobacter spp."
Por favor, gere o código completo pronto para copiar e colar, me diga exatamente o que preciso instalar no computador para rodar e salve o mapa como uma imagem PNG pronta para colar no Word.
'''
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from shapely.geometry import Point

# ==============================================================================
# 1. CONFIGURAÇÃO TIPOGRÁFICA ABNT (Times New Roman)
# ==============================================================================
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'DejaVu Serif']
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

# ==============================================================================
# 2. CARREGAR E LIMPAR OS DADOS
# ==============================================================================
arquivo = 'dados_geograficos_com_PCR.csv’     # ou .xlsx 
col_pcr = 'PCR_Positivo'     # ou .xlsx 

try:
    df = pd.read_csv(arquivo, sep=None, engine='python', encoding='utf-8-sig')
except UnicodeDecodeError:
    df = pd.read_csv(arquivo, sep=None, engine='python', encoding='latin1')

df.columns = df.columns.str.strip()

if df[col_pcr].dtype == 'object':
    df['Status_PCR'] = df[col_pcr].astype(str).str.strip().str.lower().isin(['positivo', 'sim', '1', 'pos']).astype(int)
else:
    df['Status_PCR'] = df[col_pcr].fillna(0).astype(int)

for coord in ['Latitude', 'Longitude']:
    df[coord] = df[coord].astype(str).str.replace(',', '.', regex=False).str.strip()
    df[coord] = pd.to_numeric(df[coord], errors='coerce')

df_mapa = df.dropna(subset=['Latitude', 'Longitude']).copy()

geometria = [Point(xy) for xy in zip(df_mapa['Longitude'], df_mapa['Latitude'])]
gdf_pontos = gpd.GeoDataFrame(df_mapa, geometry=geometria, crs='EPSG:4674')

# ==============================================================================
# 3. BAIXAR MALHA DOS ESTADOS + SIGLAS OFICIAIS DO IBGE
# ==============================================================================
url_estados = "https://servicodados.ibge.gov.br/api/v3/malhas/paises/BR?formato=application/vnd.geo+json&qualidade=intermediaria&intrarregiao=UF"
url_nomes_uf = "https://servicodados.ibge.gov.br/api/v1/localidades/estados"

estados = gpd.read_file(url_estados).to_crs('EPSG:4674')
nomes_uf = pd.read_json(url_nomes_uf)[['id', 'sigla']]
nomes_uf['id'] = nomes_uf['id'].astype(str)
estados['codarea'] = estados['codarea'].astype(str)

estados = estados.merge(nomes_uf, left_on='codarea', right_on='id')

# Define os 6 estados amostrados
ufs_amostradas = ['BA', 'CE', 'RJ', 'SC', 'SP', 'SE']
estados_destaque = estados[estados['sigla'].isin(ufs_amostradas)]
estados_outros = estados[~estados['sigla'].isin(ufs_amostradas)]

# ==============================================================================
# 4. PLOTAR O MAPA COSTEIRO EM ALTA RESOLUÇÃO
# ==============================================================================
fig, ax = plt.subplots(figsize=(8, 9), dpi=300)

ax.set_facecolor('#e6f2f8')  # Oceano

# Estados não amostrados (cinza bem claro)
estados_outros.plot(ax=ax, color='#f4f4f4', edgecolor='#bbbbbb', linewidth=0.6, zorder=1)

# Estados amostrados (tom areia/cinza médio para destacar a área de estudo)
estados_destaque.plot(ax=ax, color='#e2e8d8', edgecolor='#666666', linewidth=0.8, zorder=2)

# Adiciona as siglas (BA, CE, RJ, SC, SP, SE) dentro de cada estado amostrado
for _, row in estados_destaque.iterrows():
    ponto_label = row['geometry'].representative_point()
    ax.text(
        ponto_label.x, ponto_label.y, row['sigla'],
        fontsize=9, fontweight='bold', color='#333333',
        ha='center', va='center', zorder=3
    )

# Separa Negativos e Positivos
gdf_neg = gdf_pontos[gdf_pontos['Status_PCR'] == 0]
gdf_pos = gdf_pontos[gdf_pontos['Status_PCR'] == 1]

gdf_neg.plot(
    ax=ax, color='#4a7ebb', edgecolor='#1f4e79',
    markersize=35, alpha=0.75, label=f'Negativo (n = {len(gdf_neg)})', zorder=4
)

gdf_pos.plot(
    ax=ax, color='#d92b2b', edgecolor='#660000',
    markersize=50, alpha=0.95, label=f'Positivo (n = {len(gdf_pos)})', zorder=5
)

# Zoom automático englobando do CE até SC (+ margem de 2.0 graus)
minx, miny, maxx, maxy = gdf_pontos.total_bounds
margem = 2.0
ax.set_xlim(minx - margem, maxx + margem)
ax.set_ylim(miny - margem, maxy + margem)

# Título do mapa
ax.set_title(
    'Distribuição espacial de mamíferos aquáticos avaliados e positividade para Helicobacter spp.',
    fontsize=11.5, fontweight='bold', pad=12
)

ax.set_xlabel('Longitude (°)', fontsize=11, labelpad=8)
ax.set_ylabel('Latitude (°)', fontsize=11, labelpad=8)
ax.tick_params(axis='both', which='major', labelsize=10)
ax.grid(True, linestyle='--', alpha=0.5, color='#999999', zorder=0)

# Seta do Norte
ax.annotate(
    'N', xy=(0.94, 0.96), xytext=(0.94, 0.89),
    arrowprops=dict(facecolor='#222222', width=3, headwidth=10),
    ha='center', va='center', fontsize=12, fontweight='bold',
    xycoords=ax.transAxes
)

# Legenda combinada (PCR + Estados amostrados)
handles, labels = ax.get_legend_handles_labels()
handles.append(Patch(facecolor='#e2e8d8', edgecolor='#666666', label='Estados amostrados'))

ax.legend(
    handles=handles, loc='lower right', frameon=True,
    facecolor='white', edgecolor='#cccccc',
    fontsize=9.5, title='Legenda (nPCR)', title_fontsize=10
)

plt.tight_layout()
plt.savefig('mapa_distribuicao_helicobacter_brasil_ABNT.png', dpi=300, bbox_inches='tight')
plt.show()
print("✅ Mapa salvo como 'mapa_distribuicao_helicobacter_brasil_ABNT.png'!")
