# SUMO-Weather
Данный проект предоставляет возможность моделировать влияние погодных условий на транспортные потоки. Выполнено на основе [SUMO](https://sumo.dlr.de/docs/index.html) и интерфейса [TraCI](https://sumo.dlr.de/docs/TraCI.html).
### Технические требования
1. Linux или Mac OS
1. python3+ и библиотеки pyllist, numpy
1. Установленный пакет SUMO

### Требования от пользователя
* Знание английского
* Базовые знания python
* Опыт использования SUMO
* (желательно) Опыт использование TraCI

### Установка модуля
Прежде всего установить пакет SUMO, следуя инструкциям по [сслыке](https://sumo.dlr.de/docs/Installing.html). После того, как был установлен SUMO и определена переменная `$SUMO_HOME`, следует распаковать архив нашего проекта по пути `$SUMO_HOME/tools` и переименовать папку в `weather_project`.

### Использование
Прежде всего ознакомиться с двумя примерами, расположенными в папке */tests*. Для этого можно запустить исполняемый файл *runner.py* с помощью терминала(`./runner.py`)
Также желательно посмотреть на код файла *runner.py* (для удобства выложен в конце README). Примерно такой же файл должен запускать вашу симуляцию. Все необходимые параметры файлы с информацией о транспортной сети нужно передавать с помощью `.sumocfg`, путь до которого должен быть указан в аргументах команды `traci.start()` (см. пример).    
Для того, чтобы передать информацию о погоде, нужно передать её в файле `data/weather.xml`(Именно в папке *data*).   
Например,  
```xml
<snow>
    <polygon x="250, 250, 600, 600" y="450, 600, 600, 450" value="75"/>
</snow>
``` 
Подробнее как именно задавать погоду, можно посмотреть в файле `tests/double_cross/data/weather.xml`. На данный момент реализовано 3 вида зоны влияние погоды: в полигоне, в круге, на всей транспортной сети. По умолчанию сила погоды указывается с помощью значение *value* и должно находиться в отрезке [0, 100].  
По умолчанию, снег и дожь делится на три категории
* Слабый (value <= 35)
* Средние (35 < value <= 70)
* Сильный (70 < value <= 100)

В зависимости от силы погоды параметры меняются по-разному. По умолчанию погода с силой 0 и силой 35 будет влиять одинково, поскольку в различных исследовательских статьях чаще всего используется именно разделение на три категории силы снега или дождя.  
Пользователю предоставляется возможность создать файл `weather_funcs.py` в папке `data`, чтобы переопределить стандартные, нами написанные, "функции погоды", которые изменяют параметры автомобиля. Список функций, которые возможно переопределить
```python
def SnowChangeAccel(weather_val, param);
def SnowChangeDecel(weather_val, param);
def SnowChangeMaxSpeed(weather_val, param); # not recommended to change vehicle's physical maxSpeed
def SnowChangeMinGap(weather_val, param);
def SnowChangeHeadwayTime(weather_val, param);
def SnowChangeSpeed(weather_val, param); # changes desiredSpeed on current edge
def SnowChangeColoe(weather_val, color_values); # arg is RGBA list
```

Аналагично, для дождя функции будут `def Rain...();`. Функции должны возвращать значение, которое будет установлено при попадание в зону погоды. При этом *weather_val* означает силу погоды, а *param* значение в данный момент соответствующего параметра, который должен быть изменен. Пример можно увидеть в файле `tests/double_cross/data/weather_funcs.py`. 

### Структура репозитория
В папке *weather* расположены все файлы, связанные с погодой. В файле `classes.py` можно узнать, как устроеные классы погоды и др. В файле `default_weather_funcs.py` расположены "функции погоды" по умолчанию.  
В папке *tests* расположено два примера. Один из них написан нами самостоятельно (*double_cross*), второй сгенерирован с помощью встроенной в SUMO программы OSMWebWizard (развязка в Ярославле). В папке *results*, в файлах *.xlsx* можно сравнить показатели автомобилей за время симуляции с влиянием погоды и без.

### Пример runner.py

```python
#!/usr/bin/env python3
from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random # not necessarily

# import python modules from the $SUMO_HOME/tools directory including weather
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
    # path to weather
    sys.path.append(tools + '/weather_project')
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary
from weather import * # importing weather
import traci

# not necessarily
def generate_routefile():
   # ...

def run():
    weather_enable = 0 # weather_enable = 0 if you want to disable weather

    # enable or disable weather
    if weather_enable:
        weather_main()
    else:
        # runs simulation withoout weather
        while traci.simulation.getMinExpectedNumber() > 0:
            traci.simulationStep()

    traci.close() # closes connection with SUMO
    sys.stdout.flush()

if __name__ == "__main__":
    # returns path to sumo-gui
    sumoBinary = checkBinary('sumo-gui')

    generate_routefile() # not necessarily

    # start sumo using traci with given options
    traci.start([sumoBinary, "-c", "data/cross.sumocfg",
                             "--tripinfo-output", "tripinfo.xml",
                             "--collision.mingap-factor", "0",
                             "--fcd-output", "results/result_norain.xml",
                             "--no-warnings", "1",
                             "--ignore-route-errors", "1",])
    # runs simulation
    run()

```
