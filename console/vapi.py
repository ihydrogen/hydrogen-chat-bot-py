#-------------------------------------------------------------------------------
# Name:        VK_API_CONSOLE
#
# Author:      hydrogen-nt
#
# Created:     13.01.2018
# Copyright:   (c) hydrogen-nt 2018
#
# implements using VK api on console
# by typing "vapi [method] [params (x='y',)]"
#-------------------------------------------------------------------------------

from sys import argv
from vk_api.api import vapi

def print_usage():
    print("vapi [method] [params]")

#main method
def main(c):
    c = c.replace("vapi", "").strip()
    if not c:
        print_usage()
        return 0

    method = ''
    params = None
    if ' ' in c:
        arr = c.split(' ')
        method = arr[0]
        if len(arr) >= 2:
            params = arr[1]
    else:
        method = c

    x = vapi(method, params=params)
    print(x)