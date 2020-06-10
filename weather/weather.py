import os
import sys

from classes import *
from get_weather import get_weather
from pyllist import *
from random import randint
from math import sin, cos, pi

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


def createWClass(w_type, w_value):
    if w_type == "snow":
        return Snow(w_value)
    elif w_type == "rain":
        return Rain(w_value)


def changeAParams(veh_id, vehs_set, w, area, a_type):
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
        w.changeParams(veh_id, get_veh_params(veh_id))
        return ret_val
    else:
        return Vehicle("none")


def changeWParams(w_type, w_info, veh_id, vehs_set):
    ret_val = Vehicle("none")
    for polygon in w_info.findall('polygon'):
        w = createWClass(w_type, float(polygon.get('value')))
        if ret_val.id == "none":
            ret_val = changeAParams(veh_id, vehs_set, w, polygon, 'polygon')
    for circle in w_info.findall('circle'):
        w = createWClass(w_type, float(circle.get('value')))
        if ret_val.id == "none":
            ret_val = changeAParams(veh_id, vehs_set, w, circle, 'circle')
    return ret_val


def drawAreas(weather, color):
    a_num = 0
    for polygon in weather.findall('polygon'):
        shape = list()
        xp = list([float(i) for i in polygon.get('x').split(", ")])
        yp = list([float(i) for i in polygon.get('y').split(", ")])
        for i in range(len(xp)):
            shape.append((xp[i], yp[i]))
        shape.append((xp[0], yp[0]))
        traci.polygon.add('r' + str(a_num) + str(randint(0, 10 ** 6)), shape, (0, 0, 255))
        a_num += 1
    for circle in weather.findall('circle'):
        c_x = float(circle.get('c_x'))
        c_y = float(circle.get('c_y'))
        r = float(circle.get('r'))
        num_vertices = 3
        shape = list()
        while 2 * r * sin(pi / num_vertices) > 5:
            num_vertices += 1
        print(num_vertices)
        for i in range(num_vertices):
            shape.append((c_x + r * cos(2 * pi * i / num_vertices),
                          c_y + r * sin(2 * pi * i / num_vertices)))
        traci.polygon.add('r' + str(a_num) + str(randint(0, 10 ** 6)), shape, (0, 0, 255))
        a_num += 1


def consider_weather_area(w_info):
    all_vehs = set()
    aff_vehs = dllist()
    for rain in w_info.findall('rain'):
        drawAreas(rain, (0, 0, 255))
    for snow in w_info.findall('snow'):
        drawAreas(snow, (175, 238, 238))
    # for w_type, w_val in w_info:
    #     if w_type == "rain":
    #         w_list.append(Rain(w_val['value']))
    #     if w_type == "snow":
    #         w_list.append(Snow(w_val['value']))

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        vehs = traci.vehicle.getIDList()
        for veh_id in vehs:
            for snow in w_info.findall('snow'):
                v = changeWParams('snow', snow, veh_id, all_vehs)
                if v.id != "none":
                    aff_vehs.append(v)
            for rain in w_info.findall('rain'):
                v = changeWParams('rain', rain, veh_id, all_vehs)
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
                if not flag:
                    curr_veh.value.restore_params()
                    aff_vehs.remove(curr_veh)
                    all_vehs.remove(curr_veh.value.id)
                curr_veh = temp


def weather_main():
    weather = get_weather('data/weather.xml')
    consider_weather_area(weather)
