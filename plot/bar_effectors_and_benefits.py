import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from utils.brm import *

matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Arial']

df_p = pd.read_pickle("data/base_prestaciones/misiones_2019_completa.pkl")
n_registros_p = df_p.shape[0]

color_cath = dict({'Posta Rural': 'mediumturquoise',
                   'Posta Urbano': 'lightcoral',
                   'Centro de salud Rural': 'dodgerblue',
                   'Centro de salud Urbano': 'crimson',
                   'Hospital': 'gold',
                   'Administración': 'gray'})

color_ben_type = dict({'Consulta': 'mediumseagreen',
                       'Práctica': 'gold',
                       'Imagenología': 'darkorange',
                       'Inmunizaciones': 'darkorchid',
                       'Taller': 'darkgreen',
                       'Laboratorio': 'violet'})

custom_sort_eff = dict({'Posta Rural': 0,
                        'Posta Urbano': 2,
                        'Centro de salud Rural': 1,
                        'Centro de salud Urbano': 3,
                        'Hospital': 4,
                        'Administración': 5})


def plot_benefit_type_probability_v2(freq_table, fig_size=(10, 5), fontsize=10):
    '''
    Graphs benefit representation matrix showing probability of each benefit type normalized by effector.

    Parameters
    ----------
    freq_table: DataFrame
        Index must be effectors (usually cathegory).
    freq: bool (default=False)
        Says whether the plot has frequency or probabilities in y-axis. 
        Probabilities are normalized by index (bars of same color sums one).
    show: bool (default=True)
        Says whether figure is shown or not.

    Returns
    -------
    fig: instance of figure
    '''

    fig, ax = plt.subplots()

    fig.set_size_inches(fig_size)

    # benefit types
    labels = list(freq_table.columns)

    # values of each effector cathegory
    values = dict.fromkeys(list(freq_table.index))

    x = np.arange(len(labels))
    y = x
    width = 0.1  # the width of the bars

    for effector_cath in list(freq_table.index):
        v = list(freq_table.loc[effector_cath])

        # normalizo por efector (barras del mismo color suman 1)
        v = [item / np.sum(v) for item in v]

        values[effector_cath] = v

        ax.bar(x, values[effector_cath], width,
               label=effector_cath, color=color_cath[effector_cath])
        x = x + width

    factor = (len(list(freq_table.index)) - 1) / 2

    ax.set_xticks(y + factor*width, labels, rotation=0)

    ax.set_xlabel('Tipo prestacion', size=fontsize)
    ax.set_ylabel('Probabilidad por efector', size=fontsize)

    # ax.legend(fontsize=fontsize-2, loc='center left', bbox_to_anchor=(1, 0.5))
    ax.legend(fontsize=fontsize-2)
    ax.tick_params(labelsize=fontsize-2)

    fig.tight_layout()

    plt.show()

    return fig


def plot_benefit_profile_v2(freq_table, fig_size=(10, 5), fontsize=10):
    '''
    La diferencia de este gráfico con respecto a benefit_type_probability() es que acá la probabilidad
    de un tipo de prestación es por efector (las barras de cada categoría de efector suman 1).
    '''

    fig, ax = plt.subplots()

    fig.set_size_inches(fig_size)

    # effector categories

    labels = list(freq_table.index)

    # values of each benefit type

    values = dict.fromkeys(list(freq_table.columns))

    # total of records per effector cathegory

    n_total = freq_table.transpose().sum().to_frame().transpose()

    x = np.arange(len(labels))
    y = x
    width = 0.1  # the width of the bars

    # probability (normalized per effector cathegory: bars in each "group" sum 1)

    prob_table = freq_table.copy()

    for eff in list(prob_table.index):
        prob_table.loc[eff] = prob_table.loc[eff] / n_total[eff].item()

    for benefit_type in list(freq_table.columns):

        v = list(prob_table[benefit_type])

        values[benefit_type] = v

        ax.bar(x, values[benefit_type], width,
               label=benefit_type, color=color_ben_type[benefit_type])
        x = x + width

    factor = (len(list(freq_table.columns)) - 1) / 2

    ax.set_xticks(y + factor*width, labels, rotation=10)
    ax.set_xlabel('Categoria efector', size=fontsize)
    ax.set_ylabel('Probabilidad por efector', size=fontsize)

    # ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.legend(fontsize=fontsize-2)
    ax.tick_params(labelsize=fontsize-2)

    fig.tight_layout()

    plt.show()

    return fig


# plot config
thresh_rare_benefits = 1000
thresh_low_records = 1000
percentage_thresh = False

# build brm
p = df_p['tipo_pres_nombre_imput']
e = df_p['categoria_efe']
bnr_tipo_nombre = build_matrix(p, e)

# apply thresholds
bnr_no_rare, rare_benefits = remove_rare_benefits(
    bnr_tipo_nombre, thresh_rare_benefits, percentage_thresh)

bnr_no_low, removed_effectors = remove_low_records_effectors(
    bnr_tipo_nombre, thresh_low_records, percentage_thresh)

bnr_int = intersect_tables(bnr_no_low, bnr_no_rare)

# removemos los "Sin datos" porque no son relevantes
bnr_int = bnr_int.drop(['Sin datos'], axis=0)

# ordenamos las categorías de efector para mejor visualización en el gráfico
bnr_int = bnr_int.sort_index(axis=0, key=lambda x: x.map(custom_sort_eff))

# ordenamos tipos de prestación por cantidad de registros (de mayor a menor)
custom_sort_ben_type = dict.fromkeys(list(bnr_int.columns))

for t in list(bnr_int.columns):
    custom_sort_ben_type[t] = bnr_int.sum()[t]

bnr_int = bnr_int.sort_index(axis=1, key=lambda x: x.map(
    custom_sort_ben_type), ascending=False)

# fig config
b = 16
h = 11
cm = 1/2.54
fontsize = 11

# FIGURA 20

# fig2 = plot_benefit_type_probability_v2(
#     bnr_int, fig_size=(b*cm, h*cm), fontsize=fontsize)

# fig2.savefig(
#     f'images/effectors/benefit_type_probability_trare_{thresh_rare_benefits}_tlowrec_{thresh_low_records}_({b}, {np.round(h, 2)}).png', dpi=1200)


# FIGURA 30

fig3 = plot_benefit_profile_v2(
    bnr_int, fig_size=(b*cm, h*cm), fontsize=fontsize)

# fig3.savefig(
#     f'images/effectors/effectors_cath_bar_trare_{thresh_rare_benefits}_tlowrec_{thresh_low_records}_({b}, {np.round(h, 2)}).png', dpi=1200)
