import xml.etree.ElementTree as ET

# parse xml file. returns info about weather 
def get_weather(file_name):
    tree = ET.parse(file_name)
    root = tree.getroot()
    weather = dict()
    for child in root:
        if child.tag in weather:
            raise SyntaxError("Weather duplicate.")
        weather[child.tag] = child.attrib
    return weather
