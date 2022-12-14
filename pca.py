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

df_pca_prob['rural_urbano'] = ''
df_pca_prob['cluster_custom'] = ''
df_pca_prob['categoria_efe'] = ''

for index, row in df_pca_prob.iterrows():
    rural_urbano = df_p.loc[df_p.efector ==
                            row.efector, 'rural_urbano'].iloc[0]
    cluster_custom = 2 if (row.PC1 < -0.32) else 1
    categoria = df_p.loc[df_p.efector == row.efector, 'categoria_efe'].iloc[0]

    df_pca_prob.loc[df_pca_prob.efector ==
                    row.efector, 'rural_urbano'] = rural_urbano
    df_pca_prob.loc[df_pca_prob.efector ==
                    row.efector, 'cluster_custom'] = cluster_custom
    df_pca_prob.loc[df_pca_prob.efector ==
                    row.efector, 'categoria_efe'] = categoria

df_pca_prob

df_pca_prob.to_pickle("./data/pca/misiones_2019/probability.pkl")

# ------------------------------------------------------------------

# PCA Z Score (por columna de "matrix", ie, por prestaci??n)


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
