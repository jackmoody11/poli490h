import geopandas as gpd
import matplotlib.pyplot as plt
import os

path = os.path.abspath(os.path.dirname(__file__))

# Read in files
us_counties = gpd.read_file(path + '/../data/us_counties.json')
nc_zip_codes = gpd.read_file(path + '/../data/nc_zip_codes.json')

nc_zip_codes.drop(['STATEFP10', 'FUNCSTAT10'], inplace=True, axis=1)

us_counties['STATEFP'] = us_counties['STATEFP'].apply(
    lambda x: int(x))

print(nc_zip_codes.head())
# us_counties[us_counties['STATEFP'] == 37].plot()
# nc_zip_codes.plot()
us_counties.plot()
plt.show()
