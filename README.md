# Black Widow

[![Python 3.x](https://img.shields.io/badge/python-3.x-yellow.svg)](https://www.python.org/) 
[![License](https://img.shields.io/badge/license-GPLv3-red.svg)](https://raw.githubusercontent.com/FabrizioFubelli/black-widow/master/LICENSE)
[![Docker Pulls](https://img.shields.io/docker/pulls/offensive/black-widow.svg)](https://hub.docker.com/r/offensive/black-widow)
<!--
[![Image Size](https://img.shields.io/microbadger/image-size/offensive/black-widow.svg)](https://hub.docker.com/r/offensive/black-widow)
-->

![image](https://raw.githubusercontent.com/FabrizioFubelli/black-widow/master/resources/black-widow-img.png)


## Offensive penetration testing tool (Open Source)

**black-widow** is one of the most useful, powerful and complete offensive penetration testing tool.

It provides easy ways to execute many kinds of information gatherings and attacks.

 - Fully Open Source
 - Written in Python
 - Continuously updated and extended

### Features:
 - Localhost Web GUI
 - Sniffing
 - Website crawling
 - Web page parsing
 - SQL injection
 - Injected database management
 - Brute force attacks
 - Cluster between other black-widows
 - Multiple asynchronous requests
 - Multiple targets management
 - Useful CTF features

### <img alt="DOCKER_IMAGE" src="https://docs.docker.com/favicons/docs@2x.ico" height="50px" title="Docker"/> Docker Installation:
1. If you haven't Docker, [install it](https://docs.docker.com/install/linux/docker-ce/ubuntu)
2. Run docker:
  - Command line: `docker run --rm offensive/black-widow [arguments]`
  - GUI: `docker run -d -p 8095:80 --rm offensive/black-widow -g`
      - Than visit: [http://localhost:8095](http://localhost:8095/)

### Default Installation:
1. `sudo apt-get update && sudo apt-get install tidy clang tshark`
2. `git clone git@github.com:FabrizioFubelli/black-widow.git`
3. `cd black-widow`
4. `sudo pip3 install -U -r requirements.txt`
5. `cp ./app/env_local_dist.py ./app/env_local.py`
6. `./black-widow.py --django migrate`
7. `sudo ./black-widow.py <arguments>`

### Run:
- **GUI:** `sudo ./black-widow.py -g`
- **Command line:** `sudo ./black-widow.py <arguments>`

### Debug:
- Run django (examples):
  - `./black-widow.py --django runserver`
  - `./black-widow.py --django help`
  - `./black-widow.py --django "help createsuperuser"`

<br/>

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
  |-- black-widow.py   # Eseguibile principale
  |-- test.py          # Eseguibile di testing
```

<br/>

### Links:
- Homepage: [https://black-widow.io](https://black-widow.io)
- GitHub: [https://github.com/offensive-hub/black-widow](https://github.com/offensive-hub/black-widow)
- Docker Registry: [https://hub.docker.com/r/offensive/black-widow](https://hub.docker.com/r/offensive/black-widow)
- Free Software Directory: [https://directory.fsf.org/wiki/Black-widow](https://directory.fsf.org/wiki/black-widow)

### Contacts:
 -  [offensive-hub@protonmail.com](mailto:offensive-hub@protonmail.com)

### Authors:
 -  [Fabrizio Fubelli](https://fabrizio.fubelli.org)

### Thanks to:
 - [PyShark](https://github.com/KimiNewt/pyshark)
 - [Sqlmap](https://github.com/sqlmapproject/sqlmap)
 - [Material Dashboard](https://github.com/creativetimofficial/material-dashboard)

### Follow Us:
&ensp;
<a href="https://www.facebook.com/offensive.black.widow" title="Facebook"><img title="Facebook" src="https://it.facebookbrand.com/wp-content/uploads/2019/04/f_logo_RGB-Hex-Blue_512.png" width="32"/></a>
&ensp;
<a href="https://www.instagram.com/8l4ck_w1d0w" title="Instagram"><img title="Instagram" src="https://instagram-brand.com/wp-content/uploads/2016/11/Instagram_AppIcon_Aug2017.png" width="32"/></a>
&ensp;
<a href="https://twitter.com/Offensive_Hub" title="Twitter"><img title="Twitter" src="https://upload.wikimedia.org/wikipedia/it/0/09/Twitter_bird_logo.png" width="32"/></a>
&ensp;
<a href="https://www.youtube.com/playlist?list=PLUrUcT-zI_BfkAagJ5eAgOW8TcVYY5gB6&fbclid=IwAR1hWrMt1vchrDTr8MbAyrOk3l2KZ09uogc8tl38D052w3F1bSk5HyVXn-8" title="YouTube"><img title="YouTube" src="https://developers.google.com/site-assets/logo-youtube.svg" width="32"/></a>
&ensp;
