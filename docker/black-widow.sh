#!/bin/sh

if [ "$1" = '-g' ] || [ "$1" = '--gui' ];then
    cd black_widow/app/gui || exit 1
    gunicorn -b :80 web.wsgi:application
else
    ./black-widow.py "$@"
fi
