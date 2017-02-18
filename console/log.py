import bot_header

CMAND = "log"

def main(c):

    # get all after 'log'
    cnt = str(c).replace(CMAND, "")
    cnt = cnt.strip()

    if cnt and not str.isnumeric(cnt):
        raise Exception("value must be numeric")

    if not cnt:
        for l in bot_header.LOG:
            print("[LOG] " + l)
    else:
        # convert all after 'log' to integer
        _len = int(cnt)

        # get length of log list
        ll = len(bot_header.LOG)


        if _len > ll:
            _len = ll

        for i in range(ll - _len, ll):
            print("[LOG] " + bot_header.LOG[i])