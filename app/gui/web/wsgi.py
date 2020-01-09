"""
*********************************************************************************
*                                                                               *
* wgsi.py -- WSGI config for web project.                                       *
*                                                                               *
* It exposes the WSGI callable as a module-level variable named ``application`` *
*                                                                               *
* For more information on this file, see                                        *
* https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/                 *
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

import os
import sys

from os.path import dirname
from django.core.wsgi import get_wsgi_application


WEB_PACKAGE = 'black_widow.app.gui.web'

root_path = dirname(dirname(dirname(dirname(dirname(__file__)))))    # to access at "black_widow" package
sys.path.insert(0, root_path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", WEB_PACKAGE + ".settings")

application = get_wsgi_application()
