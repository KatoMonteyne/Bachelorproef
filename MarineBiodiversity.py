import pandas as pd
biodiversity = pd.read_csv("Data/Diversity_data_with_env.csv")
variables = pd.read_csv("Data/Diversity_data_with_biooracle_2010.csv")


df = pd.read_csv("Data/Diversity_data_with_biooracle_2010.csv")
print(df)
df.columns

df2 = pd.read_csv("Data/Diversity_data_with_env.csv")
df2.columns
df2["MPA"].unique()


df = df.rename(columns={
    'marine_species_richness': 'SR',
    'co1_genetic_diversity_mean': 'GD',
    'long_deg':'long',
    'lat_deg':'lat'
})


SR = df[['SR', 'long', 'lat']]
GD = df[['GD', 'long', 'lat']]
PD = df[['PD', 'long', 'lat']]

import plotly.express as px
import plotly.io as pio
pio.renderers.default = "notebook"


fig = px.scatter_geo(
    SR,
    lat="lat",
    lon="long",
    color="SR",   # kleurt de punten op basis van biodiversiteit
    hover_name="SR",  
    projection="natural earth"    # mooie wereldkaart
)
fig.show()

fig = px.scatter_geo(
    GD,
    lat="lat",
    lon="long",
    color="GD",   # kleurt de punten op basis van biodiversiteit
    hover_name="GD",  
    projection="natural earth"    # mooie wereldkaart
)
fig.show()


fig = px.scatter_geo(
    PD,
    lat="lat",
    lon="long",
    color="PD",   # kleurt de punten op basis van biodiversiteit
    hover_name="PD",  
    projection="natural earth"    # mooie wereldkaart
)
fig.show()



temp = df[['long', 'lat', 'T_mean']]
print(temp)



fig = px.scatter_geo(
    temp,
    lat="lat",
    lon="long",
    color="T_mean",
    color_continuous_scale="thermal",
    title="Gemiddelde temperatuur (T_mean)"
)

fig.update_layout(
    geo=dict(
        projection_type="natural earth",
        showland=True,
        landcolor="rgb(240,240,240)",
        showocean=True,
        oceancolor="rgb(210,230,255)"
    )
)

fig.show()



O2 = df[['long', 'lat', 'o2_mean']]

fig = px.scatter_geo(
    O2,
    lat="lat",
    lon="long",
    color="o2_mean",
    color_continuous_scale="Viridis",
    projection = "natural earth",
    title="O2-concentratie",
)

fig.update_traces(marker=dict(size=5))

fig.update_layout(
    coloraxis_colorbar=dict(
        title="O2 (mmol/m3)"
    )
)


fig.show()



salinity = df[['long', 'lat', 'salinity_mean']]


fig = px.scatter_geo(
    salinity,
    lat="lat",
    lon="long",
    color="salinity_mean",
    color_continuous_scale="Turbo",  # goede schaal voor salinity
    projection="natural earth",
    title="salinity"
)

fig.update_traces(marker=dict(size=5))

fig.update_layout(
    coloraxis_colorbar=dict(
        title="Salinity"
    )
)

fig.show()



pH = df[['long', 'lat', 'ph_mean']]

fig = px.scatter_geo(
    pH,
    lat="lat",
    lon="long",
    color="ph_mean",
    color_continuous_scale="RdBu_r",  # goed voor pH (laag ↔ hoog)
    projection="natural earth",
    title="pH"
)

fig.update_traces(marker=dict(size=5))

fig.update_layout(
    coloraxis_colorbar=dict(
        title="pH"
    )
)

fig.show()



MPA = df2[['long_deg', 'lat_deg', 'MPA']]

fig = px.scatter_geo(
    MPA,
    lat="lat_deg",
    lon="long_deg",
    color="MPA",
    color_continuous_scale="Viridis",
    projection="natural earth",
    title="MPA"
)

fig.update_traces(marker=dict(size=6))

fig.update_layout(
    coloraxis_colorbar=dict(
        title="MPA"
    )
)

fig.show()




koraal = df2[['long_deg', 'lat_deg', 'Coral']]

fig = px.scatter_geo(
    koraal,
    lat="lat_deg",
    lon="long_deg",
    color="Coral",  # nu numeriek
    color_continuous_scale="Viridis",  # mooie continue kleur
    projection="natural earth",
    title="Koraal"
)

fig.update_traces(marker=dict(size=6))

fig.update_layout(
    coloraxis_colorbar=dict(
        title="Koraal"
    )
)

fig.show()





