from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user', views.user, name='user'),
    path('tables', views.tables, name='tables'),
    path('typography', views.typography, name='typography'),
    path('icons', views.icons, name='icons'),
    path('notifications', views.notifications, name='notifications'),
]
