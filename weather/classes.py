import os, sys
from default_weather_funcs import *

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci

FLAG = 0
if os.path.exists(os.getcwd() + '/data/weather_funcs.py'):
    FLAG = 1
    FUNCS = os.getcwd() + '/data/'
    sys.path.append(FUNCS)
    import weather_funcs


# checks if veh in polygon
def inPolygon(veh_id, xp, yp):
    x = traci.vehicle.getPosition(veh_id)[0]
    y = traci.vehicle.getPosition(veh_id)[1]
    c = 0
    for i in range(len(xp)):
        if (((yp[i] <= y and y < yp[i - 1]) or (yp[i - 1] <= y and y < yp[i])) and \
                (x > (xp[i - 1] - xp[i]) * (y - yp[i]) / (yp[i - 1] - yp[i]) + xp[i])): c = 1 - c

    return c


def inCircle(veh_id, c_x, c_y, r):
    x = traci.vehicle.getPosition(veh_id)[0]
    y = traci.vehicle.getPosition(veh_id)[1]
    return ((c_x - x) ** 2 + (c_y - y) ** 2) ** 0.5 <= r


def inArea(veh_id, a_type, a_params):
    if a_type == 'global':
        return True
    if a_type == 'polygon':
        xp = a_params[0]
        yp = a_params[1]
        return inPolygon(veh_id, xp, yp)
    elif a_type == 'circle':
        c_x = a_params[0]
        c_y = a_params[1]
        r = a_params[2]
        return inCircle(veh_id, c_x, c_y, r)


# return parametres of vehicle
def get_veh_params(veh_id):
    params = {
        'accel': traci.vehicle.getAccel(veh_id),
        'color': traci.vehicle.getColor(veh_id),
        'decel': traci.vehicle.getDecel(veh_id),
        'maxSpeed': traci.vehicle.getMaxSpeed(veh_id),
        'minGap': traci.vehicle.getMinGap(veh_id),
        'tau': traci.vehicle.getTau(veh_id),
        'zlane': traci.vehicle.getLaneID(veh_id)
    }

    return params


class Weather:
    def __init__(self, area, weather_val=1.0):
        self.weather_val = float(weather_val)  # how strong is weather
        self.area = area  # where is weather
        self.name = "none"

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

    def changeSpeed(self, veh_id, param):
        pass

    def changeHeadwayTime(self, veh_id, param):
        pass

    def changeParams(self, veh_id, veh_params):
        self.changeAccel(veh_id, veh_params['accel'])
        self.changeDecel(veh_id, veh_params['decel'])
        self.changeMaxSpeed(veh_id, veh_params['maxSpeed'])
        self.changeMinGap(veh_id, veh_params['minGap'])
        self.changeColor(veh_id, veh_params['color'])
        self.changeSpeed(veh_id, veh_params['zlane'])
        self.changeHeadwayTime(veh_id, veh_params['tau'])

    def printWValue(self):
        print(self.weather_val)


class Snow(Weather, object):
    def __init__(self, area, snow_val=1.0):
        super(Snow, self).__init__(area, snow_val)
        self.name = "snow"

    def changeAccel(self, veh_id, param):
        if FLAG and 'SnowChangeAccel' in dir(weather_funcs):
            traci.vehicle.setAccel(veh_id, weather_funcs.SnowChangeAccel(self.weather_val, param))
        else:
            SnowChangeAccelD(self.weather_val, veh_id, param)

    def changeDecel(self, veh_id, param):
        if FLAG and 'SnowChangeDecel' in dir(weather_funcs):
            traci.vehicle.setDecel(veh_id, weather_funcs.SnowChangeDecel(self.weather_val, param))
        else:
            SnowChangeDecelD(self.weather_val, veh_id, param)

    def changeMaxSpeed(self, veh_id, param):
        if FLAG and 'SnowChangeMaxSpeed' in dir(weather_funcs):
            traci.vehicle.setMaxSpeed(veh_id,
                                      weather_funcs.SnowChangeMaxSpeed(self.weather_val, param))
        else:
            SnowChangeMaxSpeedD(self.weather_val, veh_id, param)

    def changeSpeedFactor(self, veh_id, param):
        if FLAG and 'SnowChangeSpeedFactor' in dir(weather_funcs):
            traci.vehicle.setSpeedFactor(veh_id,
                                         weather_funcs.SnowChangeSpeedFactor(self.weather_val, param))
        else:
            SnowChangeSpeedFactorD(self.weather_val, veh_id, param)

    def changeMinGap(self, veh_id, param):
        if FLAG and 'SnowChangeMinGap' in dir(weather_funcs):
            traci.vehicle.setMinGap(veh_id, weather_funcs.SnowChangeMinGap(self.weather_val, param))
        else:
            SnowChangeMinGapD(self.weather_val, veh_id, param)

    def changeHeadwayTime(self, veh_id, param):
        if FLAG and 'SnowChangeHeadwayTime' in dir(weather_funcs):
            traci.vehicle.setMinGap(veh_id, weather_funcs.SnowChangeHeadwayTime(self.weather_val, param))
        else:
            SnowChangeHeadwayTimeD(self.weather_val, veh_id, param)

    def changeColor(self, veh_id, param):
        if FLAG and 'SnowChangeColor' in dir(weather_funcs):
            color_values = list(param)
            traci.vehicle.setColor(veh_id, tuple(
                weather_funcs.SnowChangeColor(self.weather_val, color_values)))
        else:
            SnowChangeColorD(self.weather_val, veh_id, param)


