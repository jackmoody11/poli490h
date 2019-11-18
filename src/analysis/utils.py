import statsmodels.api as sm
import pandas as pd


def linear_regression(df, dep_vars, indep_vars, *dummy_vars):
    _df = pd.concat([df[dep_vars], df[indep_vars], *[pd.get_dummies(df[dummy_var])
                                                     for dummy_var in dummy_vars]], axis=1).dropna()
    X = _df.drop(dep_vars, axis=1)

    # Avoid numpy .ptp deprecation warning : https://stackoverflow.com/questions/56310898/futurewarning-method-ptp
    X = sm.add_constant(X.to_numpy())
    y = _df[dep_vars]
    model = sm.OLS(y, X)
    results = model.fit()
    return results
