import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Arial']

df_p = pd.read_pickle("data/base_prestaciones/misiones_2019_completa.pkl")

df_pca_prob = pd.read_pickle("./data/pca/misiones_2019/probability.pkl")

# algunas definiciones

color_cath = dict({'Posta Rural': 'blueviolet',
                   'Posta Urbano': 'blueviolet',
                   'Centro de salud Rural': 'darkorange',
                   'Centro de salud Urbano': 'darkorange',
                   'Hospital': 'limegreen',
                   'Administración': 'deeppink'})

color_ru = dict(
    {'Rural': 'deepskyblue', 'Urbano': 'tomato', 'Sin datos': 'gray'})

marker_ru = dict({'Rural': 'x', 'Urbano': '.', 'Sin datos': 'v'})


def plot_pca_v2(df, df_pca, pcx_name, pcy_name, fontsize=10, fig_size=(6.4, 4.8), xlim=[], ylim=[]):
    fig, ax = plt.subplots()

    fig.set_size_inches(fig_size)

    efectores = list(df_pca['efector'])

    for efector in efectores:
        indexes = df_pca['efector'] == efector

        cath = df.loc[df_p.efector == efector, 'categoria_efe'].iloc[0]
        ru = df.loc[df_p.efector == efector, 'rural_urbano'].iloc[0]

        ax.scatter(df_pca.loc[indexes, pcx_name],
                   df_pca.loc[indexes, pcy_name],
                   marker=marker_ru[ru],
                   c=color_cath[cath],
                   label=cath,
                   )

    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), fontsize=fontsize-2)

    ax.set_xlabel(pcx_name, fontsize=fontsize)
    ax.set_ylabel(pcy_name, fontsize=fontsize)

    ax.tick_params(labelsize=fontsize-2)

    if len(xlim) > 0:
        ax.set_xlim(xlim)

    if len(ylim) > 0:
        ax.set_ylim(ylim)

    # plt.axvline(x=-0.30, color='tab:gray', alpha=0.3, ls=":")

    # ax.grid()

    plt.show()

    return fig


# removemos los "Sin datos" porque no son relevantes
df_pca_prob = df_pca_prob.loc[df_pca_prob['categoria_efe'] != 'Sin datos']

# fig config
b = 16
h = 11
cm = 1/2.54
fontsize = 11

fig = plot_pca_v2(df_p, df_pca_prob, 'PC1', 'PC2',
                  fontsize=fontsize, fig_size=(b*cm, h*cm))

# fig.savefig(
#     f'images/pca/pca_effectors_({b}, {np.round(h)}).png', dpi=1200)

# fig.savefig(
#     f'images/pca/pca_effectors_with_thresh_line({b}, {np.round(h)}).png', dpi=1200)

plt.close()
