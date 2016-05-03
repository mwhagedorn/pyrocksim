import untangle
import os

from engine import Engine


class RSEParser(object):
    def __init__(self,filename):
        self._filename = filename

    def parse(self):
        if not os.path.exists(self._filename):
            print("no file %s" % self._filename)
            return False
        engine =  untangle.parse(self._filename)
        engine_attributes = engine.engine_database.engine_list.engine
        data_points =  [(dp["t"],dp["f"], dp["m"]) for dp in engine.engine_database.engine_list.engine.data.eng_data]
        engine = Engine(**engine_attributes._attributes)
        engine.data_points = data_points
        return engine
