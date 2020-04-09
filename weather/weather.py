import sys
import os

from get_weather import get_weather
from classes import *

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci


# return parametres of vehicle
def get_veh_params(veh_id):
    params = {'accel': traci.vehicle.getAccel(veh_id), 
              'decel': traci.vehicle.getDecel(veh_id),
              'maxSpeed': traci.vehicle.getMaxSpeed(veh_id),
              'minGap': traci.vehicle.getMinGap(veh_id)}

    return params

def consider_weather(w_info):
    all_vehs = list()
    w_list = list()
    for w_type, w_val in w_info:
        if w_type == "rain":
            w_list.append(Rain(w_val['value']))
        if w_type == "snow":
            print("here")
            w_list.append(Snow(w_val['value']))
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        vehs = traci.vehicle.getIDList()
        for veh_id in vehs:
            if veh_id not in all_vehs:
                veh_params = get_veh_params(veh_id)
                for w in w_list:
                    w.changeParams(veh_id, veh_params)
                all_vehs.append(veh_id)


def weather_main():
    weather = get_weather('data/weather.xml')
    consider_weather(weather.items())
