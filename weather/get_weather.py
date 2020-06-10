import xml.etree.ElementTree as ET
from numpy import random

# parse xml file. returns info about weather 
def get_weather(file_name):
    tree = ET.parse(file_name)
    root = tree.getroot()
    weather = dict()
    for child in root:
        if child.tag in weather:
            raise SyntaxError("Weather duplicate.")
        weather[child.tag] = child.attrib

    xp, yp = -1, -1
    for w in weather:
        if 'x' in weather[w] and 'y' in weather[w]:
            xp = [float(i) for i in weather[w]['x'].split(", ")]
            yp = [float(i) for i in weather[w]['y'].split(", ")]

        if 'value' not in weather[w]:
            weather[w]['value'] = random.uniform(0, 100)
        elif float(weather[w]['value']) > 100 or float(weather[w]['value']) < 0:
            raise SyntaxError("Value must be in [0, 100]")

    return weather, xp, yp

    for w in weather:
        if 'value' not in w:
            weather[w]['value'] = random.uniform(0, 100)

    return weather
