README
======

What is siteChangesNotifier?
--------------
Let's strart from beginning: why i wrote this code?

Simply: I am a university student and I did not want to check every minute the sites of my teachers if they had published marks of exams.

So siteChangesNitifier is a python3 script developed to check if a website is changed. If the site is changed it will send you an email!

Ok, cool I want to use it
-------------------------
I am very happy if you want to use my script, but I have to warn you that this script works perfectly is the site is not dynamic, in fact some CMSs print comments in html source the date and hour where the page is downloaded or may require cookies.

My teachers uses only obsolete websites (like 1997) so I never had this problem. If you want to improve code you're welcome.

How install
-----------
What you need:
 * Python3

You have 2 scripts and 1 config file.

**config.ini**: is the configuration file (you will find *config.default.ini*, you have to rename it in *config.ini*) where set email options and where store data. For more informations directly read comments in that file. If you want to move the config file in another directory you have to open *sitechangesnotifier.py* and *sitechangesnotifierdeamon.py* and at line

    config.read('config.ini')
    
edit the path (may be useful an absolute path if you install the script in the system).

**sitechangesnotifier.py**: is the config editor

you can use in this way or (if you install it or configure path you can use in a simpler way but if you can do this you don't need instructions):

**Add a site**

    $ python3 sitechangesnotifier.py add sitename -i 5m -u http://stuff.site.org

All arguments that start with minus can be omitted (but the script will go in interactive mode and will ask for that informations). Sitename is the nick to "call" the site.

-i: you can choose how often check the site. You can write 80 and the site will be check (more or less) every 80 seconds or 80s, 80m (minutes) 80h (hours).

Why I said more or less? Because the deamon will cycle evey minutes so if you have too much sites to check or you put an intervel lower than 1 minute the interval may not be respected.

**Remove a site**

    $ python3 sitechangesnotifier.py del sitename

**Show sites**

    $ python3 sitechangesnotifier.py show all

**sitechangesnotifierdeamon.py**: is the deamon

After configurated with *sitechangesnotifier* you can load the deamon. It will check sites and if it has been changed it will send you an email.