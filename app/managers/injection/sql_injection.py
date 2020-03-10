"""
*********************************************************************************
*                                                                               *
* sql_injection.py -- Methods to try injection in forms.                        *
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
from time import sleep
from urllib.parse import urlparse

from black_widow.app.env import APP_STORAGE_OUT
from black_widow.app.managers.injection.sql_injection_util.sqlmaptask import SqlmapTask
from black_widow.app.managers.parser import HtmlParser
from black_widow.app.services import Log, JsonSerializer
from black_widow.app.helpers.util import now

from .sql_injection_util import SqlmapClient


class SqlInjection:
    """
    SqlInjection Manager
    """

    @staticmethod
    def inject(
            forms: bool,
            url: str = None,
            max_depth: int = None,
            listen: bool = False
    ) -> dict:
        """
        Try SQL injection
        :param forms: True if you want to search forms in provided url
        :param url: The url to inject, or the url to visit in search for forms
        :param max_depth: The max crawling depth (if forms is False, it is skipped)
        :param listen: True, if you want to show the results in the console, otherwise False
        :return: A dictionary of SqlmapTask
        """
        if not forms:
            # Inject directly the provided url
            task = SqlInjection.__inject_url(url)
            tasks = {
                task.id: task
            }
        else:
            tasks = SqlInjection.__inject_forms(url, max_depth)
        # Search forms inside the provided url
        if listen:
            SqlInjection.__listen_tasks(tasks)
        else:
            return tasks

    @staticmethod
    def __inject_url(url: str) -> SqlmapTask:
        return SqlmapClient.try_inject_url(url)

    @staticmethod
    def __inject_forms(url, max_depth) -> dict:
        """
        Search a form in the page returned by url.
        If it doesn't find a form, or the injection can't be done, it visit the website in search for other forms
        :param url: str The url to visit
        :param max_depth: int The max depth during the visit
        :return A dictionary of SQL injection tasks
        """

        base_url = urlparse(url).netloc
        parsed_forms = dict()
        out_file = APP_STORAGE_OUT + '/' + now() + '_DEEP_FORMS_' + base_url + '.json'

        def deep_inject_form(href, depth=0):
            # Check the domain
            if href in parsed_forms or \
                    urlparse(href).netloc != base_url or \
                    (max_depth is not None and depth > max_depth):
                return ''

            # Visit the current href
            parsed_relevant, request_cookies = HtmlParser.relevant_parse(href)

            # Find forms in page
            parsed_forms[href] = HtmlParser.find_forms(parsed_relevant, href)

            # Find adjacent links
            links = HtmlParser.find_links(parsed_relevant)

            if len(parsed_forms) % 10 == 0:
                Log.info('Writing result in ' + out_file + '...')
                JsonSerializer.set_dictionary(parsed_forms, out_file)

            # Visit adjacent links
            for link in links:
                # print('link: '+link)
                child_request_cookies = deep_inject_form(link, depth+1)
                if len(child_request_cookies) > len(request_cookies):
                    request_cookies = child_request_cookies

            return request_cookies

        cookies = deep_inject_form(url)
        Log.info('Writing result in ' + out_file + '...')
        JsonSerializer.set_dictionary(parsed_forms, out_file)
        Log.success('Result wrote in ' + out_file)
        Log.success('Website crawled! Found '+str(len(parsed_forms))+' pages')
        tasks = SqlmapClient.try_inject_forms(parsed_forms, cookies)
        return tasks

    @staticmethod
    def __listen_tasks(tasks: dict):
        while True:
            sleep(3)
            for task_id, task in tasks.items():
                SqlInjection.__print_task(task)

    @staticmethod
    def __print_task(task: SqlmapTask):
        scan_log = task.scan_log()
        scan_data = task.scan_data()
        print('')
        print('[SQL injection] Scan Log:')
        pprint(scan_log)
        print('')
        print('[SQL injection] Scan Data:')
        pprint(scan_data)
        print('')
