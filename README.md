# Weather station based on ESP8266 and BME280

[![Weather Station GUI by Krzysztof Brzozowski](https://krzysztofbrzozowski.pl/media/2020/02/01/iot-api-lrg.png)](https://krzysztofbrzozowski.pl)

Simple weather station running on ESP8266 and BME280. PCB, schematic and obj files you can download from repository [weather_station_ESP8266_PCB](https://github.com/krzysztofbrzozowski/weather_station_ESP8266_PCB).
Station is sending data to custom written [IoT_API](https://github.com/krzysztofbrzozowski/IoT_API). The data you can read by [IoT_GUI](https://github.com/krzysztofbrzozowski/IoT_GUI).
Firmware ESP8266 in MicroPython you can find here: [weather_station_ESP8266_firmware](https://github.com/krzysztofbrzozowski/weather_station_ESP8266_firmware).

Whole project is describerd in polish on my webpage: https://krzysztofbrzozowski.com/project/termo-wifi-monitoring-temperatury-przez-internet/

## Repository Contents

- **/core** - main application for requests handling
- **/IoT_API** - settings etc.
- **/static_in_env** - all static files
- **/templates** - .html templates
