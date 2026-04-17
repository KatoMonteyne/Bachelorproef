import pathlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import (
    train_test_split, cross_val_score, GroupKFold,
)

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.inspection import permutation_importance

sns.set_theme(style="whitegrid")

data = pd.read_csv("Data/Diversity_data_with_biooracle_2010.csv")


data2 = pd.read_csv("Data/Diversity_data_with_env.csv")
data2.columns
data2.head()

data_samen = data.merge(data2, on = ["long_deg", "lat_deg"])
data_samen.tail()
data_samen.columns

print(f"Diversity_data_with_env:             {data_samen.shape}")
# de data heeft 2452 rijen en 75 kolommen
# de data samen heeft 2452 rijen en 106  kolommen 


data.head()
data.columns

target = "PD_x" # Geselecteerde biodiversiteitsmaat om te voorspellen.

feature_cols = [ # Dit zijn de variabelen die we hier selecteren om de biodiversiteit te voorspellen.
    "clt_mean",        
    "currentdirection_mean",
    "currentvelocity_mean",
    "dfe_mean",
    "mlotst_mean",
    "o2_mean",
    "par_mean",
    "phyc_mean",
    "ph_mean",
    "po4_mean",
    "salinity_mean",
    "si_mean",
    "tas_mean",
    "terrain_characteristics_bea_mean",
    "terrain_characteristics_slope",
    "T_mean", 
    "LandDist",
]

df = data_samen[[target] + feature_cols].copy()
print(f"Shape before cleaning: {df.shape}")  
df.describe() # geeft een beschrijvende statistiek van de variabelen 


# Ontbrekende waarden worden als -9999 aangegeven in de dataset.
df.replace(-9999.0, np.nan, inplace=True)
df.replace(-9999, np.nan, inplace=True)

missing = df.isna().sum() # Ontbrekende waarden tellen.
print("Missing values per column:\n")
print(missing[missing > 0])

df.dropna(inplace=True) # Ontbrekende waarden verwijderen.
print(f"\nShape after dropping rows with NaN: {df.shape}")


# histogram van de gekozen biodiversiteitsmaat
fig, ax = plt.subplots(figsize=(7, 4))
ax.hist(df[target], bins=50, edgecolor="white")
ax.set_xlabel("Phylogenetic diversity")
ax.set_ylabel("Count")
ax.set_title("Distribution of PD")
plt.tight_layout()
plt.show()


# Correlatie heatmap 
corr = df.corr(numeric_only=True)
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r", center=0, ax=ax)
ax.set_title("Pearson correlatie matrix")
plt.tight_layout()
plt.show()


# willekeurig splitsen van de data in een training set en test set
X = df[feature_cols]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=2026
)

X_train.columns
print(f"Training samples: {X_train.shape[0]}")
print(f"Test samples:     {X_test.shape[0]}")


# hyperparameters aanpassen 
rf = RandomForestRegressor(
    n_estimators=800,
    max_depth=20,
    min_samples_leaf=1,
    random_state=42,
    n_jobs=-1,
)
rf.fit(X_train, y_train)

#-----------------------------------------------------------------------------

from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestRegressor

rf = RandomForestRegressor(random_state=42)

# de hyperparameters optimaliseren 
param_grid = {
    "n_estimators": [200, 500, 800],
    "max_depth": [10, 20, 30, None],
    "min_samples_leaf": [1, 5, 10],
    "max_features": ["sqrt", 0.3, 0.5]
}

grid = GridSearchCV(
    rf,
    param_grid,
    cv=5,
    scoring="r2",
    n_jobs=-1
)

grid.fit(X_train, y_train)

print(grid.best_params_)
# een proberen met n_estimators = 800, max_depth = 20 en min_samples_leaf = 1
# ----------------------------------------------------

y_pred = rf.predict(X_test)

r2_train = rf.score(X_train, y_train)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Train R² : {r2_train:.4f}")
print(f"Test  R² : {r2:.4f}")
print(f"RMSE     : {rmse:.4f}")
print(f"MAE      : {mae:.4f}")
print(f"\nTrain–test gap: {r2_train - r2:.4f}")


fig, ax = plt.subplots(figsize=(6, 6))
ax.scatter(y_test, y_pred, s=10, alpha=0.4)
lims = [min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())]
ax.plot(lims, lims, "r--", linewidth=1)
ax.set_xlabel("Observed PD")
ax.set_ylabel("Predicted PD")
ax.set_title(f"Observed vs Predicted  (R² = {r2:.3f})")
ax.set_aspect("equal")
plt.tight_layout()
plt.show()


residuals = y_test - y_pred
fig, axes = plt.subplots(1, 2, figsize=(12, 4))


