#!/bin/python
# <copyright-info>
# </copyright-info>
# 
# author: Iliyan (Tank) Stankov
# version: 1.0
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
import time
import platform
from datetime import datetime as dt

### Global Constants
path_to_hosts_file_Windows           = "C:\\Windows\\System32\\drivers\\etc\\hosts"
path_to_hosts_file_Linux_and_Mac     = "/etc/hosts"
path_to_list_of_distracting_websites = "distracting_websites_list"
localhost                            = "127.0.0.1"

### Global Variables
work_start = dt.strptime("8:30", "%H:%M")
work_end   = dt.strptime("13:00", "%H:%M")

### Function Definitions
## -----------------------------------------------------------------------------
def check_if_now_is_within_working_hours(work_start, work_end):
    if (dt.strftime(work_start, "%H:%M") 
        < dt.strftime(dt.now(), "%H, %M") 
        < dt.strftime(work_end, "%H:%M")):
        return "yes"
    else:
        return "no"

## -----------------------------------------------------------------------------
def block_websites(hosts_file):
    websites_to_block = get_list_of_distracting_websites()

    with open(hosts_file, "r+") as fd:
        content = fd.read()
        for website in websites_to_block:
            if website in content:
                pass
            else:
                fd.writelines(localhost + " " + website + "\n")

## -----------------------------------------------------------------------------
def unblock_websites(hosts_file):
    websites_to_block = get_list_of_distracting_websites()

    with open(hosts_file, "r+") as fd:
        content = fd.readlines()
        fd.truncate(0)
        for line in content:
            if not any(website in line for website in websites_to_block):
                fd.write(line)

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
    
    with open(path_to_list_of_distracting_websites, "r") as fd:
        websites_to_block = fd.read().splitlines()

    return websites_to_block

################################################################################
## MAIN FUNCTION
###########
def main():    
    path_to_hosts_file = check_os_type_and_return_path_to_hosts_file()
    websites_are_blocked = "I dont know" ## Random starting value

    while True:
        if (check_if_now_is_within_working_hours(work_start, work_end) == "yes"):
            if websites_are_blocked != "yes":
                block_websites(path_to_hosts_file)
                websites_are_blocked = "yes"
        else:
            if websites_are_blocked != "no":
                unblock_websites(path_to_hosts_file)
                websites_are_blocked = "no"

        time.sleep(30)

## -----------------------------------------------------------------------------
if __name__ == '__main__':
    main()
