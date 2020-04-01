from get_weather import get_weather
from snow_functions import *
from classes import *
import sys, os

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci

# return parametres of vehicle
def get_veh_params(veh_id):
    params = {
        'accel': 0.0,
        'decel': 0.0,
        'maxSpeed': 0.0,
        'minGap': 0.0
    }

    params['accel'] = traci.vehicle.getAccel(veh_id)
    params['decel'] = traci.vehicle.getDecel(veh_id)
    params['maxSpeed'] = traci.vehicle.getMaxSpeed(veh_id)
    params['minGap'] = traci.vehicle.getMinGap(veh_id)

    return params

# snow influences all vehicles
def consider_snow(snow_val):
    all_vehs = list()
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        vehs = traci.vehicle.getIDList()
        for veh_id in vehs:
            if veh_id not in all_vehs:
                veh_params = get_veh_params(veh_id)
                s = Snow(snow_val)
                s.changeParams(veh_id, veh_params)
                all_vehs.append(veh_id)
        #if 'left_0' in vehs:
            # print(traci.vehicle.getSpeed('left_0'))


def weather_main():
    weather = get_weather('data/weather.xml')
    if 'snow' in weather:
        snow_val = weather['snow']['value']
        consider_snow(snow_val)
    if 'rain' in weather:
        rain_val = weather['rain']['value']
        # consider_rain(rain_val)
