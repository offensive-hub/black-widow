---
description: >-
  black-widow is one of the most useful, powerful and complete offensive
  penetration testing tool
---

# black-widow

[![Python 3.x](https://img.shields.io/badge/python-3.x-yellow.svg)](https://www.python.org/) [![License](https://img.shields.io/badge/license-GPLv3-red.svg)](https://raw.githubusercontent.com/FabrizioFubelli/black-widow/master/LICENSE) [![Docker Pulls](https://img.shields.io/docker/pulls/offensive/black-widow.svg)](https://hub.docker.com/r/offensive/black-widow)

![](https://raw.githubusercontent.com/offensive-hub/black-widow/master/resources/black-widow.jpg)

## Offensive penetration testing tool \(Open Source\)

black-widow provides easy ways to execute many kinds of information gatherings and attacks.

* Fully Open Source
* Written in Python
* Continuously updated and extended

### Features

* [x] Localhost Web GUI
* [x] Sniffing
* [x] Website crawling
* [x] Web page parsing
* [ ] SQL injection
* [ ] Injected database management
* [ ] Brute force attacks
* [ ] Cluster between other black-widows
* [ ] Multiple asynchronous requests
* [ ] Multiple targets management
* [ ] Useful CTF features

### ![](https://raw.githubusercontent.com/offensive-hub/black-widow/master/resources/logos/pypi.png)   PyPI installation

    sudo pip3 install black-widow

### ![](https://raw.githubusercontent.com/offensive-hub/black-widow/master/resources/logos/docker-hub.png)   Docker installation

1. If you haven't Docker, [install it](https://docs.docker.com/install/linux/docker-ce/ubuntu)
2. Run docker:
   * Command line: `docker run --rm offensive/black-widow [arguments]`
   * GUI: `docker run -d -p 8095:80 --rm offensive/black-widow -g`
     * Than visit: [http://localhost:8095](http://localhost:8095/)

### Manual installation

1. `sudo apt-get update && sudo apt-get install tidy clang tshark`
2. `git clone git@github.com:offensive-hub/black-widow.git`
3. `cd black-widow`
4. `sudo pip3 install -U -r requirements.txt`
5. `./black-widow.py --django migrate`
6. `sudo ./black-widow.py <arguments>`

### Run

* **GUI:** `sudo ./black-widow.py -g`
* **Command line:** `sudo ./black-widow.py <arguments>`

### Debug

* Run django \(examples\):
  * `./black-widow.py --django runserver`
  * `./black-widow.py --django help`
  * `./black-widow.py --django "help createsuperuser"`

### Project layout

```text
[root]
  |
  |-- app/              # Main application package
  |    |
  |    |-- arguments/       # User input arguments parser (100%)
  |    |
  |    |-- attack/          # Attack modality package (0%)
  |    |-- defense/         # Defense modality package (0%)
  |    |
  |    |-- gui/             # Graphical User Interface package (100%)
  |    |
  |    |-- helpers/         # Helper methods package (100%)
  |    |
  |    |-- managers/        # Managers package
  |    |    |
  |    |    |-- cluster/        # Cluster managers package (0%)
  |    |    |-- crypto/         # Encryption managers package (70%)
  |    |    |-- injection/      # Injection managers package (60%)
  |    |    |-- parser/         # Parser managers package (100%)
  |    |    |-- request/        # Request managers package (70%)
  |    |    |-- sniffer/        # Sniffer managers package (95%)
  |    |
  |    |-- services/        # Services package
  |    |    |
  |    |    |-- logger.py       # Logger service (100%)
  |    |    |-- multitask.py    # MultiTask service (100%)
  |    |    |-- serializer.py   # PickleSerializer and JsonSerializer serivces (100%)
  |    |
  |    |-- storage/         # Storage directory
  |    |
  |    |-- env.py           # Environment variables management
  |
  |-- .env              # Environment variables
  |
  |-- black-widow.py    # Main executable
```

### Links

* Homepage: [https://black-widow.io](https://black-widow.io)
* GitHub: [https://github.com/offensive-hub/black-widow](https://github.com/offensive-hub/black-widow)
* Docker Registry: [https://hub.docker.com/r/offensive/black-widow](https://hub.docker.com/r/offensive/black-widow)
* Free Software Directory: [https://directory.fsf.org/wiki/Black-widow](https://directory.fsf.org/wiki/black-widow)

### Contacts

* [offensive-hub@protonmail.com](mailto:offensive-hub@protonmail.com)

### Authors

* [Fabrizio Fubelli](https://fabrizio.fubelli.org)

### Thanks to

* [PyShark](https://github.com/KimiNewt/pyshark)
* [Sqlmap](https://github.com/sqlmapproject/sqlmap)
* [Material Dashboard](https://github.com/creativetimofficial/material-dashboard)

### Follow Us

  [![Facebook](https://raw.githubusercontent.com/offensive-hub/black-widow/master/resources/social/facebook-icon.png)](https://www.facebook.com/offensive.black.widow)   [![Instagram](https://raw.githubusercontent.com/offensive-hub/black-widow/master/resources/social/instagram-icon.png)](https://www.instagram.com/8l4ck_w1d0w)   [![Twitter](https://raw.githubusercontent.com/offensive-hub/black-widow/master/resources/social/twitter-icon.png)](https://twitter.com/Offensive_Hub)   [![YouTube](https://raw.githubusercontent.com/offensive-hub/black-widow/master/resources/social/youtube-icon.png)](https://www.youtube.com/playlist?list=PLUrUcT-zI_BfkAagJ5eAgOW8TcVYY5gB6&fbclid=IwAR1hWrMt1vchrDTr8MbAyrOk3l2KZ09uogc8tl38D052w3F1bSk5HyVXn-8)

> # 1st level Sponsors
>
>  [![Offensive Hub](https://avatars3.githubusercontent.com/u/35137101?s=300)](https://offensivehub.org)

> ## 2nd level Sponsors
>
>   [![Offensive Hub](https://avatars3.githubusercontent.com/u/35137101?s=125)](https://offensivehub.org)

> ### 3th level Sponsors
>
>   [![Offensive Hub](https://avatars3.githubusercontent.com/u/35137101?s=35)](https://offensivehub.org)
