"""
*********************************************************************************
*                                                                               *
* web_parsing_model.py -- A web parsing job info model                          *
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

from django.db import models

from black_widow.app.gui.web.black_widow.models.abstract_job_model import AbstractJobModel
from black_widow.app.managers.parser import HtmlParser


class WebParsingJobModel(AbstractJobModel):
    """
    Django Web Parsing Job Model
    """
    TYPE_SINGLE_PAGE = 'single_page'
    TYPE_WEBSITE_CRAWLING = 'website_crawling'
    TYPES = (
        (TYPE_SINGLE_PAGE, 'Single Page'),
        (TYPE_WEBSITE_CRAWLING, 'Website Crawling')
    )

    PARSE_TAGS = (
        (HtmlParser.TYPE_ALL, 'All Tags'),
        (HtmlParser.TYPE_RELEVANT, 'Relevant Tags (a, script, link, Form Tags, Meta Tags)'),
        (HtmlParser.TYPE_FORM, 'Form Tags (form, input, textarea, select, option)'),
        (HtmlParser.TYPE_META, 'Meta Tags (meta, xmp)')
    )

    url: str = models.CharField(null=False, max_length=512)
    _parsing_type: str = models.CharField(
        null=False,
        choices=TYPES,
        max_length=50
    )
    _parsing_tags: str = models.CharField(
        null=False,
        choices=PARSE_TAGS,
        max_length=50
    )
    depth: int = models.IntegerField(null=False)
    cookies: str = models.TextField(null=True)

    @staticmethod
    def all() -> models.query.QuerySet:
        return AbstractJobModel._all(WebParsingJobModel)

    def parsing_type_key(self):
        return self._parsing_type

    @property
    def parsing_type(self):
        return dict(WebParsingJobModel.TYPES).get(self._parsing_type)

    @parsing_type.setter
    def parsing_type(self, value: str):
        self._parsing_type = value

    def parsing_tags_key(self):
        return self._parsing_tags

    @property
    def parsing_tags(self):
        return dict(WebParsingJobModel.PARSE_TAGS).get(self._parsing_tags)

    @parsing_tags.setter
    def parsing_tags(self, value: str):
        self._parsing_tags = value

    def __str__(self) -> str:
        return 'WebParsingJobModel(' + str({
            'id': self.id,
            'pid': self.pid,
            'pid_file': self.pid_file,
            'status': self.status_name,
            'type': self.parsing_type,
            'tags': self.parsing_tags,
            'depth': self.depth,
        }) + ')'
