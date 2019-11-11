import pandas as pd
import matplotlib.pyplot as plt
import os

FIGURE_PATH = os.path.abspath(
    os.path.dirname(__file__)) + '/../figures'


def map_all(drug, drug_name, zip_codes, counties):
    map_cases_by_zip_code(drug, drug_name, zip_codes)
    map_cases_by_zip_code(drug, drug_name, counties)


def map_cases_by_zip_code(drug, drug_name, zip_codes):
    plt.figure()
    drug['Defendant_Address_Zip_Code'] = drug['Defendant_Address_Zip_Code'].dropna(
    ).astype(int)
    drug_zip_code_counts = pd.DataFrame(
        drug['Defendant_Address_Zip_Code'].value_counts())
    ax = zip_codes.merge(drug_zip_code_counts, left_on='ZCTA5CE10', right_index=True).plot(
        column='Defendant_Address_Zip_Code', legend=True,  cmap='OrRd')
    ax.set_title('Number of {0} Cases by Zip Code'.format(drug_name))
    ax.set_axis_off()
    drug['Defendant_Address_Zip_Code'] = drug['Defendant_Address_Zip_Code'].dropna(
    ).astype(int)
    plt.savefig(
        FIGURE_PATH + '/{0}/cases_by_zip_code.png'.format(drug_name), bbox_inches='tight')


def map_cases_by_county(drug, drug_name, counties):
    plt.figure()
    drug['Defendant_Address_Zip_Code'] = drug['Defendant_Address_Zip_Code'].dropna(
    ).astype(int)
    drug_county_counts = pd.DataFrame(
        drug['Defendant_Address_Zip_Code'].value_counts())
    ax = counties.merge(drug_county_counts, left_on='ZCTA5CE10', right_index=True).plot(
        column='Defendant_Address_Zip_Code', legend=True,  cmap='OrRd')
    ax.set_title('Number of Marijuana Cases by Zip Code')
    ax.set_axis_off()
    plt.savefig(
        FIGURE_PATH + '/{0}/cases_by_county.png'.format(drug_name), bbox_inches='tight')
