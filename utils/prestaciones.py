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
    print('Effectors in benefits base but not in cathegory base:', n_no_cath, '\n')

    return match_table
