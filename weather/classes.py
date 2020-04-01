import os, sys
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci

class Weather:
    def __init__(self, weather_val=1.0):
        self.weather_val = float(weather_val)

    def changeAccel(self, veh_id, param):
        pass

    def changeDecel(self, veh_id, param):
        pass

    def changeMaxSpeed(self, veh_id, param):
        pass

    def changeMinGap(self, veh_id, param):
        pass

    def changeParams(self, veh_id, veh_params):
        self.changeAccel(veh_id, veh_params['accel'])
        self.changeDecel(veh_id, veh_params['decel'])
        self.changeMaxSpeed(veh_id, veh_params['maxSpeed'])
        self.changeMinGap(veh_id, veh_params['minGap'])

    def printAll(self):
        print(self.weather_val)


class Snow(Weather, object):
    def __init__(self, snow_val=1.0):
        super(Snow, self).__init__(snow_val)

    def changeAccel(self, veh_id, param):
        if (self.weather_val <= 12.5):
            traci.vehicle.setAccel(veh_id, 1.0)
        else:
            traci.vehicle.setAccel(veh_id, param / (0.08 * self.weather_val))

    def changeDecel(self, veh_id, param):
        if (self.weather_val <= 12.5):
            traci.vehicle.setDecel(veh_id, 1.0)
        else:
            traci.vehicle.setDecel(veh_id, param / (0.08 * self.weather_val))

    def changeMaxSpeed(self, veh_id, param):
        if (self.weather_val <= 12.5):
            traci.vehicle.setMaxSpeed(veh_id, 1.0)
        else:
            traci.vehicle.setMaxSpeed(veh_id, param / (0.08 * self.weather_val))

    def changeMinGap(self, veh_id, param):
        traci.vehicle.setMinGap(veh_id, param * (0.04 * self.weather_val))

# def main():
    # s = Snow(2)
    # s.changeParams('kn')

# if __name__ == '__main__':
#     main()
