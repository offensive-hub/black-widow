#!/bin/sh

if [ "$1" = '-g' ] || [ "$1" = '--gui' ];then
    cd app/gui
    gunicorn -b :80 web.wsgi:application
else
    ./black-widow.py $@
fi
