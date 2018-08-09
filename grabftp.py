#! /usr/bin/python

""" Download a file from an FTP server at a semi-random interval.
Save to /dev/null. """


import urllib2
import time
import random
import shutil
import os
from getpass import getpass
from contextlib import closing

#Function to download file from FTP server; saves to /dev/null
def download(address, user=None, passwd=None):
    """ Choose a random file from the list provided and attempt to
        download from FTP server. """
    file_list = ['126M.mp4', '474M.wmv', '50M.mp4', '8M.mp4']
    chosen = file_list[random.randrange(0, 3)]
    url = 'ftp://%s:%s@%s/%s' % (user, passwd, address, chosen)
    print "Downloading %s from %s" % (chosen, url)
    with closing(urllib2.urlopen(url)) as source:
        with open(os.devnull, 'wb') as filename:
            shutil.copyfileobj(source, filename)
    print "Download Finished"

if __name__ == '__main__':
    ADDRESS = ""
    USER = ""
    PASSWD = getpass()


    while True:
        download(ADDRESS, USER, PASSWD)
        INTERVAL = 900 + random.randrange(3600)
        print "Waiting for %s" % INTERVAL
        time.sleep(INTERVAL)
