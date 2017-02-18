import mpm_manager

CMAND = "modules unload"


def main(c):
    module_name = c.replace(CMAND, "")
    module_name = module_name.strip()

    if not module_name:
        raise Exception("%s 'name of modules' or '-a' for all" % CMAND)

    m = mpm_manager.ModuleManager()

    if module_name == "-a":
        m.unload_all()
    else:
        m.unload(module_name)
