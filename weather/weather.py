import sys
import os

from get_weather import get_weather
from classes import *

from pyllist import *

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci


def consider_weather(w_info):
    all_vehs = list()
    w_list = list()
    for w_type, w_val in w_info:
        if w_type == "rain":
            w_list.append(Rain(w_val['value']))
        if w_type == "snow":
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


# checks if veh in polygon
def inPolygon(veh_id, xp, yp):
    x = traci.vehicle.getPosition(veh_id)[0]
    y = traci.vehicle.getPosition(veh_id)[1]
    c = 0
    for i in range(len(xp)):
        if (((yp[i] <= y and y < yp[i - 1]) or (yp[i - 1] <= y and y < yp[i])) and \
                (x > (xp[i - 1] - xp[i]) * (y - yp[i]) / (yp[i - 1] - yp[i]) + xp[i])): c = 1 - c

    return c


def consider_weather_area(w_info, xp, yp):
    all_vehs = set()
    w_list = list()
    aff_vehs = dllist()
    for w_type, w_val in w_info:
        if w_type == "rain":
            w_list.append(Rain(w_val['value']))
        if w_type == "snow":
            w_list.append(Snow(w_val['value']))

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        vehs = traci.vehicle.getIDList()
        for veh_id in vehs:
            if veh_id not in all_vehs and inPolygon(veh_id, xp, yp):
                aff_vehs.append(Vehicle(veh_id, xp, yp))
                for w in w_list:
                    w.changeParams(veh_id, get_veh_params(veh_id))
                all_vehs.add(veh_id)
        if len(aff_vehs) > 0:
            curr_veh = aff_vehs.last
            for _ in range(len(aff_vehs)):
                temp = curr_veh.prev
                if not inPolygon(curr_veh.value.id, curr_veh.value.polygon_x,
                                 curr_veh.value.polygon_y):
                    curr_veh.value.restore_params()
                    aff_vehs.remove(curr_veh)
                curr_veh = temp


def weather_main():
    weather, xp, yp = get_weather('data/weather.xml')
    print(xp, yp)
    if xp == -1 and yp == -1:
        consider_weather(weather.items())
    else:
        print('here')
        consider_weather_area(weather.items(), xp, yp)
