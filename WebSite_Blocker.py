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
import platform
from datetime import datetime as dt

### Global Constants
path_to_hosts_file_Windows           = "C:\\Windows\\System32\\drivers\\etc\\hosts"
path_to_hosts_file_Linux_and_Mac     = "hosts_test"
path_to_list_of_distracting_websites = "distracting_websites_list"
localhost                            = "127.0.0.1"

### Global Variables
work_start = dt.strptime("9:30", "%H:%M")
work_end   = dt.strptime("13:00", "%H:%M")

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
def block_websites(hosts_file):
    websites_to_block = get_list_of_distracting_websites()

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
def unblock_websites(hosts_file):
    websites_to_block = get_list_of_distracting_websites()

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
        return path_to_hosts_file_Linux_and_Mac
    else:
        return path_to_hosts_file_Windows 

## -----------------------------------------------------------------------------
def get_list_of_distracting_websites():
    websites_to_block = []

    try:
        with open(path_to_list_of_distracting_websites, "r") as fd:
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
def main():    
    path_to_hosts_file = check_os_type_and_return_path_to_hosts_file()
    websites_are_blocked = None 

    while True:
        try:
            if (check_if_now_is_within_working_hours(work_start, work_end)):
                if websites_are_blocked is not True:
                    block_websites(path_to_hosts_file)
                    websites_are_blocked = True
            else:
                if websites_are_blocked is not False:
                    unblock_websites(path_to_hosts_file)
                    websites_are_blocked = False
            time.sleep(30)
        except KeyboardInterrupt:
            print("The program was interrupted with 'CTRL+C'.")
            sys.exit()

## -----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
