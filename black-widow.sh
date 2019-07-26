#!/bin/sh

if [ "$1" = '-g' ] || [ "$1" = '--gui' ];then
    cd app/gui
    gunicorn web.wsgi 127.0.0.1:80
    exit 0
fi

./black-widow.py $@
