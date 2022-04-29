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

### ![](https://raw.githubusercontent.com/offensive-hub/black-widow/master/resources/logos/tux.png)   APT installation (ubutu/debian)

    sudo add-apt-repository ppa:offensive-hub/black-widow
    sudo apt-get update
    sudo apt-get install black-widow

### ![](https://raw.githubusercontent.com/offensive-hub/black-widow/master/resources/logos/tux.png)   APT installation (other distro)

 1) Put the following text on `/etc/apt/sources.list.d/black-widow.list` file:
    ```text
    deb http://ppa.launchpad.net/offensive-hub/black-widow/ubuntu focal main 
    deb-src http://ppa.launchpad.net/offensive-hub/black-widow/ubuntu focal main 
    ```
 2) Execute the following commands:
    ```text
    sudo sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 5D26C76613E84EA9
    sudo apt-get update
    sudo apt-get install black-widow
    ```

### ![](https://raw.githubusercontent.com/offensive-hub/black-widow/master/resources/logos/pypi.png)   PyPI installation
```shell
sudo pip3 install black-widow
```

### ![](https://raw.githubusercontent.com/offensive-hub/black-widow/master/resources/logos/docker-hub.png)   Docker installation
If you haven't Docker, [install it](https://docs.docker.com/install/linux/docker-ce/ubuntu)
  * GUI: `docker run -d -p 8095:80 offensive/black-widow -g`
    * Than visit: [http://localhost:8095](http://localhost:8095/)
  * Command line: `docker run --rm offensive/black-widow <arguments>`

### Manual installation

 1) `sudo apt-get update && sudo apt-get install tidy clang tshark`
 2) `mkdir black-widow`
 3) `cd black-widow`
 4) `touch black-widow.py && chmod +x black-widow.py`
 5) Copy and paste the following code in file `black-widow.py`:
    ```python
    #!/usr/bin/env python3
    
    from black_widow.black_widow import main
    
    if __name__ == "__main__":
        main()
    
    ```
 6) `git clone git@github.com:offensive-hub/black-widow.git black_widow`
 7) `sudo pip3 install -U -r black_widow/requirements.txt`
 8) `./black-widow.py --django migrate black_widow`
 9) Now you can run **black-widow** with: `./black-widow.py <arguments>`

### Run

* **GUI:** `black-widow -g`
* **Command line:** `black-widow <arguments>`

### Debug

* Run django \(examples\):
  * `black-widow --django runserver`
  * `black-widow --django help`
  * `black-widow --django "help createsuperuser"`

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

* Homepage: [https://black-widow.it](https://black-widow.it)
* PyPI: [https://pypi.org/project/black-widow](https://pypi.org/project/black-widow/)
* GitHub: [https://github.com/offensive-hub/black-widow](https://github.com/offensive-hub/black-widow)
* Docker Registry: [https://hub.docker.com/r/offensive/black-widow](https://hub.docker.com/r/offensive/black-widow)
* PPA: [Launchpad.net](https://launchpad.net/~offensive-hub/+archive/ubuntu/black-widow)
* Free Software Directory: [https://directory.fsf.org/wiki/Black-widow](https://directory.fsf.org/wiki/black-widow)

### Contacts

* [fabrizio@fubelli.org](mailto:fabrizio@fubelli.org)

### Authors

* [Fabrizio Fubelli](https://fabrizio.fubelli.org)

### Thanks to

* [PyShark](https://github.com/KimiNewt/pyshark)
* [Sqlmap](https://github.com/sqlmapproject/sqlmap)
* [Material Dashboard](https://github.com/creativetimofficial/material-dashboard)

### Follow Us

  [![Facebook](https://raw.githubusercontent.com/offensive-hub/black-widow/master/resources/social/facebook-icon.png)](https://www.facebook.com/OffensiveHub/)   [![Instagram](https://raw.githubusercontent.com/offensive-hub/black-widow/master/resources/social/instagram-icon.png)](https://www.instagram.com/0ffens1ve_hub/)   [![Twitter](https://raw.githubusercontent.com/offensive-hub/black-widow/master/resources/social/twitter-icon.png)](https://twitter.com/Offensive_Hub)

# SPONSORS

### 1st level Sponsors

  [![Offensive Hub](https://avatars3.githubusercontent.com/u/35137101?s=140)](https://offensivehub.org)

#### 2nd level Sponsors

  [![Offensive Hub](https://avatars3.githubusercontent.com/u/35137101?s=70)](https://offensivehub.org)

##### 3th level Sponsors

  [![Offensive Hub](https://avatars3.githubusercontent.com/u/35137101?s=35)](https://offensivehub.org)
