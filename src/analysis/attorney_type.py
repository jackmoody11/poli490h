import matplotlib.pyplot as plt
from analysis import save_figure


def attorney_type_analysis(df, drug_name):
    plot_min_sentence_by_attorney_type(df, drug_name)


def plot_min_sentence_by_attorney_type(df, drug_name):
    ax = df[['District_Court_Attorney_Type', 'Minimum_Sentence_Length_in_Days']].boxplot(
        grid=False, by='District_Court_Attorney_Type', showfliers=False)
    ax.set_title(
        'Minimum Sentence Outcomes by Attorney Type: {0}'.format(drug_name))
    plt.xticks(rotation=90)
    ax.get_figure().suptitle('')
    ax.set_xlabel('Attorney Type (District Court)')
    ax.set_ylabel('Minimum Sentence Length (Days)')
    save_figure(drug_name, 'min_sentence_by_attorney_type')
