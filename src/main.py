#!/usr/bin/python3

import urllib.request
import json
import os
import shutil
import datetime
import logging
import sys

PATH = os.getcwd()
log_file = PATH + '/logs/events.log'
backup_file = PATH + "/backup/"

logging.basicConfig(filename=log_file,
                    level = logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

def log_except_hook(*exc_info):
    exc = "".join(tracebook.format_exception(*exc_info))
    logging.critical(exc)
    failure(exc)

sys.excepthook = log_except_hook
logging.debug("Start")

sites = ["golmal"]

def get_content(site):
    req = urllib.request.urlopen("https://www.protectedtext.com/%s?action=getJSON" % site)
    return json.loads(req.read().decode("utf-8"))['eContent']

def save_file(data, site):
    secret_file = PATH + "/backup/" + site
    with open(secret_file, "w") as f:
        f.write(data)
        logging.debug("Wrote: " + site)

def main():

    for site in sites:
        content = get_content(site)

        if not content:
            logging.debug("There is no secret "  + site )
            sys.exit(2)

        save_file(content, site)


if __name__=="__main__":
    main()
