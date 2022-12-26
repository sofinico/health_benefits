import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_p = pd.read_pickle("data/base_prestaciones/misiones_2019_completa.pkl")

# algunas definiciones

color_cath = dict({'Posta Rural': 'tab:green',
                   'Posta Urbano': 'tab:green',
                   'Centro de salud Rural': 'tab:orange',
                   'Centro de salud Urbano': 'tab:orange',
                   'Hospital': 'tab:red',
                   'Administración': 'tab:cyan',
                   'Sin datos': 'tab:pink'})

color_ru = dict(
    {'Rural': 'tab:green', 'Urbano': 'tab:red', 'Sin datos': 'tab:pink'})

marker_ru = dict({'Rural': 'x', 'Urbano': '.', 'Sin datos': 'v'})


def plot_pca(ax, df, df_pca, pcx, pcy, xlim=[], ylim=[], legend=True, title=''):
    ax.set_xlabel(pcx, fontsize=14)
    ax.set_ylabel(pcy, fontsize=14)

    efectores = list(df_pca['efector'])

    for efector in efectores:
        indexes = df_pca['efector'] == efector

        cath = df.loc[df_p.efector == efector, 'categoria_efe'].iloc[0]
        ru = df.loc[df_p.efector == efector, 'rural_urbano'].iloc[0]

        ax.scatter(df_pca.loc[indexes, pcx],
                   df_pca.loc[indexes, pcy],
                   marker=marker_ru[ru],
                   c=color_cath[cath],
                   label=cath,
                   )

    if legend == True:
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys())

    if len(xlim) > 0:
        ax.set_xlim(xlim)

    if len(ylim) > 0:
        ax.set_ylim(ylim)

    if len(title) > 0:
        ax.set_title(title)

    ax.grid()


df_pca_freq = pd.read_pickle("./data/pca/misiones_2019/frequencies.pkl")
df_pca_prob = pd.read_pickle("./data/pca/misiones_2019/probability.pkl")
df_pca_z = pd.read_pickle("./data/pca/misiones_2019/z_score.pkl")

# Plots

# FREQ

# fig = plt.figure(figsize=(7.5, 5))
# fig.suptitle('PCA Frequencies', fontsize=18)
# ax1 = fig.add_subplot(1, 1, 1)
# plot_pca(ax1, df_p, df_pca_freq, 'PC1', 'PC2')
# plt.show()
# plt.savefig('images/pca/freq_pc1_pc2.png')
# plt.close()

# fig = plt.figure(figsize=(7.5, 5))
# fig.suptitle('PCA Frequencies', fontsize=18)
# ax1 = fig.add_subplot(1, 1, 1)
# plot_pca(ax1, df_p, df_pca_freq, 'PC1', 'PC3')
# plt.show()
# plt.savefig('images/pca/freq_pc1_pc3.png')
# plt.close()

# PROB

# fig = plt.figure(figsize=(7.5, 5))
# fig.suptitle('PCA Probability normalized by effector', fontsize=18)
# ax1 = fig.add_subplot(1, 1, 1)
# plot_pca(ax1, df_p, df_pca_prob, 'PC1', 'PC2')
# plt.show()
# plt.savefig('images/pca/prob_pc1_pc2.png')
# plt.close()

# fig = plt.figure(figsize=(13, 5))
# fig.suptitle('PCA Probability - 3rd component', fontsize=18)
# ax1 = fig.add_subplot(1, 2, 1)
# ax2 = fig.add_subplot(1, 2, 2)
# plot_pca(ax1, df_p, df_pca_prob, 'PC2', 'PC3')
# plot_pca(ax2, df_p, df_pca_prob, 'PC1', 'PC3')
# plt.show()
# plt.savefig('images/pca/prob_pc3.png')
# plt.close()

# ZSCORE

# fig = plt.figure(figsize=(7.5, 5))
# fig.suptitle('PCA Z Score', fontsize=18)
# ax1 = fig.add_subplot(1, 1, 1)
# plot_pca(ax1, df_p, df_pca_z, 'PC1', 'PC2')
# plt.show()
# plt.savefig('images/pca/zscore_pc1_pc2.png')
# plt.close()

# fig = plt.figure(figsize=(7.5, 5))
# fig.suptitle('PCA Z Score', fontsize=18)
# ax1 = fig.add_subplot(1, 1, 1)
# plot_pca(ax1, df_p, df_pca_z, 'PC2', 'PC3')
# plt.show()
# plt.savefig('images/pca/zscore_pc1_pc3.png')
# plt.close()
