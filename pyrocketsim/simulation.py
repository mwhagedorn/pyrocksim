import math
import prettytable
import numpy as np
from scipy.interpolate import interp1d
from termcolor import colored

GRAV = 9.80665

#density of air
RHO = 1.2505

class Simulation(object):

    def __init__(self, rocket,engine):
        self._rocket = rocket
        self._engine = engine

    @property
    def rocket(self):
        return self._rocket

    @property
    def engine(self):
        return self._engine

    def execute(self):
        self.rocket.engine = self.engine
        self._simTable = prettytable.PrettyTable(["Time Stamp","Force", "Altitude", "Velocity", "Mass", "Acceleration",])
        self._summaryTable = prettytable.PrettyTable(["Apogee","Burnout V","Max A", "Ave A", "Burn Time", "Burnout Altitude", "Coast Time","Coast Distance","Eject Time","Launch Rod V"])
        self._simTable.align = "l"
        self._simTable.float_format = "6.4"
        self._summaryTable.align = "l"
        self._summaryTable.float_format="6.4"
        self._data = []

        self._time_stamp       = 0
        self._current_velocity = 0.0
        self._max_velocity     = 0
        self._max_acceleration = 0
        self._altitude         = 0
        self._time_step        = 0.005
        self._velocity         = 0
        self._accelleration    = 0
        self._total_mass       = self.rocket.mass_at(0.0)/1000
        self._motor_force      = 0
        area = self.rocket.cross_sectional_area()
        self._drag_constant =  (RHO*self.rocket.drag_coefficient*area)/2

        assert self._total_mass is not None
        self.log()
        self.velocity_at_instant()

        #boost
        while (self._current_velocity > 0 or self._time_stamp < self.burn_time()) and self.remaining_delay_time() > 0:
            self.velocity_at_instant()

        while self.remaining_delay_time() > 0:
            self.velocity_at_instant()




        print(self._simTable)
        self._summaryTable.add_row([self.apogee(),self.max_velocity(), self.max_acceleration(),self.ave_acceleration(),self.burn_time(), self.burnout_altitude(), self.coast_to_apogee_time(),self.coast_distance(),self.total_delay_time(), self.end_of_launch_rod_velocity()])
        print(self._summaryTable)
        print(self.remaining_delay_time())
        return



    def log(self):
        self._simTable.add_row([self._time_stamp, self._motor_force, self._altitude, self._current_velocity, self._total_mass, self._accelleration])
        self._data.append((self._time_stamp,self._motor_force,self._altitude, self._current_velocity, self._total_mass, self._accelleration))
        return


    def velocity_at_instant(self):
      self._motor_force = self.engine.force_at(self._time_stamp)
      self._total_mass  = self.rocket.mass_at(self._time_stamp)/1000
      self._time_stamp  += self._time_step

      memo_velocity = self._current_velocity
      self._altitude, self._current_velocity = self.rk4(memo_velocity)

      if self._altitude < 0:
          self._altitude = 0.0

      if self._current_velocity < 0 and self._time_stamp < self.burnout_time():
          self._current_velocity = 0.0

      self._accelleration = (self._current_velocity - memo_velocity)/self._time_step * 0.101971621

      # if self._current_velocity < 0
      #   interpolate_apogee_value
      # end

      self.log()
      self.check_max_velocity()
      self.check_max_accell()

    def rk4(self,velocity):
      dt = self._time_step
      k1             = dt*self.altitude_derivative_at_n(velocity)
      l1             = dt*self.velocity_derivative_at_n(velocity)
      k2             = dt*self.altitude_derivative_at_n(velocity)
      l2             = dt*self.velocity_derivative_at_n(velocity+l1/2.0)
      k3             = dt*self.altitude_derivative_at_n(velocity+l2/2.0)
      l3             = dt*self.velocity_derivative_at_n(velocity+l2/2.0)
      k4             = dt*self.altitude_derivative_at_n(velocity+l3)
      l4             = dt*self.velocity_derivative_at_n(velocity+l3)
      altitude_n     = self._altitude+1.0/6.0*(k1+2.00*k2+2.00*k3+k4)
      velocity_n     = velocity+1.0/6.0*(l1+2.00*l2+2.00*l3+l4)
      return (altitude_n, velocity_n)

    def velocity_derivative_at_n(self,velocity,angle=90):
      # vertical forces = (thrust(t) - drag(t))*sin(angle) - weight
      # a = f/m
      angle_rad = angle * math.pi/180
      drag_force = self._drag_constant*(velocity**2)
      weight_force = self._total_mass*GRAV
      return ((self._motor_force-drag_force)*math.sin(angle_rad)-weight_force)/self._total_mass

    def altitude_derivative_at_n(self,velocity):
      return velocity

    def burn_time(self):
        return self.engine.burn_time

    def interpolate_apogee_value(self):
      pass
      # vel_distance          = @data.last[:velocity] + -1*self.current_velocity
      # pct                   = (1.0 - -1*self.current_velocity/vel_distance)
      # alt_distance          = self.altitude - @data.last[:altitude]
      # new_altitude          = alt_distance*pct + @data.last[:altitude]
      # self.altitude         = new_altitude
      # self.current_velocity = 0

    def check_max_velocity(self):
        pass

    def check_max_accell(self):
        pass

    def apogee(self):
        altitudes = [data[2] for data in self._data]
        return max(altitudes)

    def burnout_altitude(self):
        altitude = [x[2] for x in self._data]
        self.a_curve  = interp1d([float(x[0]) for x in self._data ],altitude,kind="cubic")
        return self.a_curve(self.burnout_time())

    def burnout_time(self):
        return self.engine.burn_time

    def max_velocity(self):
        velocities = [data[3] for data in self._data]
        return max(velocities)

    def max_acceleration(self):
        accells = [data[5] for data in self._data]
        return max(accells)

    def ave_acceleration(self):
        accells = [data[5] for data in self._data if data[5] > 0]
        return np.mean(accells)

    def coast_to_apogee_time(self):
        if self._data[-1][3] > 0.0001:
            # eject while still fast
            return self.total_delay_time();

        row = next(x for x in self._data if (x[3] < 0.0001 and x[0] > self.burnout_time()))
        apogee_time = row[0]
        coast_time = apogee_time - self.burnout_time()
        return coast_time

    def end_of_launch_rod_velocity(self):
         row = next(x for x in self._data if x[2] >= 1.0 )
         value = row[3]
         if value > 15.0:
             return colored(value,color="green")
         else:
             return colored(value,color="red")

    def coast_distance(self):
        return self.apogee() - self.burnout_altitude()

    def total_delay_time(self):
        return 3.0

    def remaining_delay_time(self):
        return self.total_delay_time() - (self._time_stamp - self.burnout_time())




if __name__ == '__main__':

    from repository import Repository
    repo = Repository()
    rocket = repo.find_rocket_by_name("esteslj2")
    assert rocket is not None
    engine = repo.find_engine_by_code("D12")
    assert engine is not None

    print(Simulation(rocket,engine).execute())
