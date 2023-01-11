## Objetivos generales

I. Caracterizar los efectores de salud (hospitales, centros médicos, etc.) de la provincia de Misiones según el perfil de servicios prestados a individuos menores de 5 años.

II. Caracterizar las prestaciones efectuadas a la población infantil vulnerable de la provincia de Misiones (menores de 5 años) y su asociación con variables sociodemográficas y con la desnutrición.

## Objetivos específicos

_Etapa 1: Prestaciones a niñes general_

a. Estudiar diferencias de perfiles de prestaciones para diferentes efectores de la salud de Misiones (hospitales, centros médicos, etc.).

b. Cuantificar la inequidad en acceso a la salud en zonas urbanas contra zonas rurales.

c. Disminuir la dimensionalidad del espacio de prestaciones, en la matriz efectores-prestaciones.

d. Estudiar la relación entre las características sociodemográficas de los efectores y el perfil de prestaciones que ofrecen.

_Etapa 2: Prestaciones a niñes con desnutrición_

e. Estudiar diferencias de perfiles de prestaciones para diferentes efectores de la salud de Misiones para el subset de niñes con desnutrición.

f. Determinar la proporción de individuos con desnutrición con cobertura de prestaciones asociadas a desnutrición (acatamiento al protocolo o inconstancia de carga al sistema por parte de los efectores).

## Dudas

- [ ] Probabilidades de BRM si removemos según un cierto thresh de freq: ¿se cuentan las removidas para el N total?

## To-do

**Base**

- [ ] Buscar efectores sin datos en internet (completar la base `categorias_efectores`)
- [ ] Pasar a db el documento 04_Ninos_1608.pdf
- [ ] Referencia única para categorizar e identificar prestaciones

**Otras**

- [ ] Documento con lista de análisis ya realizados, para referencia y visualización

**a.**

- [ ] Gráficos barras: cambian en algo con la "nueva" base?
- [ ] PCA con nombre de prestación en lugar de código
- [ ] Laburar la matriz del PCA (remover ciertas prestaciones, etc)

**b.**

- [ ] Sortear por N en la `ratio_table`
- [ ] CEB para la `ratio_table`
- [ ] `ratio_table` con nombre de prestación en lugar de código

**c.**

- [ ] Clústering jerárquico
- [ ] Clústering distancia euclídea

## Backlog

## Ideas

- [ ] Sub o sobre representación de prestaciones por zonas geográficas
- [ ] PCA: tamaño marker según cantidad de registros del efector
