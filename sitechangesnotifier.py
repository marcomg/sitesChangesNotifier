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
import urllib.request
import os
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# csv: name, interval, url
try:
    db = open(config['paths']['db'], "r+")
except PermissionError:
    print("If you have opened config file please close it")
except FileNotFoundError:
    db = open(config['paths']['db'], "w+")


argParse = argparse.ArgumentParser(description='A program to notify if a website has changed', prog='Web changes notifier')
argParse.add_argument('command', action='store', type=str, help='add a site, del or show?')
argParse.add_argument('name', action='store', type=str, help='name of the job')
argParse.add_argument('-u', '--url', action='store', type=str, help='the url of the site (with protocol)')
argParse.add_argument('-i', '--interval', action='store', type=str, help='how often check urls? please input as 3600 or 3600s or 60m or 1h')
argParse.add_argument('-v', '--version', action='version', version='%(prog)s version 1.0')
args = argParse.parse_args()

if args.command == "add":
    lines = csv.reader(db, dialect='unix')

    for line in lines:
        try:
            if line[0] == args.name:
                print("Error, name %s already exists, please del it or create a new name" % (args.name))
                exit()
        except IndexError:
            pass
            
    if args.interval == None:
        args.interval = str(input("how often check urls? please input something as 3600 or 3600s or 60m or 1h: "))
        
    time = args.interval[-1]
    if str.isdigit(time):
        args.interval = str(int(float(args.interval)))
    elif time == "s":
        args.interval = str(int(float(args.interval[:-1]) * 1))
    elif time == "m":
        args.interval = str(int(float(args.interval[:-1]) * 60))
    elif time == "h":
        args.interval = str(int(float(args.interval[:-1]) * 3600))
    else:
        print("Error, time %s don't recognized, please write it correctly" % (args.interval))
        exit()
    if(int(args.interval) < 60):
        print("The delay is < than 60")
    if args.url == None:
        args.url = str(input("Please insert url (with also protocol): "))
        
    dbw = csv.writer(db, dialect='unix')
    dbw.writerow([args.name, args.interval, args.url])
    
    with open(config['paths']['sites'] + args.name + ".txt", "w") as html:
        web = urllib.request.urlopen(args.url)
        try:
            data = web.read().decode('utf-8')
        except UnicodeDecodeError:
            data = web.read().decode("Windows-1252")
        html.writelines(data)

elif args.command == "del":
    lines = csv.reader(db, dialect='unix')
    out = []
    try:
        fremove = False
        for line in lines:
            if line[0] != args.name:
                out.append(line)
            else:
                fremove = True
    except IndexError:
        pass
    db.close()
    db = open(config['paths']['db'], "w")

    dbw = csv.writer(db, dialect='unix')
    for line in out:
        dbw.writerow(line)
    db.close()
    if fremove:
        os.remove(config['paths']['sites'] + args.name + ".txt")
    print("Done")
    
elif args.command == "show":
    if args.name == "all":
        lines = csv.reader(db, dialect='unix')
        try:
            for line in lines:
                print("%10s    %8s    %25s" % (line[0], line[1], line[2]))
        except IndexError:
            print("Db is empty!!")
    else:
        print("Nothing to show, please use show all")
else:
    print("Input parsing error, please set add, del or show as first input arg")