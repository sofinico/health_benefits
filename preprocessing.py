import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import load
from utils.utils import *
from utils.prestaciones import *

display_info = True

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

print('\n')
print('*' * 50)
print('\nCompletamos la base de prestaciones')

print('\nCantidad de registros:', entries(df_p))
print('Cantidad de efectores:', total_effectors(df_p))
print('Cantidad de niñxs:', total_childs(df_p))
print('Cantidad de prestaciones:', len(df_p['codigo_prestacion'].unique()))

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

print("\nAgregamos columnas: 'tipo_pres', 'objeto_pres', 'tipo_y_objeto_pres' y 'diagnostico_pres'")
print('\nCantidad de prestaciones considerando tipo + objeto:',
      len(df_p['tipo_y_objeto_pres'].unique()))

# ------------------------------------------------------------------

print('\n')
print('*' * 50)
print('\nBase categorías efectores...')

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

print("\nAgregamos columnas: 'rural_urbano' y 'tipo_efe', si no tienen categoría ponemos 'Sin datos'")

# ------------------------------------------------------------------

print('\n')
print('*' * 50)
print('\nBase categorías prestaciones...')

print("\nLe agregamos las columnas: 'tipo_pres', 'objeto_pres', 'tipo_y_objeto_pres' y 'diagnostico_pres'")

df_c['tipo_pres'] = None
df_c['objeto_pres'] = None
df_c['diagnostico_pres'] = None
df_c['tipo_y_objeto_pres'] = None

for index, prestacion in df_c['codigo'].iteritems():
    df_c.loc[index, 'tipo_pres'] = prestacion[:2]
    df_c.loc[index, 'objeto_pres'] = prestacion[2:6]
    df_c.loc[index, 'tipo_y_objeto_pres'] = prestacion[:6]
    df_c.loc[index, 'diagnostico_pres'] = prestacion[6:]

# primero estandarizamos los strings de la base de categorías (un poco a mano, sí)

for index, data in df_c.loc[:].iterrows():

    for col in list(df_c.columns):
        if type(data[col]) == str:
            df_c.loc[index, col] = data[col].strip()

            if col in ['seccion', 'categoria_atencion', 'subcategoria', 'linea_de_cuidado', 'tipo', 'nombre', 'diagnostico']:
                df_c.loc[index, col] = data[col].lower().capitalize().strip()

                if 'Prevención primaria' in df_c.loc[index, col]:
                    df_c.loc[index, col] = 'Prevención primaria'

# -------------------------

# mapeo tipo prestación - nombre tipo

# qué tipos están en la base de prestaciones y no en la de categorías

table_match_type = match_benefits(
    df_p['tipo_pres'], df_c['tipo_pres'], True, 'Type')

# construimos el mapeo

_, map_type_names = map_by_max_occurencies(
    'tipo_pres', 'tipo', df_c, 0.60, 10, True)

print('\nImputamos TIPO - NOMBRE TIPO según el criterio de maximas ocurrencias')
print('\nHubieron', list(map_type_names.values()).count('Sin datos'),
      'tipos que no cumplieron los criterios de imputación')

add_no_cath_to_map(table_match_type, map_type_names)

# -------------------------

# mapeo prestación - línea de cuidado

# qué prestaciones están en la base de prestaciones y no en la de categorías

table_match_benefits_full = match_benefits(
    df_p['codigo_prestacion'], df_c['codigo'], True)

# qué prestaciones (tipo + obj) están en la base de prestaciones y no en la de categorías

table_match_benefits = match_benefits(
    df_p['tipo_y_objeto_pres'], df_c['tipo_y_objeto_pres'], True, 'tipo_y_objeto')

# construimos el mapeo

# uso un df_c filtrado, pues no quiero mapear prestaciones que no están en la base de prestaciones

df_c_filt = df_c[df_c['tipo_y_objeto_pres'].isin(
    list(df_p['tipo_y_objeto_pres'].unique()))]

_, map_lc_names = map_by_max_occurencies(
    'tipo_y_objeto_pres', 'linea_de_cuidado', df_c_filt, 0.60, 10, False)

print('\nImputamos TIPO + OBJ - LÍNEA DE CUIDADO según el criterio de maximas ocurrencias')
print('\nHubieron', list(map_lc_names.values()).count('Sin datos'),
      'prestaciones que no cumplieron los criterios de imputación')

add_no_cath_to_map(table_match_benefits, map_lc_names)

# inicializo las columas

df_p['seccion_pres'] = 'Sin datos'
df_p['categoria_atencion_pres'] = 'Sin datos'
df_p['subcategoira_pres'] = 'Sin datos'
df_p['linea_de_cuidado'] = 'Sin datos'
df_p['tipo_pres_nombre'] = 'Sin datos'
df_p['objeto_pres_nombre'] = 'Sin datos'
df_p['diagnostico_pres_nombre'] = 'Sin datos'
df_p['is_in_cathegory_base'] = False
df_p['tipo_pres_nombre_imput'] = 'Sin datos'
df_p['linea_de_cuidado_imput'] = 'Sin datos'

for index, row in df_p.loc[:].iterrows():
    code = row['codigo_prestacion']

    has_cat = table_match_benefits_full.loc[table_match_benefits_full.index ==
                                            code]['has_cathegory'].item()

    df_p.loc[index, 'is_in_cathegory_base'] = has_cat

    if has_cat:
        df_p.loc[index, 'seccion_pres'] = df_c.loc[df_c.codigo ==
                                                   code]['seccion'].item()
        df_p.loc[index, 'categoria_atencion_pres'] = df_c.loc[df_c.codigo ==
                                                              code]['categoria_atencion'].item()
        df_p.loc[index, 'subcategoira_pres'] = df_c.loc[df_c.codigo ==
                                                        code]['subcategoria'].item()
        df_p.loc[index, 'linea_de_cuidado'] = df_c.loc[df_c.codigo ==
                                                       code]['linea_de_cuidado'].item()
        df_p.loc[index, 'tipo_pres_nombre'] = df_c.loc[df_c.codigo ==
                                                       code]['tipo'].item()
        df_p.loc[index, 'objeto_pres_nombre'] = df_c.loc[df_c.codigo ==
                                                         code]['nombre'].item()
        df_p.loc[index, 'diagnostico_pres_nombre'] = df_c.loc[df_c.codigo ==
                                                              code]['diagnostico'].item()

    df_p.loc[index, 'tipo_pres_nombre_imput'] = map_type_names[row['tipo_pres']]
    df_p.loc[index, 'linea_de_cuidado_imput'] = map_lc_names[row['tipo_y_objeto_pres']]

print("\nAgregamos las columnas sección, categoría atención, subcategoría, línea de cuidado, nombre tipo, " +
      "nombre objeto y diagnóstico que vienen de la base de categorías")
print("Luego una columna 'is_in_cathegory_base' y finalmente nombre tipo imputado, línea de cuidado imputada.")

# para más info de la imputación ver notebook 2

# ------------------------------------------------------------------

print('\n')
print('*' * 50)
print('\nLayout final de la base de prestaciones\n')
db_p.df.info()

# ------------------------------------------------------------------

# guardamos todo

print('\nGuardamos las bases en ./data/')

df_p.to_pickle("./data/base_prestaciones/misiones_2019_completa.pkl")
df_e.to_pickle("./data/categorias_efectores/2021.pkl")
df_e.to_pickle("./data/categorias_prestaciones/2022.pkl")
