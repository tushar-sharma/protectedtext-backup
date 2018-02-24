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
import argparse

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
    with open(backup_file, "w") as f:
        f.write(data)
        logging.debug("Wrote: " + site)

"""
create directories if not exist
"""
def setup(path):
    if not os.path.exists(path):
        os.makedirs(path)

"""
Parse the sites url to parse
"""
def get_args():
    parser = argparse.ArgumentParser(description='Protectedtext.com backup')

    parser.add_argument('--nargs', nargs='+', help="Sites name to save")

    for _,  value in parser.parse_args()._get_kwargs():
        if value is not None:
            return value

def main():
    PATH = os.getcwd()
    log_path = PATH + '/logs/'
    backup_path = PATH + "/backup/"
    log_file = log_path + 'events.log'

    # create required directories
    setup(log_path)
    setup(backup_path)

    sites = get_args()


    logging.basicConfig(filename=log_path + 'events.log',
                    level = logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s')

    sys.excepthook = log_except_hook

    logging.debug("Start")

    if sites:

        for site in sites:
            backup_file = backup_path + site
            content = get_content(site)

            if not content:
                logging.debug("There is no secret "  + site )
                sys.exit(1)

            save_file(content, site, backup_file)
    else:
        logging.debug("No sites to save ")
        sys.exit(1)

if __name__=="__main__":
    main()
