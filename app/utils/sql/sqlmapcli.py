"""
*********************************************************************************
*                                                                               *
* sqlmapcli.py -- sqlmap client.                                                *
*                                                                               *
* Class to interface with the sqlmap local server.                              *
*                                                                               *
* sqlmap repository:                                                            *
* https://github.com/sqlmapproject/sqlmap                                       *
*                                                                               *
* sqlmap license:                                                               *
* https://raw.githubusercontent.com/sqlmapproject/sqlmap/master/LICENSE         *
*                                                                               *
********************** IMPORTANT BLACK-WIDOW LICENSE TERMS **********************
*                                                                               *
* This file is part of black-widow.                                             *
*                                                                               *
* black-widow is free software: you can redistribute it and/or modify           *
* it under the terms of the GNU General Public License as published by          *
* the Free Software Foundation, either version 3 of the License, or             *
* (at your option) any later version.                                           *
*                                                                               *
* black-widow is distributed in the hope that it will be useful,                *
* but WITHOUT ANY WARRANTY; without even the implied warranty of                *
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                 *
* GNU General Public License for more details.                                  *
*                                                                               *
* You should have received a copy of the GNU General Public License             *
* along with black-widow.  If not, see <http://www.gnu.org/licenses/>.          *
*                                                                               *
*********************************************************************************
"""

from pprint import pprint
from sqlmap.lib.utils.api import server as sqlmap_server

from app.utils.helpers.logger import Log
from app.utils.helpers.multitask import multithread


class SqlmapClient:
    _client = None

    def __init__(self, host='0.0.0.0', port=8775):
        self.host = host
        self.port = port
        # Start the sqlmap-api server in a parallel thread
        Log.info("Starting sqlmap-api server in a parallel thread")
        multithread(sqlmap_server, (self.host, self.port), True, 1)
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
        pprint(forms)
        Log.info('Trying injection with cookies: '+str(cookies))
        Log.error("try_inject: Not Implemented")
        # TODO: Use sqlmap-api server to inject all forms
