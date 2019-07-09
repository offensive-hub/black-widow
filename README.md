# Black Widow

[![Python 3.x](https://img.shields.io/badge/python-3.x-yellow.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/license-GPLv3-red.svg)](https://raw.githubusercontent.com/FabrizioFubelli/black-widow/master/LICENSE)

![image](resources/black-widow-img.png)


## Offensive penetration testing tool (Open Source)


### Features:
 - Sniffing
 - SQL Injection
 - Injected-database management
 - Web page parser
 - Website crawler
 - Multiple targets management
 - Mapping **{server -> vulnerabilities}**
 - Cluster between **black-widow** that are running inside the same network
 - Encrypted communications between other **black-widows**
 - Useful features for **CTF** challenges

##### Suggest you other features!


### Links:
 - Homepage: [https://black-widow.io](https://black-widow.io)
 - GitHub: [https://github.com/FabrizioFubelli/black-widow](https://github.com/FabrizioFubelli/black-widow)


### Docker Installation:
 1) If you haven't docker, [install it](https://docs.docker.com/install/linux/docker-ce/ubuntu)
 2) Build Docker: `docker build -t black-widow .`
 3) Run **black-widow**: `docker run black-widow <arguments>`


### Default Installation:
 1) Install dependencies: `sudo pip3 install -r requirements.txt`
 2) Run **black-widow**: `sudo ./black-widow.py <arguments>`


### Directories:
```
[root]
  |
  |-- app/      # Package principale dell'applicazione
  |    |
  |    |-- attack/         # Package per modalità di attacco
  |    |-- defense/        # Package per modalità di difesa
  |    |
  |    |-- gui/            # Package per la grafica dell'applicazione
  |    |
  |    |-- storage/        # Package per salvare i files (settings, output, ...)
  |    |
  |    |-- utils/
  |    |    |
  |    |    |-- cluster/        # Package che fornisce metodi per condividere e ricevere info
  |    |    |-- crypto/         # Package per criptare/decriptare/codificare/decodificare stringhe e files
  |    |    |-- exceptions/     # Eventuali eccezioni personalizzate
  |    |    |-- helpers/        # Package contenente helpers generici usati in più parti del programma
  |    |    |-- history/        # Package che fornisce classi e funzioni per salvare cronologie di vario tipo
  |    |    |-- html/           # Package che fornisce metodi per fare il parsing di un html
  |    |    |-- requests/       # Package che fornisce metodi per effettuare richieste (anche multiple)
  |    |    |-- settings/       # Package dedito al settaggio di parametri globali (es. IP gaming server, ...)
  |    |    |-- sniffing/       # Package che fornisce metodi per sniffing in una rete
  |    |    |-- sql/            # Package che fornisce metodi per sql injection
  |    |
  |    |-- env.py          # Variabili d'ambiente
  |
  |-- main.py   # Eseguibile principale
  |-- test.py   # Eseguibile di testing
```


### Useful commands:
 - Update dependencies: `pip3 freeze > requirements.txt`


### Authors:
 -  [Fabrizio Fubelli](https://fabrizio.fubelli.org)
 

### Thanks to:
 - [PyShark](https://github.com/KimiNewt/pyshark)
 - [Sqlmap](https://github.com/sqlmapproject/sqlmap)
