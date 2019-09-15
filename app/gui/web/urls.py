"""
*********************************************************************************
*                                                                               *
* urls.py -- Web URL Configuration.                                             *
*                                                                               *
* The `urlpatterns` list routes URLs to views. For more information please see: *
*    https://docs.djangoproject.com/en/1.11/topics/http/urls/                   *
* Examples:                                                                     *
* Function views                                                                *
*   1. Add an import:  from my_app import views                                 *
*   2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')           *
* Class-based views                                                             *
*   1. Add an import:  from other_app.views import Home                         *
*   2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')       *
* Including another URLconf                                                     *
*   1. Import the include() function: from django.conf.urls import url, include *
*   2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))          *
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

import re

# from django.conf.urls import url
# from django.contrib import admin
from django.urls import include, path
from django.urls import re_path
from django.views.static import serve

from app.gui.web.wsgi import WEB_PACKAGE
from app.gui.web.settings import STATIC_URL


urlpatterns = [
    path('', include(WEB_PACKAGE + '.black_widow.urls')),
    # url(r'^admin/', admin.site.urls),
]

# urlpatterns += staticfiles_urlpatterns()
