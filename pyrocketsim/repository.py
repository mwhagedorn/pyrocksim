
import os
import yaml

from couchbase.bucket import Bucket
from couchbase.views.iterator import RowProcessor

import prettytable
from rocket import Rocket

import uuid



CONFIG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'config'))
from pyrocketsim.engines.engine_parser import EngineParser

class RocketRowProcessor(RowProcessor):
    def __init__(self):
        super(RocketRowProcessor, self).__init__(rowclass=Rocket)

ENGINE_DATA = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data','engines'))

class Repository(object):

    def __init__(self):
        path = os.path.join(CONFIG_DIR, "couchbase.yml")
        with open(path, 'r') as ymlfile:
            self.cfg = yaml.load(ymlfile)

        self.hostname = self.cfg['development']['hostname']
        self.bucket = self.cfg['development']['bucket']
        self.cb = Bucket('couchbase://%s/%s' % (self.hostname,self.bucket))

        self.engines = {}
        self.setup_engines()






    def __str__(self):
        return 'Couchbase %s: %s' % (self.hostname, self.bucket)

    def setup_engines(self):
      self.engines["A8"] = EngineParser(os.path.join(ENGINE_DATA, "Estes_A8.rse")).parse()
      self.engines["A6"] = EngineParser(os.path.join(ENGINE_DATA, "Quest_A6.rse")).parse()
      self.engines["A10"] = EngineParser(os.path.join(ENGINE_DATA, "Estes_A10.rse")).parse()
      self.engines["C6"] = EngineParser(os.path.join(ENGINE_DATA, "Estes_C6.rse")).parse()
      self.engines["B6"] = EngineParser(os.path.join(ENGINE_DATA, "Estes_B6.rse")).parse()
      self.engines["B4"] = EngineParser(os.path.join(ENGINE_DATA, "Estes_B6.rse")).parse()
      self.engines["D12"] = EngineParser(os.path.join(ENGINE_DATA, "Estes_D12.rse")).parse()
      #self.engines["J275"] = EngineParser(os.path.join(ENGINE_DATA, "AeroTech_J275.rse")).parse()


    def find_rocket_by_name(self, rocketname):
        data = self.cb.query("rocket","all",key=rocketname,row_processor=RocketRowProcessor(),include_docs=True)
        return [rocket for rocket in data][0]

    def all_rockets(self):
        data = self.cb.query("rocket","all",row_processor=RocketRowProcessor(),include_docs=True)
        rockets = [rocket for rocket in data ]
        uniqueTable = prettytable.PrettyTable(["ID","Name"])
        for item in rockets:
            uniqueTable.add_row([item.id, item.name])
        return uniqueTable

    def all_engines(self):
        uniqueTable = prettytable.PrettyTable(["Code","MFG"])
        for key, value in self.engines.items():
            uniqueTable.add_row([key, value.mfg])
        return uniqueTable



    def find_engine_by_code(self,code):
        return self.engines[code]

    def create_rocket(self, name, empty_weight_g, diameter_mm, drag_coefficient):
        key = uuid.uuid4()
        self.cb.insert()
