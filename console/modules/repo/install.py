import pbmgr
import mpm_manager
import sys
from utils.http import download_file
import os

def main(c):
    c = c.replace("modules repo install", '').strip()
    #print("Looking for %s ..." % c
    #print("Getting available modules list ...")
    modules = pbmgr.pastes_get()
    for module in modules:
        c = c.lower() + ".py"
        if c == module.paste_title.lower().strip():
            print("Found %s" % module.paste_title)
            #raw_url = "https://pastebin.com/raw/%s" % module.paste_key
            print("Downloading with pastebin API")
            #download_file(raw_url, "modules%s%s" % (os.sep, module.paste_title))
            data = pbmgr.get_private_paste_raw(module)
            with open("modules%s%s" % (os.sep, module.paste_title), "wt") as file:
                file.write(data)
            print("Module saved.")
            try:
                mpm_manager.ModuleManager().get_module_from_file(module.paste_title.replace(".py", "")).print()
            except Exception as e:
                print("Module not loaded: %s" % str(e))