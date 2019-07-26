#!/bin/sh

cd app/gui
gunicorn web.wsgi 127.0.0.1:80
