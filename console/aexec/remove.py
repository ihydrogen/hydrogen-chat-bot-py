from optparse import OptionParser

import bot_header
from autoexec.autoexec_rules_manager import AutoexecRulesManager
from utils.time_utils import parse_time
from autoexec.autoexec_action_type import AutoexecActionType
from autoexec.autoexec import AutoexecRule


def main(c):
    parser = OptionParser()
    parser.set_usage(__name__.replace(".", " ") + " [OPTIONS]")
    parser.add_option("-#", "--id", dest="id", help="set id")
    parser.add_option("-?", "--?", default=None, action="callback", callback=help, help="show this help message")

    o, a = parser.parse_args(c.split())
    o = o.__dict__

    id = o['id']

    mgr = AutoexecRulesManager()

    if id is not None and str.isnumeric(id):
        id = int(id)
    else:
        raise Exception("invalid id")
    print("Removing rule with id=%s" % (id))
    mgr.remove(id)


def help(option, opt, value, parser):
    parser.print_help()
