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
    for w in weather:
        if 'value' not in w:
            weather[w]['value'] = random.uniform(0, 100)

    return weather

def main():
    print get_weather('../traci_tls_weather/data/weather.xml')


if __name__ == '__main__':
    main()
