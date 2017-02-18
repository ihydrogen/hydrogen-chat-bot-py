import os,sys,inspect
import traceback
from imp import reload
# set current path to root of project
import bot_header

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from enum import Enum

class LongPoolEvent(Enum):
    MESSAGE_FLAG_REPLACE = 1
    MESSAGE_FLAG_SET = 2
    MESSAGE_FLAG_RESET = 3
    MESSAGE_SEND = 4
    MESSAGE_READALL_OUT = 7
    MESSAGE_READALL_IN = 6
    FRIEND_ONLINE = 8
    FRIEND_OFFLINE = 9
    FILTER_FLAG_RESET = 10
    FILTER_FLAG_REPLACE = 11
    FILTER_FLAG_SET = 12
    MCHAT_PARAM_CHANGE = 51
    START_TYPING_C = 61
    START_TYPING_MC = 62
    UNREAD_UPDATE = 80
    UNKNOWN = -1

    def __str__(self):
        return '%s' % self._value_


    def process(evid, resp, lp_thread_ins):
        # get name of event by id
        method_name = LongPoolEvent(evid).name.lower()
        # execute file in $rootOfProject/long_pool_events/$nameOfMethod
        try:
            exec('from long_pool_events import module_%s' % method_name)
            exec("reload( module_" + method_name + ")")
            exec('module_%s.main(resp, lp_thread_ins)' % method_name)
            # exec("retval = LongPoolEvent.__%s__(evid)" % method_name)
        except ImportError as e:
            bot_header.v(e)
            bot_header.v("---W---[LP] define new file in long_pool_events: module_%s with method 'main'" % method_name)
            pass
        except Exception as exc:
            exceptiondata = traceback.format_exc().splitlines()
            exceptionarray = exceptiondata[-1] + " " + exceptiondata[-2] + " " + exceptiondata[-3]
            bot_header.w("[LP] Exception in modules %s:\n  | %s Trace:\n  | %s" % (method_name,
                                                                  str(exc),
                                                                  str(exceptionarray)))
