#### dudas

- [x] interpretación de la ubicación de los puntos en el PCA en relación a los pesos de los ejes. ¿Qué pasa cuando una misma prestación aparece en dos componentes con peso de signo opuesto?
- [x] criterio de remoción "bueno", para las figuras del notebook 1 (inequidad rural-urbano) => remover no por porcentaje si no por frecuencia, con una justificación de fluctuaciones estadísticas (2% pueden ser 30k). Elaborar más esta justificación y pensar cuando sí tiene sentido remover por porcentaje (prestaciones "raras").
- [x] decisiones en mapeo lineas de cuidado => OK (con cierto thresh frecuencia). Estaría bueno comparar después con la decisión más conservadora de sacar los datos que no podemos mapear y hacer los mismos gráficos. Lo que estamos haciendo propiamente se llama _imputación_ de datos: sustitución de valores no informados en una observación por otros.
- [x] sub o sobre representacion: con threshold de frecuencias => OK (suma de ambos con un límite)

#### to-do

- [x] mapeo líneas de cuidado<sup>1</sup>
- [x] completar base prestaciones con la metadata de la base de cateogorías prestaciones (valores imputados)
- [x] presentación de resultados más útil: colocar conclusiones y corresponderlos con los objetivos para diciembre
- [ ] ~gráficos probabilidad línea de cuidado por categoría y perfil líneas de cuidado (tipo notebook 1) (1)~ <sup>2</sup>
- [x] benefit representation matrix con prestaciones full dim (2)
  - [x] postas
  - [x] centro de salud
  - [x] todos rurales vs todos urbanos
  - [x] todos rurales vs todos urbanos (sólo consultas o sólo inmunizaciones)
- [x] PCA (3)
- [ ] PCA: elipses rural-urbano
- [ ] clústering prestaciones (4)
  - [ ] jerárquico
  - [ ] distancia euclídea

<sup>1</sup> No es trivial. Ver notebook 2. La raíz del problema es que la intersección de prestaciones (código completo) entre las bases es del 30%. Se elaboró el método de imputación de máximas ocurrencias.
<sup>2</sup> Se cierra esto por el momento, ver notebook 1 v2. La distribución de ocurrencias de línea de cuidado (o cualquier otro agrupamiento) en la base no permite extraer información significativa. Ver `benefit_occ` table.

#### backlog

- [ ] pasar a db el documento 04_Ninos_1608.pdf
- [ ] referencia única para categorizar e identificar prestaciones

#### ideas

- [ ] sub o sobre representación de prestaciones por zonas geográficas
- [ ] PCA: tamaño marker según cantidad de registros del efector
- [ ] PCA: por diagnóstico en lugar de prestación
