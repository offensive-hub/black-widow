import hashlib
from base64 import b64decode, b64encode
from app.utils.requests import request, Type as RequestType
from app.utils.helpers.logger import Log

class md5:
    api_url_1 = 'https://md5.pinasthika.com/api/decrypt?value='
    api_url_2 = 'https://www.md5.ovh/index.php?result=json&md5='

    @staticmethod
    def encrypt(string):
        m = hashlib.md5()
        m.update(string.encode())
        return str(m.hexdigest())

    @staticmethod
    def decrypt(string):
        def attempt(api_url):
            r = request(api_url+string, RequestType.GET)
            if (r == None): return None
            r_json = r.json()
            if (api_url == md5.api_url_1):
                return r_json.get('result')
            elif (api_url == md5.api_url_2):
                return r_json[0].get('decrypted')
            return None
        result = attempt(md5.api_url_1)
        if (result == None):
            Log.info('md5 decryption: 2nd attempt')
            result = attempt(md5.api_url_2)
        return result

class base64:
    @staticmethod
    def encode(string):
        return b64encode(string)

    @staticmethod
    def decode(string):
        return b64decode(string)
