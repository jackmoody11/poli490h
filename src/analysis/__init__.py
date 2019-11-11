import os
import matplotlib.pyplot as plt


path = os.path.abspath(os.path.dirname(__file__))
data_path = os.path.join(path, '/../data')
# DRUG_OUTPUT_FILES = {k: data_path + '/' +
#                      k for k in ['marijuana', 'cocaine', 'heroin']}
FIGURE_PATH = os.path.abspath(
    os.path.dirname(__file__)) + '/../../figures'


def save_figure(drug_name, filename):
    plt.savefig(
        FIGURE_PATH + '/{0}/{1}.png'.format(drug_name, filename), bbox_inches='tight', transparent=True)
    plt.close()
