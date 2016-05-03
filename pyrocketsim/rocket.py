import prettytable
import math

class Rocket(object):
    def __init__(self,key,value,docid,doc):
        self._id = str(docid)
        self.document = doc.value if doc and doc.success else None
        self.engine = None

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self.document.get("name",None) if self.document else None

    @property
    def diameter(self):
        return float(self.document.get("max_body_tube_diameter_mm",None)) if self.document else None

    @property
    def drag_coefficient(self):
        return float(self.document.get("drag_coefficient",None)) if self.document else None

    @property
    def empty_weight_g(self):
        return float(self.document.get("empty_weight_g",None)) if self.document else None

    @property
    def engine(self):
        return self._engine

    @engine.setter
    def engine(self, value):
        self._engine = value

    def mass_at(self,time):
         assert self.engine.mass_at(time) is not None
         assert self.empty_weight_g  is not None
         return self.empty_weight_g + self.engine.mass_at(time)

    def cross_sectional_area(self):
      diameter_m = self.diameter/1000.0
      return math.pi*(diameter_m**2.0)/4

    def __str__(self):
        uniqueTable = prettytable.PrettyTable(["ID","Name", "Max Dia MM", "Weight G", "Cd"])
        uniqueTable.add_row([self.id,self.name,self.diameter, self.empty_weight_g, self.drag_coefficient])
        return str(uniqueTable)