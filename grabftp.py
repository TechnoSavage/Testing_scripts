#Download a file from an FTP server at a semi-random interval.  Save to /dev/null

#! /usr/bin/python

import urllib2, time, random, shutil
from getpass import getpass
from contextlib import closing

#Function to download file from FTP server; saves to /dev/null
def download(address, user=None, passwd=None):
    file_list = ['126M.mp4', '474M.wmv', '50M.mp4', '8M.mp4']
    chosen = file_list[random.randrange(0,3)]
    url = 'ftp://' + user + ':' + passwd + '@' + address + '/' + chosen
    print "Downloading %s from %s" % (chosen, url)
    with closing(urllib2.urlopen(url)) as r:
        with open(chosen, 'wb') as f:
            shutil.copyfilejob(r, f)

if __name__ == '__main__':
    address = '192.168.1.210'
    user = 'ftpuser'
    passwd = 'CirrusT3st8'


    while True:
        download(address, user, passwd)
        time.sleep(900 + random.randrange(3600))
