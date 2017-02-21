
# Parse time by string e.g:
import re


def parse_time(time):
    if type(time) == int:
        return time
    elif type(time) == str:
        rtime = 0
        r = re.findall("(\d+)s", time)
        for o in r:
            rtime += int(o)

        r = re.findall("(\d+)m", time)
        for o in r:
            rtime += int(o) * 60

        r = re.findall("(\d+)h", time)
        for o in r:
            rtime += int(o) * 3600

        r = re.findall("(\d+)d", time)
        for o in r:
            rtime += int(o) * 3600 * 24
        return rtime
