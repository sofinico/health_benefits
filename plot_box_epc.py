import pandas as pd
import numpy as np
from utils.brm import build_matrix, occ_to_prob
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Arial']

df_p = pd.read_pickle("data/base_prestaciones/misiones_2019_completa.pkl")
df_pca_prob = pd.read_pickle("./data/pca/misiones_2019/probability.pkl")

p = df_p['codigo_prestacion']
e = df_p['efector']

matrix = build_matrix(p, e)
matrix_prob = occ_to_prob(matrix)

epc = 'CTC001A97'
df_pca_prob['prob_epc'] = ''

for index, row in df_pca_prob.iterrows():
    prob_epc = matrix_prob.loc[matrix_prob.index == row.efector, epc].item()

    df_pca_prob.loc[df_pca_prob.efector == row.efector, 'prob_epc'] = prob_epc

# data 1, para boxplot rural/urbano

epc_rural = df_pca_prob.loc[(df_pca_prob.rural_urbano == 'Rural') & (
    df_pca_prob.cluster_custom == 1), 'prob_epc'].to_numpy()
epc_urbano = df_pca_prob.loc[(df_pca_prob.rural_urbano == 'Urbano') & (
    df_pca_prob.cluster_custom == 1), 'prob_epc'].to_numpy()

data = [epc_rural, epc_urbano]

# data 2, para boxplot categoría efe

data2 = []
caths = ['Posta Rural', 'Centro de salud Rural',
         'Posta Urbano', 'Centro de salud Urbano', 'Hospital']
caths_label = ['Posta Rural', 'Centro Rural',
               'Posta Urbano', 'Centro Urbano', 'Hospital']

for cath in caths:
    data2.append(df_pca_prob.loc[(df_pca_prob.categoria_efe == cath) & (
        df_pca_prob.cluster_custom == 1), 'prob_epc'].to_numpy())

# fig config
b = 16
h = 8
cm = 1/2.54
fontsize = 11

fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(b*cm, h*cm))

axs[0].boxplot(data)
axs[0].set_xticks([y + 1 for y in range(len(data))],
                  labels=['Rural', 'Urbano'], fontsize=fontsize-2)
axs[0].set_xlabel('Efector', fontsize=fontsize-1)
axs[0].set_ylabel('Probabilidad prestación EPC', fontsize=fontsize-1)
axs[0].yaxis.grid(True)

axs[1].boxplot(data2)
axs[1].set_xticks([y + 1 for y in range(len(data2))],
                  labels=caths_label, rotation=22, fontsize=fontsize-2)
axs[1].set_xlabel('Categoría de efector', fontsize=fontsize-1)
axs[1].yaxis.grid(True)

plt.show()

fig.savefig(
    f'images/pca/box_plot_epc_({b}, {np.round(h, 2)}).png', dpi=1200, bbox_inches="tight")
