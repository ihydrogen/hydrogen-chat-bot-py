#-------------------------------------------------------------------------------
# Name:        pastebin manager
# Description: provides methods for pastebin paste managment
#
# Author:      hydrogen-nt
#
# Created:     13.01.2018
# Copyright:   (c) hydrogen-nt 2018
#-------------------------------------------------------------------------------

import requests
import xml.etree.ElementTree as ET
from sys import argv
import os


"""
<paste>
	<paste_key>0b42rwhf</paste_key>
	<paste_date>1297953260</paste_date>
	<paste_title>javascript test</paste_title>
	<paste_size>15</paste_size>
	<paste_expire_date>1297956860</paste_expire_date>
	<paste_private>0</paste_private>
	<paste_format_long>JavaScript</paste_format_long>
	<paste_format_short>javascript</paste_format_short>
	<paste_url>https://pastebin.com/0b42rwhf</paste_url>
	<paste_hits>15</paste_hits>
</paste>
"""

# Pastebin.com paste object
class Paste():
    paste_key = None
    paste_date = None
    paste_title = None
    paste_size = None
    paste_expire_date = None
    paste_private = None
    paste_format_long = None
    paste_url = None
    paste_hits = None

    pass

###                   KEYS need for pastebin API          ###
# Pastebin API dev key
PASTE_BIN_API_KEY = "05494a8c839e7f74cc757c402a647b3e"
# Pastebin API usr key
PASTE_BIN_API_KEY_U = "e17c41ee778cdcf57aa35b1da0422f5e"
###                                                       ###

# Creating new paste
def create_new_paste(code, name=''):
    r = requests.post("https://pastebin.com/api/api_post.php", data={
                'api_dev_key': PASTE_BIN_API_KEY,\
                'api_user_key': PASTE_BIN_API_KEY_U,\
                 'api_option': 'paste', \
                 'api_paste_code': code, \
                 'api_paste_name': name, \
                 'api_paste_private': 2, \
                 'api_paste_expire_date': 'N'
                                                })
    return r.text


# XML Server response processing
def process_xml(text):
    # Make XML Response valid for python XML parser
    text = "<response>\n%s\n</response>" % text
    # Parse XML Response string
    r00t = ET.fromstring(text)
    # Create empty pasts list
    # ...
    xpastes = []
    for child in r00t:
        # Parsing data
        if child.tag == 'paste':
            xpaste = Paste()
            xpaste.date = child[1].text
            xpaste.paste_title = child[2].text
            xpaste.paste_size = child[3].text
            xpaste.paste_expire_date = child[4].text
            xpaste.paste_private = child[5].text
            xpaste.paste_format_long = child[6].text
            xpaste.paste_url = child[8].text
            xpaste.paste_hits = child[9].text
            xx = xpaste.paste_url.split("/")
            xpaste.paste_key = xx[len(xx) - 1]

            # Adding data to pasts list
            xpastes.append(xpaste)
    return xpastes

# Get's API usr key
def reg_user(u, p):
    r = requests.post("https://pastebin.com/api/api_login.php", data={"api_dev_key": PASTE_BIN_API_KEY, 'api_user_name': u, "api_user_password": p})
    return r.text

# Remove paste by key
def delete_paste(key):
    r = requests.post("https://pastebin.com/api/api_post.php", data={"api_dev_key": PASTE_BIN_API_KEY, 'api_option': 'delete', 'api_user_key': PASTE_BIN_API_KEY_U, 'api_paste_key': key})
    return  "Paste Removed" in r.text.strip()


# Get RAW private paste
"""
1. api_dev_key - this is your API Developer Key, in your case: 05494a8c839e7f74cc757c402a647b3e
2. api_user_key - this is the session key of the logged in user. How to obtain such a key
3. api_paste_key - this is paste key you want to fetch the data from.
4. api_option - set as 'show_paste'

"""
def get_private_paste_raw(paste=None, paste_key=None):
    if paste_key == None:
        if paste != None:
            paste_key = paste.paste_key
        else:
            raise AttributeError("need to specify 'paste' or 'paste_key' parameters")

    print(paste_key)

    r = requests.post("https://pastebin.com/api/api_raw.php", data={
                'api_dev_key': PASTE_BIN_API_KEY,\
                'api_user_key': PASTE_BIN_API_KEY_U,\
                'api_paste_key': paste_key, \
                'api_option': 'show_paste' })

    return r.text


def pastes_get():
    r = requests.post("https://pastebin.com/api/api_post.php", data={"api_dev_key": PASTE_BIN_API_KEY, 'api_option': 'list', 'api_user_key': PASTE_BIN_API_KEY_U, 'api_results_limit': 1000})
    return process_xml(r.text)
    pass

def read(fname):
    with open(fname) as f:
        content = f.read()
    return content

def main():
    name = argv[1]
    if len(argv) >= 2:
        if os.sep in argv[1]:
            names = argv[1].split(os.sep)
            name =  names[len(names) - 1]
        print(create_new_paste(read(argv[1]), name=name))

if __name__ == '__main__':
    main()
