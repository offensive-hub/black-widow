# Black Widow

[![Python 3.x](https://img.shields.io/badge/python-3.x-yellow.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/license-GPLv3-red.svg)](https://raw.githubusercontent.com/FabrizioFubelli/black-widow/master/LICENSE) [![Image Size](https://img.shields.io/microbadger/image-size/offensive/black-widow.svg)](https://hub.docker.com/r/offensive/black-widow)

![image](https://raw.githubusercontent.com/FabrizioFubelli/black-widow/master/resources/black-widow-img.png)


## Offensive penetration testing tool (Open Source)


> ### Features:
>  - Sniffing
>  - SQL Injection
>  - Injected-database management
>  - Web page parser
>  - Website crawler
>  - Multiple targets management
>  - Mapping **{server -> vulnerabilities}**
>  - Cluster between **black-widow** that are running inside the same network
>  - Encrypted communications between other **black-widows**
>  - Useful features for **CTF** challenges
> 
> ##### Suggest you other features!

<br/>

> ### Links:
> - Homepage: [https://black-widow.io](https://black-widow.io)
> - GitHub: [https://github.com/FabrizioFubelli/black-widow](https://github.com/FabrizioFubelli/black-widow)

<br/>

> <img src="https://docs.docker.com/favicons/docs@2x.ico" height="50px" title="Docker"/>
> 
> ### Docker Installation:
> 1. If you haven't Docker, [install it](https://docs.docker.com/install/linux/docker-ce/ubuntu)
> 2. Run docker:
>   - Command line: `docker run --rm offensive/black-widow [arguments]`
>   - GUI: `docker run -d -p 8095:80 --rm offensive/black-widow -g`
>
> ### Docker Registry:
> [https://hub.docker.com/r/offensive/black-widow](https://hub.docker.com/r/offensive/black-widow)

<br/>

> ### Default Installation:
> 1. `sudo apt-get update && sudo apt-get install tidy`
> 2. `git clone git@github.com:FabrizioFubelli/black-widow.git`
> 3. `cd black-widow`
> 4. `sudo pip3 install -U -r requirements.txt`
> 5. `cp ./app/env_local_dist.py ./app/env_local.py`
> 6. `sudo ./black-widow.py <arguments>`

<br/>

> ### Debug:
> - Run django (examples):
>   - `./black-widow.py --django runserver`
>   - `./black-widow.py --django help`
>   - `./black-widow.py --django "help createsuperuser"`

<br/>

> ### Directories:
> ```
> [root]
>   |
>   |-- app/      # Package principale dell'applicazione
>   |    |
>   |    |-- attack/         # Package per modalità di attacco
>   |    |-- defense/        # Package per modalità di difesa
>   |    |
>   |    |-- gui/            # Package per la grafica dell'applicazione
>   |    |
>   |    |-- storage/        # Package per salvare i files (settings, output, ...)
>   |    |
>   |    |-- utils/
>   |    |    |
>   |    |    |-- cluster/        # Package che fornisce metodi per condividere e ricevere info
>   |    |    |-- crypto/         # Package per criptare/decriptare/codificare/decodificare stringhe e files
>   |    |    |-- exceptions/     # Eventuali eccezioni personalizzate
>   |    |    |-- helpers/        # Package contenente helpers generici usati in più parti del programma
>   |    |    |-- history/        # Package che fornisce classi e funzioni per salvare cronologie di vario tipo
>   |    |    |-- html/           # Package che fornisce metodi per fare il parsing di un html
>   |    |    |-- requests/       # Package che fornisce metodi per effettuare richieste (anche multiple)
>   |    |    |-- settings/       # Package dedito al settaggio di parametri globali (es. IP gaming server, ...)
>   |    |    |-- sniffing/       # Package che fornisce metodi per sniffing in una rete
>   |    |    |-- sql/            # Package che fornisce metodi per sql injection
>   |    |
>   |    |-- env.py          # Variabili d'ambiente
>   |
>   |-- main.py   # Eseguibile principale
>   |-- test.py   # Eseguibile di testing
> ```

<br/>

> ### Authors:
>  -  [Fabrizio Fubelli](https://fabrizio.fubelli.org)

<br/>

> ### Thanks to:
>  - [PyShark](https://github.com/KimiNewt/pyshark)
>  - [Sqlmap](https://github.com/sqlmapproject/sqlmap)
