import sys
import os
import xml.etree.ElementTree as ET
from get_weather import get_weather
from classes import *
from pyllist import *

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

import traci

# creates vehicle class, checks if vehicle in the weather area
def changeVehicleParams(veh_id, vehs_set, w, area, a_type):
    a_params = list()
    ret_val = Vehicle(veh_id, a_type, a_params)
    if a_type == 'polygon':
        a_params.append(list([float(i) for i in area.get('x').split(", ")]))
        a_params.append(list([float(i) for i in area.get('y').split(", ")]))
    elif a_type == 'circle':
        a_params.append(float(area.get('c_x')))
        a_params.append(float(area.get('c_y')))
        a_params.append(float(area.get('r')))
    if veh_id not in vehs_set and inArea(veh_id, a_type, a_params):
        vehs_set.add(veh_id)
        print("in", veh_id, traci.vehicle.getSpeed(veh_id), traci.lane.getMaxSpeed(traci.vehicle.getLaneID(veh_id)))
        w.changeParams(veh_id, get_veh_params(veh_id))
        return ret_val
    else:
        return Vehicle("none")

# "main"
def consider_weather_area(weathers):
    all_vehs = set()
    aff_vehs = dllist()

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        vehs = traci.vehicle.getIDList()
        for veh_id in vehs:
            v = Vehicle("none")
            for weather in weathers:
                v = changeVehicleParams(veh_id, all_vehs, weather, weather.area[1], weather.area[0])
                if v.id != "none":
                    aff_vehs.append(v)
            
        if len(aff_vehs) > 0:
            curr_veh = aff_vehs.last
            for _ in range(len(aff_vehs)):
                flag = 1
                temp = curr_veh.prev
                try:
                    flag = curr_veh.value.in_area()
                except traci.exceptions.TraCIException:
                    aff_vehs.remove(curr_veh)
                    all_vehs.remove(curr_veh.value.id)
                    flag = 1

                if not flag:
                    if traci.vehicle.getLaneID(curr_veh.value.id) != '':
                        print("out", curr_veh.value.id, traci.vehicle.getSpeed(curr_veh.value.id),
                              traci.lane.getMaxSpeed(traci.vehicle.getLaneID(curr_veh.value.id)))
                    curr_veh.value.restore_params()
                    aff_vehs.remove(curr_veh)
                    all_vehs.remove(curr_veh.value.id)
                curr_veh = temp


def weather_main():
    weathers = get_weather('data/weather.xml')
    consider_weather_area(weathers)
