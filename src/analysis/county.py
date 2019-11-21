from analysis.base import _Base
import geopandas as gpd
import pandas as pd


class CountyAnalysis(_Base):

    # us_counties = gpd.read_file('../../data/map/us_counties.json')
    # nc_counties = us_counties[us_counties['STATEFP']
    #                           == '37'][['NAME', 'geometry']]
    # nc_counties['NAME'] = nc_counties['NAME'].apply(lambda x: x.upper())
    # county_regressions = pd.read_csv('../../data/county_regressions.csv')

    def __init__(self, df, drug_name, sentence_type):
        super().__init__(df, drug_name, sentence_type)
        self.__metods__ = []

    def map_cases_by_county():
        coefficient_header = self.drug_name + '_' + self.st
