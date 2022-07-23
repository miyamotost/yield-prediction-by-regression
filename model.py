import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from utils import *


"""
    Set dataset
"""
df, df_future = set_dataset()
print(df)
print(df_future)


"""
    Predict
"""
print('Predict...')
results = smf.ols("y ~ 1 + x9 + I(x9**2) + x16 + I(x16**2) + x12", data=df).fit()
print(results.summary())
print(results.params)


"""
    Analyze and display graph
"""
# (1) label
print('label...')
pred = results.predict(df) # class: pandas.core.series.Series
pred = pred.tolist() # class: list

# (2) summary
print('summary...')
for f in ['x16', 'x9', 'x12']:
    plt.scatter(df[f], df['y'], label='label', s=5)
    plt.scatter(df[f], pred, label='predict', s=5)
    plt.grid()
    plt.legend()
    plt.savefig("./output/summary_{}.png".format(f), format="png", dpi=300)
    plt.clf()

# (2) future prediction
print('future prediction...')
for y in [2020, 2040, 2060, 2080, 2100, 2120]:
    tmp_df = df_future[(df_future['x12'] == y)]
    tmp_pred = results.predict(tmp_df) 
    tmp_pred = tmp_pred.tolist()

    for f in ['x16', 'x9']:
        plt.scatter(df[f], df['y'], label='label', s=5)
        plt.scatter(df[f], pred, label='predict', s=5)
        plt.scatter(tmp_df[f], tmp_pred, label='predict_future', s=5)
        plt.grid()
        plt.legend()
        plt.savefig("./output/future_{}_{}.png".format(y, f), format="png", dpi=300)
        plt.clf()

# (3) past prediction
print('past prediction...')
for y in range(12):
    year_start = 1960 + y*5
    year_end = 1960 + (y+1)*5
    length = 5
    tmp_df = df[(df['x12'] >= year_start) & (df['x12'] <= year_end)]
    tmp_pred = results.predict(tmp_df)
    tmp_pred = tmp_pred.tolist()

    for f in ['x16', 'x9']:
        plt.scatter(tmp_df[f], tmp_df['y'], label='label', s=5)
        plt.scatter(tmp_df[f], tmp_pred, label='predict', s=5)
        plt.grid()
        plt.legend()
        plt.savefig("./output/past_{}_{}_{}_{}.png".format(length, year_start, year_end, f), format="png", dpi=300)
        plt.clf()