import re
from utils import time_utils


class AutoexecRule:
    id = None
    ticks = None
    time_each = None
    time_when = None
    action = None
    action_value = None

    def from_json(d):
        s = AutoexecRule(force=True)
        s.__dict__.update(d)
        return s

    def __init__(self, time_each=None, time_when=None, action_type=None, force=False):
        if not force:

            if not time_each:
                time_each = None

            if not time_when:
                time_when = None

            print("%s%s" % (time_each, time_when))

            if time_each == None and time_when == None:
                raise AttributeError("You must specify time when it action will be go")

            if time_each != None and time_when != None:
                raise AttributeError("You can't specify each and when parameters in the same time")

            if time_when is not None:
                self.time_when = time_utils.parse_time(time_when)

            if time_each is not None:
                self.time_each = time_utils.parse_time(time_each)

        pass

