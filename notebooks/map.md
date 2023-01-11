### 5 - unificación bases

---

### 4 - pca

Exploratorio. Principal component analysis para reducir la dimensionalidad del espacio de prestaciones y lograr una visualización 2D de los efectores.

Se decidió que hacerlo con la BRM de probabilidades es lo que tiene más sentido.

#### 4_v2

Idem 4 pero sólo con probabilidad. Más conciso y prolijo y pruebo otras agrupaciones dadas por el Sumar para las prestaciones en lugar de hacer el PCA con código prestación.

#### 4_v3

Focalizamos en PCA con probabilidad normalizada por efector con código prestación. Probamos diferentes visualizaciones y fiteamos elipses para rural-urbano.

---

### 3 - sub o sobre representación de prestaciones

Cálculo de benefit representation matrix. Armado de una `ratio_table` donde se comparan las probabilidades de aparición de prestaciones para cada categoría de efector.

Se hizo el análisis de sub y sobre representación para diferentes agrupamientos de efectores y prestaciones.

---

### 2 - base categorías prestaciones

La intención de ese notebook es explorar la info de la base categorías prestaciones y proponer un mapeo a la base de prestaciones. Se busca una estandarización de ese mapeo para poder aplicarlo a otras bases de prestaciones cuando lleguen (en particular el mapeo línea de cuidado - prestación (sin diagnóstico) donde debemos imputar datos).

Se elaboró el criterio de imputación de máximas ocurrencias y se lo aplicó para TIPO - NOMBRE TIPO y TIPO + OBJ - LÍNEA DE CUIDADO. Para esta imputación se hizo un análisis al final del notebook.

Lo trabajado se implementó en `preprocessing.py` de modo que la base de prestaciones se encuentra completa.

---

### 1 - inequidad rural-urbano

1. Tabla frecuencia categorías efectores: `index = rural_urbano`, `columns = tipo_efe` - **table10**
2. Gráfico de barras de la tabla con probabilidad normalizada según rural/urbano - **fig10**

prestaciones => tipo
efectores => categoría

3. Benefit representation matrix para categoría de efectores y tipo prestación - **table20**
4. Thresholds para efectores y prestaciones (o criterio de remoción)
5. Gráfico de barras con probabilidad de prestaciones normalizada por prestación - **fig2\***
6. Gráfico de barras perfil de prestaciones (probabilidades normalizadas por efector) - **fig3\***

#### 1_v2

El 1 mejorado. Ya importa la db completa y demás. Se recomienda fuertemente ver este notebook en lugar del 1.

Esencialmente:

- Calcula la BRM
- Aplica thresholds para mejor visualización y análisis
- Plotea
