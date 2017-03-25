import vk

import vk_api
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

# Defines message object
class Message:

    class MessageAttachment:
        attachment_value = None
        attachment_type = None

        def __init__(self, type, value):
            self.attachment_type = type
            self.attachment_value = value

    mid = None # ID of message
    flag = None # message flags (See VK Long pool docs)
    pid = None # peer id (Sender id)
    ts = None # timestamp
    sub = None # subject of message (if private dialog - " ... ", if chat - chat title)
    body = None # test of message
    extra = None # extra fields (forwarded messages, etc)
    attachments = None

    # get specific message flag (See VK Long pool docs)
    def msgFlag(self, i, f):
        return (f & i) > 0

    # check is message not incoming
    def is_out(self):
        return self.msgFlag(self.flag, 2)

    def is_loopback(self, account=None):
        if account is None:
            account = bot_header.CURRENT_ACCOUNT
        return  self.pid == account.user_id

    # check is message sent from chat
    def is_chat(self):
        return self.pid >= 2000000000

    # init
    def __init__(self, mid=None, flag=None, pid=None, ts=None, sub=None, body=None, extra=None):
        self.mid = mid
        self.flag = flag
        self.pid = pid
        self.ts = ts
        self.sub = sub
        self.body = body
        self.extra = extra
        if extra is not None:
            self.attachments = self.parse_attachments()

    # get message from long pool response
    def from_long_pool(self, resp):
        mid = resp[1]
        flag = resp[2]
        pid = resp[3]
        ts = resp[4]
        sub = resp[5]
        body = resp[6]
        extra = resp[7]
        return Message(mid=mid, flag=flag, pid=pid, ts=ts, sub=sub, body=body, extra=extra)

    def parse_attachments(self):
        # print(self.extra)
        # initialize empty list
        result = []

        # checking for attachments
        if not "attach1_type" in self.extra:
            return result

        # if message has attachs, start parsing
        # parse attachment
        i = 1
        print("id: %s" % i)
        # get attach by number
        while "attach%s_type" % i in self.extra:
            attach_type = self.extra["attach%s_type" % str(i)]
            attach_val = self.extra["attach%s" % str(i)]
            if attach_type == "doc":
                if "attach%s_kind" % str(i):
                    if self.extra["attach%s_kind" % str(i)] == "audiomsg":
                        attach_type = "amessage"
            print("Got id %s with data %s" % (attach_type, attach_val))
            result.append(Message.MessageAttachment(attach_type, attach_val))
            i+=1
        return result


def get_api(lpt = None, account=None):
    if lpt == None and account == None:
        raise AttributeError("longpool thread or account is required")
    if lpt is not None:
        account = lpt.account

    return vk.API(vk.Session(access_token=account.token))

def api_request(api, method, params=''):
    ret = dict(api=api, ret = None)
    if params:
        a = "ret = api.%s(v='5.62', %s)" % (method, params)
    else:
        a = "ret = api.%s(v='5.62')" % (method)

    exec(a, ret)

    if 'error' in str(ret['ret']):
        bot_header.API_REQUESTS += 1
    else:
        bot_header.FAILED_API_REQUESTS += 1


    return ret['ret']

def vapi(method, params=''):
    return api_request(get_api(account=bot_header.CURRENT_ACCOUNT), method, params)
