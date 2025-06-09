import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from projet_rattrapage.salary_prediction import OrdinaryLeastSquares

def test_fit_and_predict():
    #Données "jouets" : y = 2x + 1
    X = np.array([[1], [2], [3], [4], [5]])
    y = np.array([3, 5, 7, 9, 11])

    model = OrdinaryLeastSquares(intercept=True)
    model.fit(X, y)
    y_pred = model.predict(X)

    assert y_pred.shape == y.shape
    np.testing.assert_almost_equal(y_pred, y, decimal=5)

def test_r2_perfect_fit():
    X = np.array([[1], [2], [3]])
    y = np.array([2, 4, 6])  #y = 2x
    model = OrdinaryLeastSquares()
    model.fit(X, y)
    r2 = model.determination_coefficient(X, y)
    assert r2 == 1.0

def test_get_coeffs():
    X = np.array([[1], [2]])
    y = np.array([3, 5])
    model = OrdinaryLeastSquares(intercept=True)
    model.fit(X, y)
    coeffs = model.get_coeffs()
    assert coeffs.shape == (2,)  #β0 (intercept) et β1

def test_confidence_intervals_shape():
    X = np.random.rand(10, 3)
    y = X @ np.array([2, -1, 0.5]) + 1
    model = OrdinaryLeastSquares(intercept=True)
    model.fit(X, y)
    intervals = model.confidence_intervals(X, y)
    assert len(intervals) == X.shape[1] + 1  #3 variables + intercept = 4

def test_predict_without_fit():
    model = OrdinaryLeastSquares()
    try:
        model.predict(np.array([[1, 2, 3]]))
        assert False, "Should have failed because model is not fitted"
    except Exception:
        pass  #Ok
