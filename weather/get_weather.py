import xml.etree.ElementTree as ET
import re
from classes import *
from numpy.random import randint
from math import sin, cos, pi


# creates weather class
def createWClass(w_type, area, w_value):
    if w_type == "snow":
        return Snow(area, w_value)
    elif w_type == "rain":
        return Rain(area, w_value)


# draws areas and create weather classes
def drawAreas(weathers, w_type, weather, color):
    a_num = 0
    for gl in weather.findall('global'):
        weathers.append(createWClass(w_type, ["global", ""], float(gl.get('value'))))

    for polygon in weather.findall('polygon'):
        shape = list()
        xp = list([float(i) for i in polygon.get('x').split(", ")])
        yp = list([float(i) for i in polygon.get('y').split(", ")])
        for i in range(len(xp)):
            shape.append((xp[i], yp[i]))
        shape.append((xp[0], yp[0]))
        weathers.append(createWClass(w_type, ["polygon", polygon], float(polygon.get('value'))))
        traci.polygon.add('r' + str(a_num) + str(randint(0, 10 ** 6)), shape, (0, 0, 255))
        a_num += 1

    for circle in weather.findall('circle'):
        c_x = float(circle.get('c_x'))
        c_y = float(circle.get('c_y'))
        r = float(circle.get('r'))
        num_vertices = 3
        shape = list()
        weathers.append(createWClass(w_type, ["circle", circle], float(circle.get('value'))))
        while 2 * r * sin(pi / num_vertices) > 10:
            num_vertices += 1
        print(num_vertices)
        for i in range(num_vertices):
            shape.append((c_x + r * cos(2 * pi * i / num_vertices),
                          c_y + r * sin(2 * pi * i / num_vertices)))
        traci.polygon.add('r' + str(a_num) + str(randint(0, 10 ** 6)), shape, (0, 0, 255))
        a_num += 1


# parse xml file. returns info about weather
def get_weather(file_name):
    tree = ET.parse(file_name)
    root = tree.getroot()

    weathers = []
    for rain in root.findall('rain'):
        drawAreas(weathers, "rain", rain, (0, 0, 255))
    for snow in root.findall('snow'):
        drawAreas(weathers, "snow", snow, (175, 238, 238))

    return weathers
