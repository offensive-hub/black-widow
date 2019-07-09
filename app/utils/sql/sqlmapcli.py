from sqlmap import sqlmapapi

from app.utils.helpers.logger import Log
from app.utils.helpers.multitask import multithread


class SqlmapClient:
    _client = None

    def __init__(self, host='127.0.0.1', port=8775):
        self.host = host
        self.port = port
        # Start the sqlmap-api server in a parallel thread
        Log.info("Starting sqlmap-api server")
        # noinspection PyUnresolvedReferences
        multithread(sqlmapapi.server, (self.host, self.port), True, 1)
        Log.success("Sqlmap-api server started!")

    @staticmethod
    def try_inject(forms):
        """
        Try injection in all provided forms
        :param forms: dict A dictionary of { "<url>": [ <parsed_form_1>, <parsed_form_2>, ... ], ... }
        """
        print(forms)
        if SqlmapClient._client is None:
            SqlmapClient._client = SqlmapClient()

        Log.error("try_inject: Not Implemented")