axes[0].scatter(y_pred, residuals, s=10, alpha=0.4)
axes[0].axhline(0, color="red", linestyle="--")
axes[0].set_xlabel("Predicted GD")
axes[0].set_xlabel("Predicted PD")
axes[0].set_ylabel("Residual")
axes[0].set_title("Residuals vs Predicted")

axes[1].hist(residuals, bins=50, edgecolor="white")
axes[1].set_xlabel("Residual")
axes[1].set_ylabel("Count")
axes[1].set_title("Residual distribution")

plt.tight_layout()
plt.show()


imp = pd.Series(rf.feature_importances_, index=feature_cols).sort_values()


fig, ax = plt.subplots(figsize=(7, 5))
imp.plot.barh(ax=ax)
ax.set_xlabel("Mean decrease in impurity")
ax.set_title("Impurity-based feature importance")
plt.tight_layout()
plt.show()

top_features = imp.head(10).index.tolist()
print(top_features)




print(len(rf.feature_importances_))
print(len(feature_cols))



# spatial crossvalidation 
lat = data.loc[df.index, "lat_deg"]
lon = data.loc[df.index, "long_deg"]
lat_bin = pd.cut(lat, bins=np.arange(-90, 91, 10), labels=False)
lon_bin = pd.cut(lon, bins=np.arange(-180, 181, 10), labels=False)
spatial_blocks = lat_bin.astype(str) + "_" + lon_bin.astype(str)

print(f"\nSpatial blocks (10°×10° grid): {spatial_blocks.nunique()} unique blocks")

gkf = GroupKFold(n_splits=5)
spatial_cv = cross_val_score(
    rf, X, y, cv=gkf, groups=spatial_blocks, scoring="r2", n_jobs=-1,
)
print("Spatial  5-fold CV R² scores:", np.round(spatial_cv, 4))
print(f"Mean R²: {spatial_cv.mean():.4f}  ±  {spatial_cv.std():.4f}")





###################################
# model maken met minder variabelen
###################################

target = "PD_x" # Geselecteerde biodiversiteitsmaat om te voorspellen.

feature_cols = [ # Dit zijn de variabelen die we hier selecteren om de biodiversiteit te voorspellen.
    "chl_mean",      # variabelen kiezen die invloed gaan hebben op de biodiversiteit  
    "clt_mean",        
    "currentdirection_mean",
    "currentvelocity_mean",
    "dfe_mean",
    "kdpar_mean",
    "mlotst_mean",
    "no3_mean",
    "o2_mean",
    "par_mean",
    "phyc_mean",
    "ph_mean",
    "po4_mean",
    "salinity_mean",
    "siconc_mean",
    "sithick_mean",
    "si_mean",
    "tas_mean",
    "terrain_characteristics_aspect",
    "terrain_characteristics_bea_mean",
    "terrain_characteristics_rug",
    "terrain_characteristics_slope",
    "terrain_characteristics_topo",
    "T_mean", 
    "DepthMean",
    "LandDist",
    "Shelf",
    "Slope",
    "Abyssal",
    "Seamount",
]

df = data_samen[[target] + feature_cols].copy()
print(f"Shape before cleaning: {df.shape}")  
df.describe()

df.replace(-9999.0, np.nan, inplace=True)
df.replace(-9999, np.nan, inplace=True)

missing = df.isna().sum() # Ontbrekende waarden tellen.
print("Missing values per column:\n")
print(missing[missing > 0])

df.dropna(inplace=True) # Ontbrekende waarden verwijderen.
print(f"\nShape after dropping rows with NaN: {df.shape}")

X = df[feature_cols]
y = df[target]

from sklearn.feature_selection import RFECV

# Random Forest
estimator = RandomForestRegressor(
    n_estimators=800,
    max_depth=20,
    min_samples_leaf=1,
    random_state=42,
    n_jobs=-1
)

# RFECV met spatial CV + RMSE
selector = RFECV(
    estimator,
    step=1,
    cv=gkf,
    scoring="neg_root_mean_squared_error",
    n_jobs=-1
)

selector.fit(X, y, groups=spatial_blocks)

print(f"Optimal number of features: {selector.n_features_}")

selected_features_RFECV = X.columns[selector.support_]
print("Selected features:", list(selected_features_RFECV))

# er blijven nog 17 variabelen over 
# clt_mean, currentdirection_mean, currentvelocity_mean, dfe_mean,
# mlotst_mean, o2_mean, par_mean, phyc_mean, ph_mean, po4_mean, salinity_mean, si_mean, 
# tas_mean, terrain_characteristics_bea_mean, terrain_characteristics_slope, 
# T_mean, LandDi