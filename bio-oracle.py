import pandas as pd
df1 = pd.read_csv("Data/Diversity_data_with_biooracle_2010.csv")
df1.columns
df1.head()
df_locations = df1[["long_deg", "lat_deg"]]

df2 = pd.read_csv("Data/Diversity_data_with_env.csv")


import xarray as xr
import glob

files = glob.glob("nctest/*.nc")  # alles nc bestanden in 1 map steken en hier dan naar verwijzen 

datasets = [xr.open_dataset(f) for f in files]
ds = xr.merge(datasets)

print(ds)

df = ds.to_dataframe().reset_index()
len(df)
df.head()
df.columns
df = df.rename(columns={"longitude": "long_deg", "latitude": "lat_deg"})
print(df[["lat_deg", "long_deg"]].dtypes)
df["lat_deg"] = df["lat_deg"].astype("float64").round(5)
df["long_deg"] = df["long_deg"].astype("float64").round(5)
print(df[["lat_deg", "long_deg"]].head())



import pandas as pd
import numpy as np

# Stel:
# df = Bio-ORACLE DataFrame met kolommen 'lat' en 'long' + variabelen
# df_locations = jouw locaties met kolommen 'lat' en 'long'

# functie om dichtstbijzijnde waarde te vinden
def nearest(array, values):
    """
    array: 1D array van rasterwaarden (lat of long)
    values: array van gewenste waarden
    return: voor elke waarde in values de dichtstbijzijnde in array
    """
    array = np.array(array)
    values = np.array(values)
    idx = np.abs(array[:, None] - values).argmin(axis=0)
    return array[idx]

# vind dichtstbijzijnde lat/lon
df_locations["lat_match"] = nearest(df["lat_deg"].unique(), df_locations["lat_deg"])
df_locations["long_match"] = nearest(df["long_deg"].unique(), df_locations["long_deg"])

# merge op de “nearest” kolommen
df_subset = df.merge(
    df_locations,
    left_on=["lat_deg", "long_deg"],
    right_on=["lat_match", "long_match"],
    how="inner"
)

# optioneel: drop match kolommen
df_subset = df_subset.drop(columns=["lat_match","long_match"])

print(df_subset.head())  # long_deg_y en lat_deg_y komen normaal exact overeen 
len(df_subset)
df_subset = df_subset.rename(columns={"long_deg_y": "long_deg", "lat_deg_y": "lat_deg"})


(df1['lat_deg'] == df_subset['lat_deg']).all()  # True als alle rijen exact overeenkomen
(df1['long_deg'] == df_subset['long_deg']).all()
# dit moet 2 keer True teruggeven 

# je df_subset is dan de dataset waarmee je verder kan om in het model te steken 