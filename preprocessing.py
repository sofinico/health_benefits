import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import load
from utils.utils import *
from utils.prestaciones import *

display_info = False

# ------------------------------------------------------------------

# cargo base prestaciones

db_p = load.DataBase('prestaciones_misiones_2019.csv')

if display_info:
    db_p.df.info()

df_p = db_p.df

# cargo base categorías efectores

db_e = load.DataBase('efectores2021_09_03.csv')

if display_info:
    db_e.df.info()

df_e = db_e.df

# cargo base categorías prestaciones

db_c = load.DataBase(
    'Prestaciones SUMAR -  1 diagnostico x fila 15-09-2022.csv')

if display_info:
    db_c.df.info()

df_c = db_c.df

# ------------------------------------------------------------------

print('\nCompletamos la base de prestaciones:')

print('\nCantidad de registros:', entries(df_p))
print('Cantidad de efectores:', total_effectors(df_p))
print('Cantidad de niñxs:', total_childs(df_p), '\n')

# dividimos las prestaciones tipo, objeto y diagnóstico

df_p['tipo_pres'] = None
df_p['objeto_pres'] = None
df_p['diagnostico_pres'] = None
df_p['tipo_y_objeto_pres'] = None

for index, prestacion in df_p['codigo_prestacion'].iteritems():
    df_p.loc[index, 'tipo_pres'] = prestacion[:2]
    df_p.loc[index, 'objeto_pres'] = prestacion[2:6]
    df_p.loc[index, 'tipo_y_objeto_pres'] = prestacion[:6]
    df_p.loc[index, 'diagnostico_pres'] = prestacion[6:]

print("Agregamos columnas: 'tipo_pres', 'objeto_pres', 'tipo_y_objeto_pres' y 'diagnostico_pres'\n")

# ------------------------------------------------------------------

# qué efectores de la base de prestaciones tienen categoría

table_match_effectors = match_effectors(df_p['efector'], df_e['cuie'])

# completamos base prestaciones con data de la base de categorias efectores

df_p['rural_urbano'] = None
df_p['tipo_efe'] = None

# relleno con los valores de las categorías para los efectores que tienen categoría
# si no, ponemos "Sin datos"

for e in df_p['efector'].unique():
    if e in df_e['cuie'].unique():
        df_p.loc[df_p.efector == e,
                 'rural_urbano'] = df_e.loc[df_e.cuie == e]['rural'].item()
        df_p.loc[df_p.efector == e,
                 'tipo_efe'] = df_e.loc[df_e.cuie == e]['tipo_efe'].item()

    else:
        df_p.loc[df_p.efector == e, 'rural_urbano'] = 'Sin datos'
        df_p.loc[df_p.efector == e, 'tipo_efe'] = 'Sin datos'

check(len(df_p.loc[df_p.rural_urbano == 'Sin datos']
      ['efector'].unique()) == table_match_effectors.loc[table_match_effectors.has_cathegory == False].shape[0])

print("Agregamos columnas: 'rural_urbano' y 'tipo_efe', si no tienen categoría ponemos 'Sin datos'")

# ------------------------------------------------------------------

print('\nLayout final de la base de prestaciones\n')
db_p.df.info()

# ------------------------------------------------------------------

# guardamos todo

print('Guardamos las bases en ./data/')

df_p.to_pickle("./data/base_prestaciones/misiones_2019_completa.pkl")
df_e.to_pickle("./data/categorias_efectores/2021.pkl")
df_e.to_pickle("./data/categorias_prestaciones/2022.pkl")
