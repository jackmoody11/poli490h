import statsmodels.api as sm
import pandas as pd


def linear_regression(df, dep_vars, indep_vars, *dummy_vars):
    _df = pd.concat([df[dep_vars], df[indep_vars],
                     get_dummies(df, *dummy_vars)], axis=1).dropna()
    X = _df.drop(dep_vars, axis=1)
    X = sm.add_constant(X)
    y = _df[dep_vars]
    model = sm.OLS(y, X)
    results = model.fit()
    return results


def get_significant_coefficients(results, drug_name, sentence_type):
    summary = results.summary()
    results_html = summary.tables[1].as_html()
    coef_header = drug_name + '_' + sentence_type
    p_value_header = drug_name + '_' + sentence_type + '_p_value'
    series = pd.read_html(results_html, header=0, index_col=0)[0][[
        'coef', 'P>|t|']].rename({'coef': coef_header, 'P>|t|': p_value_header}, axis=1)
    series.drop_duplicates(inplace=True)
    # Only take values that were statistically significant so that
    return series[series[p_value_header] <= 0.05][coef_header]


def get_dummies(df, *dummies):
    """ Drops certain dummy variable to test hypotheses and prevent multicolinearity. """
    dfs = []
    dummy_map = {'Defendant_Race': 'White',
                 'County': 'WAKE',
                 'Plea_Code': 'Guilty',
                 'District_Court_Attorney_Type': 'Privately Retained or Self',
                 'Defendant_Sex_Code': 'Female'}
    for dummy in dummies:
        _df = pd.get_dummies(df[dummy])
        try:
            dfs.append(_df.drop(dummy_map[dummy], axis=1))
        # If dummy variable in dummy_map isn't available, at least one dummy var dropped.
        # No multicolinearity from dummy var.
        except KeyError:
            dfs.append(_df)
    return pd.concat(dfs, axis=1)
