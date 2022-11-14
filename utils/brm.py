import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utils.utils import *

# benefit representation matrix


def build_matrix(p, e):
    '''
    Parameters
    ----------
    p, e: Series 
        Vectores columna con todos los registros, así como vienen de la base de prestaciones.

    Returns
    ----------
    matrix: DataFrame
        Benefit representation matrix. 
        Cada elemento (i,j) indica la cantidad de apariciones de la prestación j en el efector i.
    '''

    check(p.size == e.size, 'Los vectores deben tener la misma longitud.')

    matrix = pd.DataFrame(columns=list(p.unique()),
                          index=list(e.unique())).fillna(0)

    for i, value in p.items():
        matrix.loc[e.iloc[i], value] += 1

    check(p.size == matrix.sum().sum())

    return matrix


def occ_to_prob(matrix):
    nrows = matrix.shape[0]

    for i in range(nrows):
        matrix.iloc[i] = matrix.iloc[i] / matrix.iloc[i].sum()

    check(nrows == matrix.sum().sum())

    return matrix

# apply thresholds


def remove_rare_benefits(matrix, tresh, percentage_tresh=True, strict=True):
    '''
    Nos va a interesar remover las prestaciones que tienen una frecuencia o porcentaje de aparicón menor a un treshold 
    (aparición sobre el total, no en un cierto efector).

    Parameters
    ----------
    matrix: DataFrame
        Benefit representation matrix (index=effectors, columns=benefits)
    tresh: float or integer
        If percentage treshold, must be a value between 0 and 100.
        If frequency treshold, must be an integer.
    percentage_tresh: bool (default=True)
        Says whether treshold is percentage or frequency.
    strict: bool (default=True)
        Says whether treshold removal is less than strict or less or equal. 

    Returns
    -------
    new_matrix, removed_benefits

    new_matrix: DataFrame
        Benefit representation matrix without removed benefits.
    removed_benefits: DataFrame
        Benefit representation matrix with removed benefits. Complement of new_matrix.           
    '''

    if not percentage_tresh and not type(tresh) == int:
        raise TypeError('Frecuency treshold must be integer.')

    if percentage_tresh and not (type(tresh) == int or type(tresh) == float):
        raise TypeError('Percentage treshold must be float or integer.')

    if percentage_tresh and not (tresh >= 0 and tresh <= 100):
        raise ValueError('Percentage treshold value must be between 0 and 100')

    total_occ = matrix.sum().sum()  # total of benefit occurences
    new_matrix = matrix
    removed_benefits = pd.DataFrame(index=matrix.index)

    for index, value in matrix.sum().items():
        if percentage_tresh:
            value = value * 100 / total_occ

        if value < tresh or (not strict and value == tresh):
            new_matrix = new_matrix.drop([index], axis=1)
            removed_benefits[index] = matrix[index]

    return new_matrix, removed_benefits


def remove_low_records_effectors(matrix, tresh, percentage_tresh=True, strict=True):

    if not percentage_tresh and not type(tresh) == int:
        raise TypeError('Frecuency treshold must be integer.')

    if percentage_tresh and not (type(tresh) == int or type(tresh) == float):
        raise TypeError('Percentage treshold must be float or integer.')

    if percentage_tresh and not (tresh >= 0 and tresh <= 100):
        raise ValueError('Percentage treshold value must be between 0 and 100')

    total_records = matrix.transpose().sum().sum()  # total of benefit occurences
    new_matrix = matrix
    removed_effectors = pd.DataFrame(columns=matrix.columns)

    for index, value in matrix.transpose().sum().items():

        if percentage_tresh:
            value = value * 100 / total_records

        if value < tresh or (not strict and value == tresh):
            new_matrix = new_matrix.drop([index], axis=0)
            removed_effectors = pd.concat(
                [removed_effectors, matrix.loc[index].to_frame().transpose()])

    return new_matrix, removed_effectors


def intersect_tables(table1, table2):
    '''
    Sirve para aplicar los dos thresholds: prestaciones raras y efectores con bajos registros.

    Parameters
    -----------

    table1: debe ser output de remove_low_records_effectors()
    table2: debe ser output de remove_rare_benefits()

    Tomo table1 como base y me quedo con las columnas de table1 que estén en table2.
    '''

    table = table1

    cols1 = list(table1.columns)
    cols2 = list(table2.columns)

    if not len(cols1) == len(cols2):
        check(len(cols2) < len(cols1))

        for col in cols1:
            if col not in cols2:
                table = table.drop(col, axis=1)

    return table

# plot


def plot_benefit_type_probability(freq_table, fig_number, freq=False, show=True, fig_size=(10, 5)):
    '''
    Graphs benefit representation matrix showing probability of each benefit type normalized by effector.

    Parameters
    ----------
    freq_table: DataFrame
        Index must be effectors (usually cathegory).
    freq: bool (default=True)
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

    for effector_type in list(freq_table.index):
        v = list(freq_table.loc[effector_type])

        if not freq:
            # normalizo por efector (barras del mismo color suman 1)
            v = [item / np.sum(v) for item in v]

        values[effector_type] = v

        ax.bar(x, values[effector_type], width, label=effector_type)
        x = x + width

    ax.set_xlabel('Tipo prestacion')

    factor = (len(list(freq_table.index)) - 1) / 2

    ax.set_xticks(y + factor*width, labels, rotation=10)

    ax.legend()

    if freq:
        ax.set_ylabel('Frecuencia')
        ax.set_title(
            f'FIG {fig_number}. Frecuencia tipo prestación según efector')
    else:
        ax.set_ylabel('Probabilidad por efector')
        ax.set_title(
            f'FIG {fig_number}. Probabilidad tipo prestación según efector')

    fig.tight_layout()

    if show:
        plt.show()

    return fig


def plot_benefit_profile(freq_table, fig_number, freq=False, show=True, fig_size=(10, 5), fig=None):
    '''
    Es esencialmente el mismo gráfico que benefit_type_probability() pero haciendo switch de labels. 
    L probabilidad sigue normalizada por efector. Aquí las barras de una misma categoría de efector suman 1, no las de mismo color.
    Sirve para visualizar mejor los perfiles de prestaciones asociadas a cada categoría.
    '''

    if not fig == None:
        plt.close(fig)

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

    if not freq:
        prob_table = freq_table.copy()

        for eff in list(prob_table.index):
            prob_table.loc[eff] = prob_table.loc[eff] / n_total[eff].item()

    for benefit_type in list(freq_table.columns):
        if not freq:
            v = list(prob_table[benefit_type])
        else:
            v = list(freq_table[benefit_type])

        values[benefit_type] = v

        ax.bar(x, values[benefit_type], width, label=benefit_type)
        x = x + width

    ax.set_xlabel('Categoria efector')

    factor = (len(list(freq_table.columns)) - 1) / 2

    ax.set_xticks(y + factor*width, labels, rotation=10)

    # ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.legend()

    ax.set_title(
        f'FIG {fig_number}. Perfil de prestaciones por categoría efector')

    if freq:
        ax.set_ylabel('Frecuencia')

    else:
        ax.set_ylabel('Probabilidad por efector')

    fig.tight_layout()

    if show:
        plt.show()

    return fig
