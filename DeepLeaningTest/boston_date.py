__author__ = "susmote"

import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.feature_selection import SelectKBest, f_regression
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

boston_dataset = datasets.load_boston()
X_full = boston_dataset.data
Y = boston_dataset.target
print(X_full.shape)
print(Y.shape)
