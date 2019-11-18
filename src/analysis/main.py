from analysis.age import AgeAnalysis
from analysis.attorney_type import AttorneyAnalysis
from analysis.county import CountyAnalysis
from analysis.gender import GenderAnalysis
from analysis.plea import PleaAnalysis
from analysis.race import RaceAnalysis
from analysis.general import GeneralAnalysis
from analysis.regression import RegressionAnalysis


def create_figures(df, drug_name, sentence_type):
    # Instantiate analyses objects and run each
    args = (df, drug_name, sentence_type)
    analyses = [AgeAnalysis(*args), AttorneyAnalysis(*args),
                CountyAnalysis(*args), GenderAnalysis(*args),
                PleaAnalysis(*args), RaceAnalysis(*args),
                GeneralAnalysis(*args), RegressionAnalysis(*args)]

    for analysis in analyses:
        analysis.run()
