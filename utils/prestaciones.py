import pandas as pd
import numpy as np

from utils.utils import *


def total_childs(df: pd.DataFrame, col_name='id') -> int:
    return len(df[col_name].unique())


def total_effectors(df: pd.DataFrame, col_name='efector') -> int:
    return len(df[col_name].unique())


def match_effectors(eff_benefits: pd.Series, eff_cathegories: pd.Series) -> pd.DataFrame:
    '''
    Cuáles efectores de la base de prestaciones tienen categoría. 

    Params:
    ----------

    eff_benefits: Series
        columna de los efectores de la base de prestaciones así como viene
    eff_cathegories: Series
        columa de los efectores de la base de categorías así como viene 

    Returns:
    ----------

    match_table: DataFrame
        tabla con index efector y una columna 'has_cathegory' true o false
    '''

    set_eff_cath = eff_cathegories.unique()
    set_eff_b = eff_benefits.unique()

    check(len(set_eff_cath) >= len(set_eff_b))

    # elements of set_eff_b that are in set_eff_cath

    match_eff = np.isin(set_eff_b, set_eff_cath)

    check(len(match_eff) == len(set_eff_b))

    match_table = pd.DataFrame(index=set_eff_b, columns=['has_cathegory'])
    match_table['has_cathegory'] = match_eff

    n_has_cath = match_table.loc[match_table.has_cathegory == True].shape[0]
    n_no_cath = match_table.shape[0] - n_has_cath

    check(n_no_cath + n_has_cath == len(set_eff_b))

    print('\nEffectors in both bases:', n_has_cath)
    print('Effectors in benefits base but not in cathegory base:', n_no_cath)

    return match_table


def match_benefits(ben_base: pd.Series, ben_cathegories: pd.Series, print_info=True, print_name='Benefits') -> pd.DataFrame:
    '''
    Cuáles son las prestaciones de la base de prestaciones que tienen categoría. 

    Params:
    ----------

    ben_base: Series
        columna de las prestaciones de la base de prestaciones así como viene
    ben_cathegories: Series
        columa de las prestaciones de la base de categorías así como viene 

    Returns:
    ----------

    match_table: DataFrame
        tabla con index prestacion y una columna 'has_cathegory' true o false
    '''

    set_ben_cath = ben_cathegories.unique()
    set_ben_base = ben_base.unique()

    check(len(set_ben_cath) >= len(set_ben_base))

    # elements of set_ben_base that are in set_ben_cath

    match_ben = np.isin(set_ben_base, set_ben_cath)

    check(len(match_ben) == len(set_ben_base))

    match_table = pd.DataFrame(index=set_ben_base, columns=['has_cathegory'])
    match_table['has_cathegory'] = match_ben

    n_has_cath = match_table.loc[match_table.has_cathegory == True].shape[0]
    n_no_cath = match_table.shape[0] - n_has_cath

    check(n_no_cath + n_has_cath == len(set_ben_base))

    if print_info:
        print(f'\n{print_name} in both bases:', n_has_cath)
        print(
            f'{print_name} in benefits base but not in cathegory base:', n_no_cath)

    return match_table


