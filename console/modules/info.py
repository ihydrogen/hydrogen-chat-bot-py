import mpm_manager

CMAND = "modules info"

def main(c):
    module_name = str(c).replace(CMAND, "")
    module_name = module_name.strip()

    if not module_name:
        raise Exception("%s 'name of module' or '-a' for all" % CMAND)

    m = mpm_manager.ModuleManager()
    for module in m.get_modules():
        if module_name.replace(".py", "") == module.module_fname or module_name == "-a":
            module.print()