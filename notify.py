#!/usr/bin/python3
# -*- python -*-
# coding: utf-8

from email.mime.text import MIMEText
import smtplib

import constants

EMAIL_API_KEY = open(f"{constants.PATH}/sendgrid.key", "r").read()


def notify(new_jobs, logger):
    to_addr = "dbraden@gmail.com"
    from_addr = to_addr
    subject = "New Engineering Position(s)"
    body = compose(new_jobs)

    message = MIMEText(body, "html")
    message["Subject"] = subject
    message["From"] = from_addr

    server = "smtp.sendgrid.net"
    port = 587
    username = "apikey"

    try:
        server = smtplib.SMTP(server, port)
        server.login(username, EMAIL_API_KEY)
        response = server.sendmail(from_addr, to_addr, message.as_string())
        logger.log(f"sendmail response: {response}")
    except Exception as e:
        logger.log("Unable to send: %s" % e)
    finally:
        server.quit()


def compose(new_jobs):
    body = f"<html><body><h1>New Engineering Positions Found</h1>"
    for company, jobs in new_jobs.items():
        jobs = "\n\n--\n\n".join(jobs)
        body += f"<h2>{company}</h2>\n\n{jobs}"
    body += "</body></html>"
    return body
