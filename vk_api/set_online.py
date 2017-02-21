import threading
from time import sleep

import bot_header
from vk_api.api import api_request, get_api


class OnlineThread(threading.Thread):
    account = None
    enabled = True
    interval = 20

    def __init__(self, lpt=None, account=None, enabled=True, interval=30):
        super().__init__()

        if lpt == None and account == None:
            raise AttributeError("longpool thread or account is required")
        if lpt is not None:
            self.account = lpt.account
        elif account is not None:
            self.account = account
        self.enabled = enabled
        self.interval = interval


    def print(self, text):
        print('[::OTHD] [%s] %s' % (self.account.first_last(), text))

    def v(self, text):
        bot_header.v('[::OTHD] [%s] %s' % (self.account.first_last(), text))

    def w(self, text):
        bot_header.w('[::OTHD] [%s] %s' % (self.account.first_last(), text))

    def set_online(self, online):
        if online:
            method = "account.setOnline"
            response = api_request(get_api(account=self.account), method, "voip=0")
            return response
        else:
            method = "account.setOffline"
            response = api_request(get_api(account=self.account), method, "")
            return response

    def stop(self):
        self.enabled = False
        self.set_online(False)
        bot_header.SET_ONLINE_THREAD_INSTANCE = None

    def run(self):
        self.v("Starting loop")

        while self.enabled:
            online = self.set_online(True)
            self.v("Set online: %s" % online)
            sleep(self.interval)
            pass
        self.print("Stopping thread...")









