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
        try:
            results = RegressionAnalysis(
                self.df, self.drug, self.sentence_type).get_results()
            coefficients = get_significant_coefficients(
                results, self.drug, self.sentence_type)
            us_counties = gpd.read_file(DATA_PATH + '/map/us_counties.json')
            nc_counties = us_counties[us_counties['STATEFP']
                                      == '37'][['NAME', 'geometry']]
            nc_counties['County'] = nc_counties['NAME'].apply(
                lambda x: x.upper())
            county_coefficients = nc_counties[['County', 'geometry']].merge(
                coefficients, how='outer', left_on='County', right_index=True)
            county_coefficients = county_coefficients[county_coefficients['County'].isin(
                nc_counties['County'])]
            if len(county_coefficients.dropna()) > 0:
                ax = county_coefficients.plot(column=self.drug + '_' + self.sentence_type,
                                              legend=True,
                                              cmap=self.get_cmap(),
                                              legend_kwds={
                                                  'orientation': 'horizontal'}
                                              )
                plt.title('{0} {1} Punishment Significantly Different from Wake County'.format(
                    self.drug, self.sentence_type))
                plt.xticks([])
                plt.yticks([])
                ax.axis('off')
                self.save_figure('punishment_harshness_by_county')
        except AttributeError:
            pass

    def get_cmap(self):
        cmap_dict = {
            'Marijuana': 'Greens',
            'Cocaine': 'Blues',
            'Heroin': 'Reds'
        }
        return cmap_dict[self.drug]
