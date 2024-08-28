#!/usr/bin/python3
# -*- python -*-
# coding: utf-8

import argparse
import collections
import sqlite3

import constants
from companies import Honor, Inmar, Mayo, Veeva
from log import Logger
from notify import notify

DBNAME = f"{constants.PATH}/jobs.db"
ACTIVE_COMPANIES = [Honor, Inmar, Mayo, Veeva]

logger = Logger()


def run(conn, include_all=False, only_company=None):
    to_notify = collections.defaultdict(list)
    for company in ACTIVE_COMPANIES:
        if only_company and company.NAME != only_company:
            continue

        obj = company(conn, logger)
        new_jobs = obj.pull(include_all)
        if new_jobs:
            logger.log("Found new jobs:\n")
            for job in new_jobs:
                logger.log(obj.summarize(job))
                to_notify[company.NAME].append(obj.summarize(job))

    if to_notify:
        notify(to_notify, logger)

    conn.commit()
    logger.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-all", type=bool)
    parser.add_argument("-company", type=str)

    args = parser.parse_args()
    conn = sqlite3.connect(DBNAME)
    run(conn, args.all, args.company)
