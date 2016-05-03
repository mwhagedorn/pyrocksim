import os

from engine import Engine


class ENGParser(object):
    def __init__(self,filename):
        self._filename = filename
        self._comment = ""

    def parse(self):
        if not os.path.exists(self._filename):
            return False
        lines = []
        code = ""
        dia = 0.0
        length = 0.0
        mfg = ""
        delays=""
        mass = 0.0
        prop_mass = 0.0
        data_points = []

        with open(self._filename) as f:
            lines = f.readlines()
        for line in lines:
            if line.startswith(";"):
                self._comment += line
            tokens = line.split()
            kwargs = {}
            if len(tokens) == 7:
                code = tokens[0]
                dia = float(tokens[1])
                length = float(tokens[2])
                delays = tokens[3]
                prop_mass = float(tokens[4]) * 1000.0
                mass = float(tokens[5]) * 1000.0
                mfg = tokens[6]
            if len(tokens) == 2:
                tokens = line.split()
                # TODO calculate the mass curve on each iteration
                timestamp = tokens[0]
                force = tokens[1]
                data_points.append([float(timestamp), float(force),0.0])

            if len(data_points):
                mass_increment = mass/len(data_points)

                for i in range(0,len(data_points)):
                    data_points[i][2] = i*mass_increment


            kwargs['code'] = code
            kwargs['len'] = length
            kwargs['comment'] = self._comment
            kwargs['dia'] = dia
            kwargs['propWt'] = prop_mass
            kwargs['initWt'] = mass
            kwargs['mfg'] = mfg

        engine = Engine(**kwargs)

        engine.data_points = data_points

        return engine

    def comment(self):
        return self._comment
