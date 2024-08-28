#!/usr/bin/python3
# -*- python -*-
# coding: utf-8

import datetime

PATH = "/Users/drew/app/jobs/"
LOGFILE = f"{PATH}/log.txt"


class Logger:
    def __init__(self):
        self.fh = open(LOGFILE, "a")

    def log(self, msg):
        timed = "%s - %s" % (datetime.datetime.utcnow(), msg)
        self.fh.write(timed)
        print(timed)

    def close(self):
        self.fh.close()
