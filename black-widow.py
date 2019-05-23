#!/usr/bin/env python3

import os, app
from app.utils.helpers.logger import Log

def usage():
    pass

def main():
    Log.info(app.env.APP_NAME+' started, PID='+str(os.getpid()))

main()
