import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import os

path = os.path.abspath(os.path.dirname(__file__))

# Read in files
nc_zip_codes = gpd.read_file('./data/map/nc_zip_codes.json')
nc_zip_codes['ZCTA5CE10'] = nc_zip_codes['ZCTA5CE10'].astype(int)


def map_all(drug, zip_codes):
    map_cases_by_zip_code(drug, zip_codes)


def map_cases_by_zip_code(drug, zip_codes):
    plt.figure()
    drug['Defendant_Address_Zip_Code'] = drug['Defendant_Address_Zip_Code'].dropna(
    ).astype(int)
    drug_zip_code_counts = pd.DataFrame(
        drug['Defendant_Address_Zip_Code'].value_counts())
    ax = nc_zip_codes.merge(drug_zip_code_counts, left_on='ZCTA5CE10', right_index=True).plot(
        column='Defendant_Address_Zip_Code', legend=True,  cmap='OrRd')
    ax.set_title('Number of Marijuana Cases by Zip Code')
    ax.set_axis_off()
