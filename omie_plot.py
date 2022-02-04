#!/usr/bin/python
"""
 Author: Roldán Gutiérrez García
 Email: <roldan.gutierrez@alumnos.unican.es><roldanggarcia@gmail.com>
 Created: 03/02/2021
 Description: Reads da_price.csv file containing OMIE day ahead hourly prices for each day and plots a graph comparing
    month averages through different years.
"""
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('da_price.csv', parse_dates=["datetime_utc", "fecha"])

# media, max y minimo por mes
df.set_index("fecha", inplace=True)
df = df.groupby(pd.Grouper(freq="M"))["precio"].agg(["mean", "max", "min"])
df.reset_index(inplace=True)
df = df.loc[df["fecha"].dt.year < 2022]  # como 2022 no está completo lo quitamos

# configuración de la gráfica
fig, ax = plt.subplots(figsize=(12, 6))

ax.grid(which="major", axis="y", color="#758D99", alpha=0.6, zorder=1)

for year in df["fecha"].dt.year.unique():
    ax.plot(df[df["fecha"].dt.year == year]["fecha"].dt.month,
            df[df["fecha"].dt.year == year]["mean"],
            alpha=0.8,
            linewidth=3)
    
# adición de línea y tag
ax.plot([0.12, 0.9],
       [0.98, 0.98],
       transform=fig.transFigure,
       clip_on=False,
       color="#E3120B",
       linewidth=0.6)
ax.add_patch(plt.Rectangle((0.12, 0.98),
                          0.04,
                          -0.02,
                          facecolor="#E3120B",
                          transform=fig.transFigure,
                          clip_on=False,
                          linewidth=0))

# título, subtítulo y fuente
ax.text(x=0.12, y=0.93, s="Precios medios OMIE", transform=fig.transFigure, ha="left", fontsize=13, weight="bold", alpha=0.8)
ax.text(x=0.12, y=0.89, s="Precios medios del mercado spot por mes, comparación por año", 
        transform=fig.transFigure, ha="left", fontsize=11,  alpha=0.8)
ax.text(x=0.12, y=0.01, 
        s="""Fuente: "OMIE" via https://www.omie.es/ || https://zenodo.org/record/5900902#.YfxGpurMKCp""", 
        transform=fig.transFigure, ha="left", fontsize=9,  alpha=0.7)

# eliminación de líneas exteriores del gráfico
ax.spines["top"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["right"].set_visible(False)

# texto de los ejes y leyenda
plt.xlabel("Mes")
plt.ylabel("Precio medio OMIE (€/MWh)")
plt.legend(df["fecha"].dt.year.unique(), title="Año")

plt.show()

fig.savefig("omie_avg_price_plot.png")
