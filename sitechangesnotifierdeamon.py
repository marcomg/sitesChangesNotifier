#!/usr/bin/python3

#
#    Copyright (C) 2017 marcomg
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#   


import argparse
import csv
import requests
import time
import smtplib
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

def check(name, url):
    with open(config['paths']['sites'] + name + '.txt', 'r') as f:
        oldata = f.read()
        web = requests.Session()
        data = web.get(url).text
        if data == oldata:
            print('Site %s not changed' % (name))
            return
        else:
            print('Site %s changed' % (name))
            f.close()
            with open(config['paths']['sites'] + name + '.txt', 'w') as f:
                f.writelines(data)
                f.close()
                notify(name)
                return

def notify(name):
    server = smtplib.SMTP_SSL(config['smtp']['server'], config['smtp']['port'])
    server.ehlo()
    server.login(config['smtp']['login'], config['smtp']['password'])
    msg = {}
    msg['subject'] = ((config['email']['subject']) % (name))
    msg['from'] = config['email']['from']
    msg['to'] = config['email']['to']
    msg['body'] = (('From: %s\r\nSubject: %s\r\nTo: %s\r\n\r\n' + config['email']['body']) % (msg['from'], msg['subject'], msg['to']))
    server.sendmail(msg=msg['body'], from_addr=msg['from'], to_addrs=msg['to'])
    server.close()
    
    return

argParse = argparse.ArgumentParser(description='sitechangesnotification deamon', prog='a deamon to notify changes')
argParse.add_argument('-v', '--version', action='version', version='%(prog)s version 1.0')
#argParse.add_argument('-vv', '--verbose', action='store_true', help='select if print or not')
args = argParse.parse_args()

# load database
try:
    db = open(config['paths']['db'], 'r+')
except PermissionError:
    print('If you have opened config file please close it')
    
lines = csv.reader(db, dialect='unix')
rdb = []
for line in lines:
    app = []
    app.append(line[0])
    app.append(int(line[1]))
    app.append(line[2])
    app.append(0)
    rdb.append(app)
db.close()
del lines
del line
del app


#entering in deamon mode
while True:
    nowtime = int(time.time())
    for line in rdb:
        #             last check interval
        if (nowtime - line[3]) > line[1]:
            check(line[0], line[2])
            line[3] = nowtime
    time.sleep(60)