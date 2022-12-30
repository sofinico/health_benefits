from pandas.plotting import table
import pandas as pd
import matplotlib.pyplot as plt
import dataframe_image as dfi

pd.options.display.max_colwidth = 120
pd.options.display.float_format = "{:,.2f}".format

rt_postas = pd.read_pickle(
    "./data/ratio_table/postas.pkl")

rt_centros = pd.read_pickle(
    "./data/ratio_table/centros.pkl")

N_thresh = 50
ratio_thresh = 1.5

rt_postas_display = rt_postas[(rt_postas['N'] > N_thresh) & (
    (rt_postas['R/U'] >= ratio_thresh) | (rt_postas['U/R'] >= ratio_thresh))].copy()

rt_centros_display = rt_centros[(rt_centros['N'] > N_thresh) & (
    (rt_centros['R/U'] >= ratio_thresh) | (rt_centros['U/R'] >= ratio_thresh))].copy()

for table in [rt_postas_display, rt_centros_display]:
    for index, row in table.iterrows():
        for colname in ['R/U', 'U/R']:
            if row[colname] < 1:
                table.loc[index, colname] = '-'

print('N thresh:', N_thresh)
print('Ratio thresh:', ratio_thresh)

print(rt_postas_display.to_latex(index=False))
print(rt_centros_display.to_latex(index=False))

# print(rt_postas_display)
# print(rt_centros_display)

# dfi.export(rt_centros_display,
#            f'images/ratio_table/centros_tN_{N_thresh}_tratio_{ratio_thresh}.png')

# dfi.export(rt_postas_display,
#            f'images/ratio_table/postas_tN_{N_thresh}_tratio_{ratio_thresh}.png')
