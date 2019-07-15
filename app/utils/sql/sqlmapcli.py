from sqlmap import sqlmapapi
from pprint import pprint

from app.utils.helpers.logger import Log
from app.utils.helpers.multitask import multithread


class SqlmapClient:
    _client = None

    def __init__(self, host='0.0.0.0', port=8775):
        self.host = host
        self.port = port
        # Start the sqlmap-api server in a parallel thread
        Log.info("Starting sqlmap-api server")
        # noinspection PyUnresolvedReferences
        multithread(sqlmapapi.server, (self.host, self.port), True, 1)
        Log.success("Sqlmap-api server started!")

    @staticmethod
    def try_inject(forms, cookies=''):
        """
        Try injection in all provided forms
        :param forms: dict A dictionary of { "<url>": [ <parsed_form_1>, <parsed_form_2>, ... ], ... }
        :param cookies: str the request cookies
        """
        if SqlmapClient._client is None:
            SqlmapClient._client = SqlmapClient()
        Log.info('Trying injection with cookies: '+str(cookies))
        Log.error("try_inject: Not Implemented")
        pprint(forms)
        # TODO: Use sqlmap-api server to inject all forms
