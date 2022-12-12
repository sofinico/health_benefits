from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np

from sklearn.decomposition import PCA
from utils.brm import *

# cargamos la base de prestaciones

df_p = pd.read_pickle("data/base_prestaciones/misiones_2019_completa.pkl")

p = df_p['codigo_prestacion']
e = df_p['efector']

matrix = build_matrix(p, e)
X = matrix.to_numpy()

# ------------------------------------------------------------------

# PCA Frecuencias


print('PCA Frecuencias')

pca = PCA(n_components=3)

pc = pca.fit_transform(X)

df = pd.DataFrame(data=pc, columns=['PC1', 'PC2', 'PC3'])

df_pca_freq = pd.concat([pd.Series(matrix.index, name='efector'), df], axis=1)

print('Variance ratio:', [np.round(n * 100, 2)
      for n in pca.explained_variance_ratio_], '%')
print('Variance ratio PC1 + PC2:', np.round(
    pca.explained_variance_ratio_[:2].sum() * 100, 2), '%')

df_pca_freq.to_pickle("./data/pca/misiones_2019/frequencies.pkl")

# ------------------------------------------------------------------

# PCA Probablidad normalizada por efector (por fila de "matrix")


print('\nPCA Probablidad normalizada por efector')

matrix_prob = occ_to_prob(matrix)

X_prob = matrix_prob.to_numpy()

pca = PCA(n_components=3)

pc = pca.fit_transform(X_prob)

df = pd.DataFrame(data=pc, columns=['PC1', 'PC2', 'PC3'])

df_pca_prob = pd.concat(
    [pd.Series(matrix.index, name='efector'), df], axis=1)

print('Variance ratio:', [np.round(n * 100, 2)
      for n in pca.explained_variance_ratio_], '%')
print('Variance ratio PC1 + PC2:', np.round(
    pca.explained_variance_ratio_[:2].sum() * 100, 2), '%')

df_pca_prob.to_pickle("./data/pca/misiones_2019/probability.pkl")

# ------------------------------------------------------------------

# PCA Z Score (por columna de "matrix", ie, por prestación)


print('\nPCA Z Score')


X_z = StandardScaler().fit_transform(X_prob)

pca = PCA(n_components=3)

pc = pca.fit_transform(X_z)

df = pd.DataFrame(data=pc, columns=['PC1', 'PC2', 'PC3'])

df_pca_z = pd.concat([pd.Series(matrix.index, name='efector'), df], axis=1)

print('Variance ratio:', [np.round(n * 100, 2)
      for n in pca.explained_variance_ratio_], '%')
print('Variance ratio PC1 + PC2:', np.round(
    pca.explained_variance_ratio_[:2].sum() * 100, 2), '%')

df_pca_z.to_pickle("./data/pca/misiones_2019/z_score.pkl")
