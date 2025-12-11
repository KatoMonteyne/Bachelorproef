import pandas as pd
biodiversity = pd.read_csv("Data/Diversity_data_with_env.csv")
variables = pd.read_csv("Data/Diversity_data_with_biooracle_2010.csv")


df = pd.read_csv("Data/Diversity_data_with_biooracle_2010.csv")
print(df)

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
pio.renderers.default = "browser"


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

