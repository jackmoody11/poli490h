import matplotlib.pyplot as plt
from analysis.base import _Base
from analysis.regression import RegressionAnalysis
from analysis.utils import get_significant_coefficients
import geopandas as gpd
import pandas as pd
import numpy as np
import os

DATA_PATH = os.path.abspath(os.path.dirname(__file__)) + '/../../data'


class CountyAnalysis(_Base):

    def __init__(self, df, drug_name, sentence_type):
        super().__init__(df, drug_name, sentence_type)
        self.__methods__ = [self.map_cases_by_county]

    def map_cases_by_county(self):
        results = RegressionAnalysis(
            self.df, self.drug, self.st).get_results()
        coefficients = get_significant_coefficients(
            results, self.drug, self.st)
        us_counties = gpd.read_file(DATA_PATH + '/map/us_counties.json')
        nc_counties = us_counties[us_counties['STATEFP']
                                  == '37'][['NAME', 'geometry']]
        nc_counties['County'] = nc_counties['NAME'].apply(lambda x: x.upper())
        county_coefficients = nc_counties[['County', 'geometry']].merge(
            coefficients, left_on='County', right_index=True)
        county_coefficients = county_coefficients.replace(
            to_replace=[None], value=np.nan)
        if len(county_coefficients.dropna()) > 0:
            ax = county_coefficients.plot(column=self.drug + '_' + self.st,
                                          legend=True,
                                          cmap=self.get_cmap(),
                                          legend_kwds={
                                              'orientation': 'horizontal'}
                                          )
            plt.title('{0} {1} Punishment Significanlty Different from Wake County'.format(
                self.drug, self.st))
            self.save_figure('punishment_harshness_by_county')

    def get_cmap(self):
        cmap_dict = {
            'Marijuana': 'Greens',
            'Cocaine': 'Blues',
            'Heroin': 'Reds'
        }
        return cmap_dict[self.drug]
