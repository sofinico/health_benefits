import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

df_p = pd.read_pickle("data/base_prestaciones/misiones_2019_completa.pkl")

matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Arial']


def effectors_category_bar_v2(freq_table, fig_size=(6.4, 4.8), fontsize=10):
    '''
    Parameters
    ----------
    freq_table: DataFrame
        Index must be 'Rural', 'Urbano' or 'Sin datos' and columns, types of effectors.
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

    table = freq_table.drop('Sin datos', axis=1)
    labels = list(table.columns)

    values_rural_freq = list(table.loc['Rural'])
    values_urbano_freq = list(table.loc['Urbano'])

    values_rural = [item / np.sum(values_rural_freq)
                    for item in values_rural_freq]
    values_urbano = [item / np.sum(values_urbano_freq)
                     for item in values_urbano_freq]

    x = np.arange(len(labels))  # the label locations
    # width = 0.35  # the width of the bars
    width = 0.25

    rects1 = ax.bar(x - width/2, values_rural, width,
                    label='Rural', color='deepskyblue')
    rects2 = ax.bar(x + width/2, values_urbano, width,
                    label='Urbano', color='tomato')

    ax.set_xlabel('Tipo efector', size=fontsize)
    ax.set_xticks(x, labels)
    ax.set_ylim(0, max(values_rural + values_urbano) * 1.12)
    ax.legend(fontsize=fontsize-2)

    ax.set_ylabel('Probabilidad', size=fontsize)
    ax.bar_label(rects1, padding=3, fmt='%.2f')
    ax.bar_label(rects2, padding=3, fmt='%.2f')

    ax.tick_params(labelsize=fontsize-2)
    fig.tight_layout()

    print(f'values_rural_freq: {values_rural_freq}')
    print(f'values_rural: {values_rural}')

    print(f'values_urbano_freq: {values_urbano_freq}')
    print(f'values_urbano: {values_urbano}')

    plt.show()

    return fig

# construimos la tabla de frecuencia categorías efectores


table = pd.DataFrame(
    columns=df_p['tipo_efe'].unique(), index=df_p['rural_urbano'].unique())

for cat1 in df_p['rural_urbano'].unique():
    for cat2 in df_p['tipo_efe'].unique():
        df_filtrado = df_p[(df_p.rural_urbano == cat1)
                           & (df_p.tipo_efe == cat2)]
        table.loc[cat1, cat2] = len(df_filtrado['efector'].unique())

table_renamed = table.rename(
    columns={'Posta sanitaria "B"': 'Posta', 'Centro de salud "A"': 'Centro de salud'})

# FIGURA 10

b = 14
h = 14 * (2/3)
cm = 1/2.54
fontsize = 11

fig = effectors_category_bar_v2(
    table_renamed, fig_size=(b*cm, h*cm), fontsize=fontsize)

# fig.savefig('images/effectors/effectors_cath_bar.png')
# fig.savefig(
#     f'images/effectors/effectors_cath_bar_({b}, {np.round(h, 2)}).png', dpi=1200)

plt.close()
