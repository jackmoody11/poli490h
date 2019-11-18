import matplotlib.pyplot as plt
from analysis.base import _Base


class GenderAnalysis(_Base):
    def __init__(self, df, drug_name, sentence_type):
        super().__init__(df, drug_name, sentence_type)
        self.__methods__ = []
