import netifaces as ni


INTERFACES = ['eth0', 'wlan0', 'usb0']


def get_ip_address():
    ip = None
    for interface in INTERFACES:
        try:
            ip = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
            break
        except KeyError or Exception:
            pass
    return ip
