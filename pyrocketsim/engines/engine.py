from scipy.interpolate import interp1d

class Engine(object):
    property_map = {'initWt': 'initial_weight', 'propWt':'prop_weight', 'burn-time':'burn_time'}

    def __init__(self,**kwargs):
        keys_ok = ["code","mfg","initWt","delays", "propWt", "dia", "len", "burn-time","comment"]
        for name, value in kwargs.items():
            if name in keys_ok:
                try:
                    try:
                        if self.property_map[str(name)]:
                            new_key = self.property_map[name]
                    except KeyError:
                        new_key = name

                    setattr(self,new_key, float(value))
                except ValueError:
                    setattr(self,name, value)
        self._time_step = 0.005
        self.f_curve = None
        self.m_curve = None


    @property
    def data_points(self):
        return self._data_points

    @data_points.setter
    def data_points(self,value):
        self._data_points = value
        start_time = 0.0
        total_time = float(self._data_points[-1][0])
        number_data_points = total_time/self._time_step
        force = [float(x[1]) for x in self._data_points ]
        mass = [x[2] for x in self._data_points]
        self.f_curve  = interp1d([float(x[0]) for x in self._data_points ],force,kind="cubic")
        self.m_curve =  interp1d([float(x[0]) for x in self._data_points ],mass,kind="cubic")

    def force_at(self,time):
        try:
            if self.f_curve:
                return float(self.f_curve(time))
        except ValueError:
            return 0.0

    def mass_at(self,time):
        try:
            if self.m_curve:
                return (float(getattr(self,'initial_weight'))- float(getattr(self,'prop_weight'))) + self.m_curve(time)
        except ValueError:
            return (float(getattr(self,'initial_weight'))- float(getattr(self,'prop_weight')))

    @property
    def time_step(self):
        return self._time_step

    @time_step.setter
    def time_step(self,value):
        self.time_step = value


    def __str__(self):
        assert self.mfg is not None
        assert self.code is not None
        assert self.dia is not None
        assert self.len is not None
        return "%s %s %s %s" % (self.mfg,self.code,self.dia,self.len)