# fhnw-idb-IoT-Data-Collection

Im Rahmen des Moduls "idb - IoT-Datenbeschaffung" an der FHNW habe ich eine kleine Minichallenge durchgeführt, bei der ich Daten aus meiner Umgebung gesammelt habe und diese auf ThingSpeak visualisiert. 

![image](https://github.com/7ben18/fhnw-idb-IoT-Data-Collection/assets/66916399/95708a31-b6b6-4889-9a76-d2791d4472fa)

# ThingSpeak Channel
- [ThingSpeak Channel](https://thingspeak.com/channels/2049970/private_show)  
Anmeldung auf ThingSpeak erforderlich

![image](https://github.com/7ben18/fhnw-idb-IoT-Data-Collection/assets/66916399/937efd86-f8a9-4ed4-ab07-1791dc6f6f48)

# Hardware 

- [Grove Shield for Feather](https://github.com/fhnw-imvs/fhnw-idb/wiki/Grove-Adapters#grove-shield-for-feather)

- [Feather nRF52840 Express](https://github.com/fhnw-imvs/fhnw-idb/wiki/Feather-nRF52840-Express)

- [Button](https://github.com/fhnw-imvs/fhnw-idb/wiki/Grove-Sensors#button)

- [Temperature & Humidity Sensor (DHT11)](https://github.com/fhnw-imvs/fhnw-idb/wiki/Grove-Sensors#temperature--humidity-sensor-dht11)

- [Light Sensor v1.2](https://github.com/fhnw-imvs/fhnw-idb/wiki/Grove-Sensors#light-sensor-v12)

- [Chainable RGB LED](https://github.com/fhnw-imvs/fhnw-idb/wiki/Grove-Actuators#chainable-rgb-led)

- [4-Digit Display (TM1637)](https://github.com/fhnw-imvs/fhnw-idb/wiki/Grove-Actuators#4-digit-display-tm1637)

# Software
- [CircuitPython](https://github.com/fhnw-imvs/fhnw-idb/tree/master/data-acquisition/CircuitPython)

# Repository Struktur

| File | Beschreibung |
| ------ | ------ |
| Archiv | archivierte Files, meistens py Testversuche | 
| Circuitpython_Introduction | Einführung in Circuitpython, einige Python Testfiles |
| lib | Circuitpython Bibliotheken |
| .gitignore | Files die nicht in das Repository aufgenommen werden sollen |
| ChainableLED | Bibliothek für die ChainableLEDs |
| code.py | Main Code für den Circuitpython | 
| config.py | Konfigurationsfile für den Circuitpython, API-Key, Passwort etc... |
| umgeungsdaten.csv | Die gemessenen Umgebungsdaten als csv abgespeichert | 
| README.md | Beschreibung des Repositorys |