class Rain(Weather, object):
    def __init__(self, area, rain_val=1.0):
        super(Rain, self).__init__(area, rain_val)
        self.name = "rain"

    def changeAccel(self, veh_id, param):
        if FLAG and 'RainChangeAccel' in dir(weather_funcs):
            traci.vehicle.setAccel(veh_id, weather_funcs.RainChangeAccel(self.weather_val, param))
        else:
            RainChangeAccelD(self.weather_val, veh_id, param)

    def changeDecel(self, veh_id, param):
        if FLAG and 'RainChangeDecel' in dir(weather_funcs):
            traci.vehicle.setDecel(veh_id, weather_funcs.RainChangeDecel(self.weather_val, param))
        else:
            RainChangeDecelD(self.weather_val, veh_id, param)

    def changeMaxSpeed(self, veh_id, param):
        if FLAG and 'RainChangeMaxSpeed' in dir(weather_funcs):
            traci.vehicle.setMaxSpeed(veh_id,
                                      weather_funcs.RainChangeMaxSpeed(self.weather_val, param))
        else:
            RainChangeMaxSpeedD(self.weather_val, veh_id, param)

    def changeSpeedFactor(self, veh_id, param):
        if FLAG and 'RainChangeSpeedFactor' in dir(weather_funcs):
            traci.vehicle.setSpeedFactor(veh_id,
                                         weather_funcs.RainChangeSpeedFactor(self.weather_val, param))
        else:
            RainChangeSpeedFactorD(self.weather_val, veh_id, param)

    def changeMinGap(self, veh_id, param):
        if FLAG and 'RainChangeMinGap' in dir(weather_funcs):
            traci.vehicle.setMinGap(veh_id, weather_funcs.RainChangeMinGap(self.weather_val, param))
        else:
            RainChangeMinGapD(self.weather_val, veh_id, param)

    def changeHeadwayTime(self, veh_id, param):
        if FLAG and 'RainChangeHeadwayTime' in dir(weather_funcs):
            traci.vehicle.setMinGap(veh_id, weather_funcs.RainChangeHeadwayTime(self.weather_val, param))
        else:
            RainChangeHeadwayTimeD(self.weather_val, veh_id, param)

    def changeColor(self, veh_id, param):
        if FLAG and 'RainChangeColor' in dir(weather_funcs):
            color_values = list(param)
            traci.vehicle.setColor(veh_id, tuple(
                weather_funcs.RainChangeColor(self.weather_val, color_values)))
        else:
            RainChangeColorD(self.weather_val, veh_id, param)


class Vehicle:
    def __init__(self, veh_id, a_type="none", a_params=tuple()):
        self.id = veh_id
        if veh_id == "none":
            self.original_params = tuple()
        else:
            self.original_params = tuple(sorted(get_veh_params(self.id).items()))
        self.area_type = a_type
        self.area_params = a_params

    def in_area(self):
        return inArea(self.id, self.area_type, self.area_params)

    def restore_params(self):
        traci.vehicle.setAccel(self.id, self.original_params[0][1])
        traci.vehicle.setColor(self.id, self.original_params[1][1])
        traci.vehicle.setDecel(self.id, self.original_params[2][1])
        traci.vehicle.setMaxSpeed(self.id, self.original_params[3][1])
        traci.vehicle.setMinGap(self.id, self.original_params[4][1])
        traci.vehicle.setTau(self.id, self.original_params[5][1])
        traci.vehicle.setSpeedFactor(self.id, 1)