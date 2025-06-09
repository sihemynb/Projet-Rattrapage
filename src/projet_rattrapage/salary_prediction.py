import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t

class OrdinaryLeastSquares:
    def __init__(self, intercept=True):
        self.intercept = intercept
        self.coeffs = None
        
    #La fonction fit prend des données X et y en entrée et calcule l’estimateur des moindres carrés 
    def fit(self, X, y):
        if self.intercept:
            X = self._add_intercept(X)
        XtX = X.T @ X
        try:
            XtX_inv = np.linalg.inv(XtX)
        except np.linalg.LinAlgError:
            raise ValueError("La matrice XᵗX n'est pas inversible.")
        Xty = X.T @ y
        self.coeffs = XtX_inv @ Xty
        
    #La fonction predict prend des données de test Xt et renvoie les prédictions associées
    def predict(self, X):
        if self.intercept:
            X = self._add_intercept(X)
        return X @ self.coeffs
        
    #La fonction get_coeffs retourne les valeurs des coefficients estimés
    def get_coeffs(self):
        return self.coeffs
        
    #La fonction determination_coefficient calcule et renvoie le coefficient de détermination R2
    def determination_coefficient(self, X, y):
        y_pred = self.predict(X)
        ss_total = np.sum((y - np.mean(y))**2)
        ss_res = np.sum((y - y_pred)**2)
        return 1 - ss_res / ss_total

    #Visualisation des prédictions, comparaison des observations et des prédictions
    def plot_predictions(self, X, y):
        y_pred = self.predict(X)
        plt.figure(figsize=(6, 6))
        plt.scatter(y, y_pred, alpha=0.7)
        plt.plot([y.min(), y.max()], [y.min(), y.max()], "r--", label="y = ŷ")
        plt.xlabel("Salaire observé")
        plt.ylabel("Salaire prédit")
        plt.title("Salaires prédits vs. observés")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        
    #Visualisation des résidus pour vérifier les hypothèses
    def plot_residuals(self, X, y):
        y_pred = self.predict(X)
        residuals = y - y_pred
        plt.figure(figsize=(6, 4))
        plt.scatter(y_pred, residuals, alpha=0.7)
        plt.axhline(0, color="r", linestyle="--")
        plt.xlabel("Salaire prédit")
        plt.ylabel("Résidu")
        plt.title("Analyse des résidus")
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        
    #Intervalle de conviance de 95%
    def confidence_intervals(self, X, y, alpha=0.05):
        if self.intercept:
            X = self._add_intercept(X)
        n, d = X.shape
        y_pred = X @ self.coeffs
        residuals = y - y_pred
        mse = np.sum(residuals**2) / (n - d)
        XtX_inv = np.linalg.inv(X.T @ X)
        se = np.sqrt(np.diag(mse * XtX_inv))
        t_crit = t.ppf(1 - alpha / 2, df=n - d)
        intervals = []
        for b, s in zip(self.coeffs, se):
            intervals.append((b - t_crit * s, b + t_crit * s))
        return intervals

    def _add_intercept(self, X):
        n = X.shape[0]
        ones = np.ones((n, 1))
        return np.hstack((ones, X))