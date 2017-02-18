import mpm_manager

CMAND = "modules load"


def main(c):
    module_name = c.replace(CMAND, "")
    module_name = module_name.strip()

    if not module_name:
        raise Exception("%s 'name of module' or '-a' for all" % CMAND)

    m = mpm_manager.ModuleManager()
    if module_name == "-a":
        m.load_all()
    else:
        m.load(module_name)
