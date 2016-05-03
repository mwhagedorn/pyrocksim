from rse_parser import RSEParser
from eng_parser import ENGParser


class EngineParser(object):

    def __init__(self, filename):
        self._filename = filename
        self._strategy = self._determine_strategy()

    def strategy(self):
        return self._strategy

    def parse(self):
        return self.strategy().parse()

    def _determine_strategy(self):
        '''
        :return: the class which implements the parser algo

        '''
        if self._filename.lower().endswith('.rse'):
            return RSEParser(self._filename)
        elif self._filename.lower().endswith('.eng'):
            return ENGParser(self._filename)