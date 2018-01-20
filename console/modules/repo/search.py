import pbmgr
import sys
import bot_header

def main(c):
    c = c.replace("modules repo search", '').strip()
    if not c:
        print(bot_header.WARNING + "You need to say what you wanna search")
        return 1

    # get list of pastes
    print("Getting available modules list ...")
    modules = pbmgr.pastes_get()
    print("Looking for %s ..." % c)
    for module in modules:
        print(module.paste_title + "\n" if c.lower().strip() in module.paste_title.lower().strip() else "", end="")
