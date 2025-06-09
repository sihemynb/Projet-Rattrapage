import numpy as np
import pandas as pd
import sys
import os
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from projet_rattrapage.salary_prediction import OrdinaryLeastSquares

df = pd.read_csv("data/PlayerStatistics.csv", low_memory=False)
salaries = pd.read_csv("data/Salaries.csv")

#Fusion des fichiers sur personId
df = df.merge(salaries, on="personId", how="inner")

#Filtrage saison
df["gameDate"] = pd.to_datetime(df["gameDate"])
df = df[(df["gameDate"] >= "2023-10-01") & (df["gameDate"] <= "2024-06-30")]

#Moyenne des stats pour chaque joueur
mean_stats = df.groupby("personId")[["points", "assists", "reboundsTotal"]].mean()
mean_salary = df.groupby("personId")["salaryInDollars"].mean()

#Nettoyage
X = mean_stats.values
y = mean_salary.values
mask = ~np.isnan(X).any(axis=1) & ~np.isnan(y)
X, y = X[mask], y[mask]

model = OrdinaryLeastSquares(intercept=True)
model.fit(X, y)

#Résultats des coefficients beta
print("Coefficients estimés :")
for i, b in enumerate(model.get_coeffs()):
    print(f"β{i} = {b:.3f}")

print("\n R² :", round(model.determination_coefficient(X, y), 4))

#Intervalles de confiance
print("\n Intervalles de confiance à 95 % :")
for i, (b, (inf, sup)) in enumerate(zip(model.get_coeffs(), model.confidence_intervals(X, y))):
    print(f"β{i} ∈ [{inf:.3f}, {sup:.3f}]")

#Visualisation des prédictions et des résidus
model.plot_predictions(X, y)
model.plot_residuals(X, y)
