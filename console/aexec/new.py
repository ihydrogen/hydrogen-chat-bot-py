from optparse import OptionParser

import bot_header
from autoexec.autoexec_rules_manager import AutoexecRulesManager
from utils.time_utils import parse_time
from autoexec.autoexec_action_type import AutoexecActionType
from autoexec.autoexec import AutoexecRule

def get_action_type(param):
    if param == 'HC_CONSOLE':
        return AutoexecActionType.ACTION_HC_CONSOLE
    else:
        return None
    pass


def main(c):
    parser = OptionParser()
    parser.set_usage(__name__.replace(".", " ") + " [OPTIONS]")
    parser.add_option("-t", "--type", dest="type", help="type of the rule (when - exec after some time and delete, each - execute each time)")
    parser.add_option("-T", "--time", dest="time", help="time: format: *s/m/h/d")
    parser.add_option("-a", "--action-type", dest="action", help="the action type of rule (now available only HC_CONSOLE)")
    parser.add_option("-A", "--action-value", dest="action_value", help="the value of action (USE /s instead of spaces) (in case of action type 'HC_CONSOLE' it's command to execute in console)")
    parser.add_option("-#", "--id", dest="id", help="use specific id (not required because it will be generated automatically if not defined)")
    parser.add_option("-?", "--?", default=None, action="callback", callback=help, help="show this help message")

    o, a = parser.parse_args(c.split())
    o = o.__dict__
    type = o['type']

    if str.isnumeric(o['time']):
        time = int(o['time'])
    else:
        time = parse_time(o['time'])

    a_type = get_action_type(o['action'])
    a_type_val = o['action_value']
    id = o['id']

    a = AutoexecRule(force=True)
    if type == 'each':
        a.time_each = time
    elif type == 'when':
        a.time_when = time
    else:
        raise Exception("Invalid rule type (-t/--type=) each|when")

    if a_type is not None:
        a.action = a_type
    else:
        raise Exception("Invalid action type (-a/--action-type) HC_CONSOLE")

    mgr = AutoexecRulesManager()

    a.action_value = a_type_val.replace("/s", " ")
    if id is not None and str.isnumeric(id):
        a.id = int(id)
    else:
        a.id = len(mgr.get_all_rules())

    print("Creating rule with params: time (each/when)=%s/%s, id=%s, atype=%s, aval=%s" % (a.time_each, a.time_when, a.id, a.action, a.action_value))
    mgr.add_rule(a)



def help(option, opt, value, parser):
    parser.print_help()
