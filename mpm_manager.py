# Message Processing Module Manager
import os
from imp import reload
from os import walk

MPM_PATH = "modules/"


class ModuleManager:

    # class describes mp modules
    class Module():
        module_name = None
        module_version = None
        module_author = None
        module_description = None
        module_entry = None
        module_fname = None
        module_extra = None
        res = None

        def execute_module(self, message, lpt):
            if not self.process_extra(message):
                return None

            exec('from %s import %s' % (MPM_PATH.replace("/", ""), self.module_fname))
            exec("reload(" + self.module_fname + ")")
            exec("self.res = %s.%s(message, lpt)" % (self.module_fname, self.module_entry))
            return self.res

        def print(self):
            print("Module (%s) '%s': '%s' [%s] - %s" % (self.module_fname,
                                                 self.module_name,
                                                 self.module_version,
                                                 self.module_author,
                                                 str(self.module_description)
                                                 ))

        def __init__(self, module_author=None, module_description=None, module_name=None, module_version=None,
                     module_entry="main", module_extra=None):
            self.module_author = module_author
            self.module_description = module_description
            self.module_name = module_name
            self.module_version = module_version
            self.module_entry = module_entry
            self.module_extra = module_extra

        def process_extra(self, message):
            b = True

            if type(self.module_extra) == dict:
                if "on_body" in self.module_extra:
                    b = b and message.body == self.module_extra["on_body"]
                if "attach_type" in self.module_extra:
                    found = False
                    atype = self.module_extra['attach_type']
                    for attach in message.attachments:
                        if atype == attach.attachment_type:
                            found = True
                    b = b and found



            return b
            pass

    # get list of available modules
    def get_modules(self):

        modules = []
        files = []
        for (dirpath, dirnames, filenames) in walk(MPM_PATH):
            files.extend(filenames)
            break

        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                try:
                    module = self.get_module_from_file(file.replace(".py", ""))
                    if module is not None:
                        modules.append(module)
                except Exception as error:
                    print("[LP] [MPM MANAGER] Error: %s" % str(error))
                    pass
        return modules


    # get modules by name
    def get_module_from_file(self, file, quiet=False):
        exec('from modules import %s' % file)
        exec("reload(" + file + ")")
        m = self.Module()
        m.module_fname = file
        try:
            exec('m.module_version = %s.module_version' % file)
            exec('m.module_name = %s.module_name' % file)
            exec('m.module_author = %s.module_author '% file)
        except AttributeError:
            if not quiet:
                print("[LP] [MPM MANAGER] MODULE %s is invalid!"
                  " Try to define module_version (str), module_name (str) and module_author (str)"
                  " vars" % file)
            return None
        try:
            exec('m.module_description = %s.module_description' % file)
        except AttributeError:
            pass
        try:
            exec('m.module_entry = %s.module_entry' % file)
        except AttributeError:
            pass
        try:
            exec('m.module_extra = %s.module_extra  ' % file)
        except AttributeError:
            pass

        return m

        pass

    # Get lost of modules
    # that has filename *.py.disabled
    # These files is not returning in get_modules()
    def get_disabled_modules(self):
        modules = []
        files = []
        for (dirpath, dirnames, filenames) in walk(MPM_PATH):
            files.extend(filenames)
            break

        for file in files:
            if file.endswith(".py.disabled") and file != "__init__.py":
                modules.append(file.replace(".py.disabled", ""))
        return modules

        pass

    # set name from *.py.disabled to *.py (enables modules specified in @name)
    def load(self, name):
        # get list of disabled modules
        modules = self.get_disabled_modules()
        success = 0
        for module in modules:
            # checking if name of needed modules is equal to current modules in loop
            if name == module:
                # rename file of modules
                os.rename(MPM_PATH + name + ".py.disabled", MPM_PATH + name + ".py")
                # print result to user
                print("Module '%s' successfully enabled" % name)
                success = 1
                break
        if success is 0:
            raise Exception("Module %s not found or already loaded" % name)
        pass

    # set name from *.py to *.py.disabled (disables modules specified in @name)
    def unload(self, name):
        # get list of enbled modules
        modules = self.get_modules()
        success = 0
        for module in modules:
            # checking if name of needed modules is equal to current modules in loop
            if name == module.module_fname:
                # rename file of modules
                os.rename(MPM_PATH + name + ".py", MPM_PATH + name + ".py.disabled")
                # print result to user
                print("Module '%s' successfully disabled" % name)
                success = 1
                break
        if success is 0:
            raise Exception("Module '%s' not found or already unloaded" % name)

    def unload_all(self):
        modules = self.get_modules()
        for module in modules:
            # rename file of modules
            os.rename(MPM_PATH + module.module_fname + ".py", MPM_PATH + module.module_fname + ".py.disabled")
            # print result to user
            print("Module '%s' successfully disabled" % module.module_fname)
            break

    def load_all(self):
        modules = self.get_disabled_modules()
        for module in modules:
            # rename file of modules
            os.rename(MPM_PATH + module + ".py.disabled", MPM_PATH + module + ".py")
            # print result to user
            print("Module '%s' successfully enabled" % module)
            break




