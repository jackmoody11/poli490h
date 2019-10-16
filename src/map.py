import geopandas as gpd
import matplotlib.pyplot as plt

us_counties = gpd.read_file('../data/us_counties.json')
us_counties['STATEFP'] = us_counties['STATEFP'].apply(
    lambda x: int(x))

us_counties[us_counties['STATEFP'] == 37].plot()
# us_counties.plot()
plt.show()
