def SnowChangeAccel(weather_val, param):
    if (weather_val <= 12.5):
        return param
    else:
        return param / (0.08 * weather_val)

def SnowChangeColor(weather_val, color_values):
    # RGB color
    color_values[0] = 34
    color_values[1] = 139
    color_values[2] = 34
    return color_values

def RainChangeColor(weather_val, color_values):
    # RGB color
    color_values[0] = 231
    color_values[1] = 0
    color_values[2] = 34
    return color_values