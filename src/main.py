#!/usr/bin/python3
#  Decription
#  -----------
#  * Backup secrets from www.protectedtext.com to local storage
#  * Decryption: `base64 -d BACKUP_FILE | openssl aes-256-cbc -d -k PASSWORD`

import urllib.request
import json
import os
import shutil
import datetime
import logging
import sys

def log_except_hook(*exc_info):
    exc = "".join(tracebook.format_exception(*exc_info))
    logging.critical(exc)
    failure(exc)

"""
Get encrypted data from protectedtext.com
"""
def get_content(site):
    req = urllib.request.urlopen("https://www.protectedtext.com/%s?action=getJSON" % site)
    return json.loads(req.read().decode("utf-8"))['eContent']

"""
Save data to disk
"""
def save_file(data, site, backup_file):
    with open(secret_file, "w") as f:
        f.write(data)
        logging.debug("Wrote: " + site)

"""
create directories if not exist
"""
def setup():
    if not os.path.exists(PATH):
        os.makedirs(PATH)

def main():
    PATH = os.getcwd()
    log_path = PATH + '/logs/'
    backup_path = PATH + "/backup/"
    log_file = log_path + 'events.log'

    sys.excepthook = log_except_hook
    logging.debug("Start")

    sites = ["golmal"]

    logging.basicConfig(filename=log_path + 'events.log',
                    level = logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')


    setup(log_path)
    setup(lbackup_path)

    for site in sites:
        backup_file = backup_path + site
        content = get_content(site)

        if not content:
            logging.debug("There is no secret "  + site )
            sys.exit(1)

        save_file(content, site, backup_file)


if __name__=="__main__":
    main()
