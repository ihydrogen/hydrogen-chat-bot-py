import vk

import bot_header


class User():
    first_name = ''
    last_name = ''
    user_id = ''


    def first_last(self):
        return "%s %s" % (self.first_name, self.last_name)

    def from_json(d):
        s = User()
        s.__dict__.update(d)
        return s



# class describes user account
class Account(User):
    token = ''

    def from_json(d):
        s = Account()
        s.__dict__.update(d)
        return s

class Message:
    mid = None
    flag = None
    pid = None
    ts = None
    sub = None
    body = None
    extra = None


    def msgFlag(self, i, f):
        return (f & i) > 0

    def is_out(self):
        return self.msgFlag(self.flag, 2)

    def is_chat(self):
        return self.pid >= 2000000000

    def __init__(self, mid=None, flag=None, pid=None, ts=None, sub=None, body=None, extra=None):
        self.mid = mid
        self.flag = flag
        self.pid = pid
        self.ts = ts
        self.sub = sub
        self.body = body
        self.extra = extra

    def from_long_pool(self, resp):
        mid = resp[1]
        flag = resp[2]
        pid = resp[3]
        ts = resp[4]
        sub = resp[5]
        body = resp[6]
        extra = resp[7]
        return Message(mid=mid, flag=flag, pid=pid, ts=ts, sub=sub, body=body, extra=extra)

def get_api(lpt):
    return vk.API(vk.Session(access_token=lpt.account.token))

def api_request(api, method, params):
    ret = dict(api=api, ret = None)
    a = "ret = api.%s(v='5.62', %s)" % (method, params)
    exec(a, ret)
    if type(ret['ret'] is int):
        bot_header.API_REQUESTS += 1
    else:
        bot_header.FAILED_API_REQUESTS += 1


    return ret['ret']