def map_by_max_occurencies(colname_a: str, colname_b: str, df: pd.DataFrame, prob_thresh=0.60, freq_thresh=10, use_freq_thresh=True):
    '''
    Mapea 1 a 1 variable "a" con variable "b" e imputa de ser necesario según el criterio de máximas ocurrencias.
    Reflejamos cuando la probabilidad máxima de ocurrencia es menor a un threshold (columna 'low_prob' == True).
    Reflejamos cuando la cantidad total de ocurrencias es menor a un threshold (columna 'low_freq' == True).
    No se imputa si el threshold de probabilidad no se supera. Se puede elegir si el threshold de frequencia 
    debe ser también superado o no.

    Params:
    ----------

    colname_a: str
        nombre de la columna de la variable "a"
    colname_b: str
        nombre de la columna de la variable "b"
    df: DataFrame
        data frame con los datos que se quieren mapear
    prob_thresh: float
        dado un valor de "a", es el threshold de probabilidad máxima para un valor de "b"
    freq_thresh: float
        threshold para cantidad total de ocurrencias de un cierto valor de "a"
    use_freq_thres: bool
        decide si debe superarse el threshold de frecuencias para imputar o no


    Returns:
    ----------

    df_info: DataFrame

    map_a_to_b: dict
    '''

    df_info = pd.DataFrame(
        columns=[colname_a, colname_b, 'freq', 'prob', 'is_max_prob', 'low_prob', 'low_freq'])

    map_a_to_b = dict.fromkeys(list(df[colname_a].unique()))

    # iteramos sobre todos los valores de "a"
    for a in df[colname_a].unique():

        freq_a = df.loc[df[colname_a] == a].shape[0]

        low_freq = True if freq_a < freq_thresh else False

        # possible "b" values for "a"
        a_to_b_count = df.loc[df[colname_a] == a][colname_b].value_counts()

        for i in range(0, a_to_b_count.shape[0]):
            # voy agregando filas a df_info
            df_info.loc[len(df_info)] = [a,
                                         # "b" value
                                         a_to_b_count.index[i],
                                         # freq ("b" occurencies)
                                         a_to_b_count[i],
                                         # prob
                                         np.round(
                                             a_to_b_count[i]/sum(a_to_b_count[:]), 2),
                                         # is_max_prob
                                         False,
                                         # low_prob
                                         False,
                                         low_freq
                                         ]

        # máxima probabilidad de un valor de "b"
        max_prob = df_info.loc[df_info[colname_a] == a].sort_values(
            by=['prob'], ascending=False).iloc[0]['prob']

        # si no cumple el threshold, lo marcamos
        if max_prob < prob_thresh:
            df_info.loc[df_info[colname_a] == a, 'low_prob'] = True

        # uno o más valores de "b" pueden tener máxima probabilidad
        a_most_prob_rows = df_info.loc[(df_info[colname_a] == a) & (
            df_info['prob'] == max_prob)]

        for i in range(0, a_most_prob_rows.shape[0]):
            b = a_most_prob_rows.iloc[i][colname_b]
            df_info.loc[(df_info[colname_a] == a) &
                        (df_info[colname_b] == b), 'is_max_prob'] = True

        # actual imputation

        # si sólo tenemos una ocurrencia de "a" (ie un sólo valor de "b" para "a", caso trivial)
        if a_to_b_count.shape[0] == 1:
            map_a_to_b[a] = a_most_prob_rows[colname_b].item()

        # si dos o más valores de "b" son equiprobables, decido no elegir (no imputar)
        elif a_most_prob_rows.shape[0] > 1:
            map_a_to_b[a] = 'Sin datos'

        # si sólo tenemos un valor de "b" con probabilidad máxima y...

        # no supera prob_tresh, no imputo
        elif a_most_prob_rows['low_prob'].item():
            map_a_to_b[a] = 'Sin datos'

        else:
            # pido que supere el freq_thesh, tampoco imputo
            if (use_freq_thresh and a_most_prob_rows['low_freq'].item()):
                map_a_to_b[a] = 'Sin datos'

            # no pido que supere el freq_thesh, finalmente imputo
            else:
                map_a_to_b[a] = a_most_prob_rows[colname_b].item()

    return df_info, map_a_to_b


def add_no_cath_to_map(match_table: pd.DataFrame, map_dict: dict):
    '''
    Completa las keys de los mapeos para que estén todos los valores de la base de prestaciones.
    Más que nada sirve para el momento de completar la base de prestaciones con la info de categorias.

    Params:
    ----------

    match_table: DataFrame
        output de match_benefits()
    map_dict: dict
        output de map_by_max_occurencies()

    Returns:
    ----------

    Nothing but mutates map_dict.
    '''

    if match_table.loc[match_table.has_cathegory == False].shape[0] > 0:

        for code in list(match_table.loc[match_table.has_cathegory == False]['has_cathegory'].index):
            map_dict[code] = 'Sin datos'
