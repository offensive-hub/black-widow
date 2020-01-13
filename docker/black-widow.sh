#!/bin/sh

gui=false

while [ $# -ne 0 ]
do
    case "$1" in
        -g)
            gui=true
            ;;
        --gui)
            gui=true
            ;;
    esac
    shift
done

# Executes migrations
./black-widow.py --django migrate

if ( "${gui}" );then
    cd black_widow/app/gui || exit 1
    gunicorn -b :80 web.wsgi:application
else
    ./black-widow.py "$@"
fi
