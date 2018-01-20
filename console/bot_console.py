import os
from imp import reload
import bot_header


class Console(object):
    acc = None
    acc_number = None

    def get_message(self):
        if self.acc is not None:
            return "%s >> " % self.acc.first_last()
        else:
            return ''


    def exec_startup(self):
        with open("startup.hsh") as f:
            content = f.readlines()
            # you may also want to remove whitespace characters like `\n` at the end of each line
            content = [x.strip() for x in content]
            for x in content:
                if x.startswith('.'):
                    print(x[1:].strip())
                    continue
                elif x.startswith('#'):
                    continue
                self.run(x)
        bot_header.CONSOLE_STARTED = True


    def run_looped(self):
        # process startup scripts
        if not bot_header.CONSOLE_STARTED:
            self.exec_startup()
        while 1:
            ui = input(self.get_message())
            self.run(ui)

    def run(self, ui):

        # pass if user pressed
        if not ui:
            return 1

        self.process_dir(ui, "")
        return 0

    def process_dir(self, ui, dir):
        ui = ui.strip()
        for dirname, dirnames, filenames in os.walk('console'):
            # print path to all filenames.
            for file in filenames:
                if not file.endswith(".py") or file == "bot_console.py":
                    continue
                file = os.path.join(dirname, file).replace(os.sep, "/").replace("console/", "", 1)\
                    .replace(".py", "")
                cmd = file.replace("/", " ")
                py = file.replace("/", ".")
                if ui.startswith(cmd):
                    exec('import console.' + py)
                    exec("reload(console." + py + ")")
                    execute_str = "result = console.%s.%s(ui)" % (py, "main")
                    exec(execute_str)
                    return 0
            for file in dirnames:
                file = os.path.join(dirname, file.replace(os.sep, "/"))
                cmd = file.replace("console%s" % os.sep, "", 1).replace(os.sep, " ")
                if ui == cmd:
                    r = ""
                    files = os.listdir(file)
                    for file in files:
                        if file.__contains__("__"):
                            continue
                        file = file.replace(".py", "")
                        if not r:
                            r += file
                        else:
                            r += "|" + file

                    print("Usage: %s" %(r))
                    return 0

        print("Unknown command '%s'" % ui)
