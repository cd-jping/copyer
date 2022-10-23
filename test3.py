# ------menu.py - ---------
# !/usr/bin/evn python
# -*- coding: utf-8 -*-
# Edit: turnipsmart.com
import os, sys

running = True
menu = """
  Main Menu  
--------------------
 1: Display Options
 2: Config  Options
 3: Deteting
 h: Help
 q: Quit
--------------------
"""
menu_dict = {
    "h": "Please enter the options to be operated.",
    "1": "df -h",
    "2": "free -m",
    "3": "netstat -lnt",
}


def commands(args):
    cmd = menu_dict.get(args)
    return cmd


if __name__ == "__main__":
    os.system('cls')
    print(menu)
    while running:
        cmd = input("Input Your Commond:")
        if cmd != 'q':
            os.system('cls')
            try:
                print
                menu
                if commands(cmd) != None:
                    # fo = os.popen(commands(cmd))
                    # print fo.read()
                    if cmd == '1':
                        print
                        "cmd=1"
                    elif cmd == '2':
                        print
                        "cmd=2"
                    elif cmd == '3':
                        print
                        "cmd=3"
                    else:
                        print
                        commands(cmd)
                else:
                    print
                    "Input is Wrong!"
            except Exception, e:
                print(menu)
                print(e)
    else:
        print
        'We will exit the menu.'
    os.system('cls')
    sys.exit()