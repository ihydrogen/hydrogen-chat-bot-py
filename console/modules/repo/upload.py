import pbmgr
import sys
import mpm_manager
import os


def check_that_not_exists_on_pb(file):
    print("Getting available modules list ...")
    modules = pbmgr.pastes_get()
    for module in modules:
        #print(module.paste_title.strip(), file.strip())
        if module.paste_title.strip() == file.strip():
            return False
    return True


def main(c):
    c = c.replace("modules repo upload", '').strip()
    if not c:
        print("upload [module name] [...]")
        return 1
    #print("Looking for %s ..." % c
    print("Preraping to upload %s ..." % c)
    mm = mpm_manager.ModuleManager()
    try:
        c.replace('.py', '')
        module = mm.get_module_from_file(c)
        filename = "modules" + os.sep + module.module_fname + '.py'
        print("Finisshing preparing ...")
        if check_that_not_exists_on_pb(c + '.py'):
            print("Uploading module ...")
            pbmgr.create_new_paste(pbmgr.read(filename), name=c+".py")
            print("Module successfully uploaded")

        else:
            print("Error uploading module!")
            print("Module already uploaded")

    except Exception as e:
        print("Error uploading module!")
        print(e)
        return 1
