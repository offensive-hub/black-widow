import hashlib
from base64 import b64decode, b64encode
from app.utils.requests import request, Type as RequestType
from app.utils.helpers.logger import Log

class md5:
    class Api:
        def url_1_result(json): return json.get('result')
        def url_2_result(json): return json[0].get('decrypted')
        url_1 = {'url':'https://md5.pinasthika.com/api/decrypt?value=', 'get_result': url_1_result}
        url_2 = {'url':'https://www.md5.ovh/index.php?result=json&md5=', 'get_result': url_2_result}
        def all(): return (md5.Api.url_1, md5.Api.url_2)

    @staticmethod
    def encrypt(string):
        m = hashlib.md5()
        m.update(string.encode())
        return str(m.hexdigest())

    @staticmethod
    def decrypt(string):
        for api in md5.Api.all():
            r = request(api['url']+string, RequestType.GET)
            if (r == None): continue
            try:
                r_json = r.json()
            except json.decoder.JSONDecodeError:
                return None
            result = api['get_result'](r_json)
            if (result != None): return result
        Log.error('md5: unable to decrypt: '+str(string))
        return None

class base64:
    @staticmethod
    def encrypt(string):
        return b64encode(bytes(string, encoding='utf-8')).decode('utf-8')

    @staticmethod
    def decrypt(string):
        return b64decode(string).decode('utf-8')
