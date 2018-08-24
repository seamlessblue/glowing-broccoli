#!/bin/python
# <copyright-info>
# </copyright-info>
# 
# author: Iliyan (Tank) Stankov
# version: 1.1
#
################################################################################
# File name:
#    WebSite_Blocker.py
#
# Usage: 
#    ./WebSite_Blocker.py
#
# Description:
#    This tool will block websites.
# It does it by modifying "/etc/hosts" to contain "127.0.0.1" for every webSite
# the user would like to block.
#
# It also has logic to block the website only during certain time of the day.
#
# Important:
#    The script depends on "distracting_websites_list" file to be in the same
# directory. It contains the list of websites to be blocked.
#    The script requires elevated privilages (Administrator/root/sudo) to work.
#
################################################################################

### Imports
import sys
import time
import getopt
import platform
from pathlib import Path
from datetime import datetime as dt

### Global Constants
p_distracting_websites_list = Path.cwd() / "in" / "distracting_websites_list_"
p_hosts_file_windows        = Path("C:\\Windows\\System32\\drivers\\etc\\hosts")
p_hosts_file_linux_and_mac  = Path("hosts_test")
localhost                   = "127.0.0.1"
usage                       = "Usage: ./WebSite_Blocker.py -m <easy|nightmare>"
modes                       = ['easy', 'nightmare']

### Global Variables
work_start = dt.strptime("7:30", "%H:%M")
work_end   = dt.strptime("18:00", "%H:%M")

### Function Definitions
## -----------------------------------------------------------------------------
def check_if_now_is_within_working_hours(work_start, work_end):
    if (dt.strftime(work_start, "%H:%M") 
        < dt.strftime(dt.now(), "%H, %M") 
        < dt.strftime(work_end, "%H:%M")):
        return True 
    else:
        return False

## -----------------------------------------------------------------------------
def block_websites(hosts_file, block_mode):
    websites_to_block = get_list_of_distracting_websites(block_mode)

    try:
        with open(hosts_file, "r+") as fd:
            content = fd.read()
            for website in websites_to_block:
                if website in content:
                    pass
                else:
                    fd.writelines(localhost + " " + website + "\n")
    except PermissionError:
        print("You don't have permission to edit 'hosts' file.")
        print("Make sure you are running the script as Administrator/root/sudo!")
        print("Exiting program.")
        sys.exit()

## -----------------------------------------------------------------------------
def unblock_websites(hosts_file, block_mode):
    websites_to_block = get_list_of_distracting_websites(block_mode)

    try:
        with open(hosts_file, "r+") as fd:
            content = fd.readlines()
            fd.truncate(0)
            for line in content:
                if not any(website in line for website in websites_to_block):
                    fd.write(line)
    except PermissionError:
        print("You don't have permission to edit 'hosts' file.")
        print("Make sure you are running the script as Administrator/root/sudo!")
        print("Exiting program.")
        sys.exit()

## -----------------------------------------------------------------------------
def check_os_type_and_return_path_to_hosts_file():
    os_type = platform.system()

    if (os_type == "Darwin" or os_type == "Linux"):
        return p_hosts_file_linux_and_mac
    else:
        return p_hosts_file_windows 

## -----------------------------------------------------------------------------
def get_list_of_distracting_websites(block_mode):
    websites_to_block = []
    global p_distracting_websites_list
    temp = p_distracting_websites_list.name + block_mode
    p_distracting_websites_list = p_distracting_websites_list.parent / temp

    try:
        with open(p_distracting_websites_list, "r") as fd:
            websites_to_block = fd.read().splitlines()
            if len(websites_to_block) > 0:
                return websites_to_block 
            else:
                print("'Distracting_websites_list' file is empty.")
                print("There are no websites to block. Exiting program.")
                sys.exit()
    except FileNotFoundError:
        print("'Distracting_websites_list' file cannot be found.")
        print("Make sure that it is located in the same directory as this script.")
        print("Exiting proram.")
        sys.exit()

################################################################################
## MAIN FUNCTION
###########
def main(argv):
    
    if len(sys.argv) == 1:
        block_mode = "nightmare"
    elif len(sys.argv) <= 3:
        try:    
            opts, args = getopt.getopt(argv, "hm:")        
            for opt, arg in opts:
                if opt == "-m":
                    if arg in modes:
                        block_mode = arg
                    else:
                        print(usage)
                        sys.exit()
                elif opt == "-h":
                    print(usage)
                    sys.exit()
        except getopt.GetoptError:
            print(usage)
            sys.exit()
    else:
        print(usage)
        sys.exit()

    path_to_hosts_file = check_os_type_and_return_path_to_hosts_file()
    websites_are_blocked = None 

    while True:
        try:
            if (check_if_now_is_within_working_hours(work_start, work_end)):
                if websites_are_blocked is not True:
                    block_websites(path_to_hosts_file, block_mode)
                    websites_are_blocked = True
            else:
                if websites_are_blocked is not False:
                    unblock_websites(path_to_hosts_file, block_mode)
                    websites_are_blocked = False
            time.sleep(30)
        except KeyboardInterrupt:
            print("The program was interrupted with 'CTRL+C'.")
            sys.exit()

## -----------------------------------------------------------------------------
if __name__ == '__main__':
    main(sys.argv[1:])
