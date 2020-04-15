import os, sys

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci


# return parametres of vehicle
def get_veh_params(veh_id):
    params = {'accel': traci.vehicle.getAccel(veh_id),
              'color': traci.vehicle.getColor(veh_id),
              'decel': traci.vehicle.getDecel(veh_id),
              'maxSpeed': traci.vehicle.getMaxSpeed(veh_id),
              'minGap': traci.vehicle.getMinGap(veh_id)}

    return params

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

    def changeColor(self, veh_id, param):
        pass

    def changeParams(self, veh_id, veh_params):
        self.changeAccel(veh_id, veh_params['accel'])
        self.changeDecel(veh_id, veh_params['decel'])
        self.changeMaxSpeed(veh_id, veh_params['maxSpeed'])
        self.changeMinGap(veh_id, veh_params['minGap'])
        self.changeColor(veh_id, veh_params['color'])

    def printWValue(self):
        print(self.weather_val)


class Snow(Weather, object):
    def __init__(self, snow_val=1.0):
        super(Snow, self).__init__(snow_val)

    def changeAccel(self, veh_id, param):
        if (self.weather_val <= 12.5):
            traci.vehicle.setAccel(veh_id, param)
        else:
            traci.vehicle.setAccel(veh_id, param / (0.08 * self.weather_val))

    def changeDecel(self, veh_id, param):
        if (self.weather_val <= 12.5):
            traci.vehicle.setDecel(veh_id, param)
        else:
            traci.vehicle.setDecel(veh_id, param / (0.08 * self.weather_val))

    def changeMaxSpeed(self, veh_id, param):
        if (self.weather_val <= 12.5):
            traci.vehicle.setMaxSpeed(veh_id, param)
        else:
            traci.vehicle.setMaxSpeed(veh_id, param / (0.08 * self.weather_val))

    def changeMinGap(self, veh_id, param):
        traci.vehicle.setMinGap(veh_id, param * (0.04 * self.weather_val))

    def changeColor(self, veh_id, param):
        color_values = list(param)
        print(param)
        color_values[3] = 50
        traci.vehicle.setColor(veh_id, tuple(color_values))


class Rain(Weather, object):
    def __init__(self, snow_val=1.0):
        super(Rain, self).__init__(snow_val)

    def changeAccel(self, veh_id, param):
        if self.weather_val <= 12.5:
            traci.vehicle.setAccel(veh_id, param)
        else:
            traci.vehicle.setAccel(veh_id, param / (0.03 * self.weather_val))

    def changeDecel(self, veh_id, param):
        if self.weather_val <= 12.5:
            traci.vehicle.setDecel(veh_id, param)
        else:
            traci.vehicle.setDecel(veh_id, param / (0.03 * self.weather_val))

    def changeMaxSpeed(self, veh_id, param):
        if self.weather_val <= 12.5:
            traci.vehicle.setMaxSpeed(veh_id, param)
        else:
            traci.vehicle.setMaxSpeed(veh_id, param / (0.03 * self.weather_val))

    def changeColor(self, veh_id, param):
        color_values = list(param)
        color_values[0] /= 2
        color_values[1] /= 3
        color_values[2] = 255
        traci.vehicle.setColor(veh_id, tuple(color_values))

    def changeMinGap(self, veh_id, param):
        traci.vehicle.setMinGap(veh_id, param * (0.03 * self.weather_val))


class Vehicle:
    def __init__(self, veh_id, xp, yp):
        self.id = veh_id
        self.inPoly = list()
        self.inPoly.append(False)
        self.original_params = tuple(sorted(get_veh_params(self.id).items()))
        self.polygon_x = xp
        self.polygon_y = yp

    def restore_params(self):
        traci.vehicle.setAccel(self.id, self.original_params[0][1])
        traci.vehicle.setColor(self.id, self.original_params[1][1])
        traci.vehicle.setDecel(self.id, self.original_params[2][1])
        traci.vehicle.setMaxSpeed(self.id, self.original_params[3][1])
        traci.vehicle.setMinGap(self.id, self.original_params[4][1])
