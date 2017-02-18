import json
import os,sys,inspect

import requests

from long_pool.long_pool_event import LongPoolEvent
# set current path to root of project
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import bot_header
import vk
import random
import threading
import time

class LongPoolThread(threading.Thread):
    # Account that will be used for Messages.GetLongPoolServer
    # .. Method on VK API
    account = None
    enabled = True
    timeout = 20

    # Stop sending requests to longpool server
    def stop(self):
        self.print("Stopping Longpool thread...")
        self.enabled = False

    class LongPoolServerObject:
        key = None
        ts = None
        server = None
        timeout = 20

        def from_json(d):
            s = LongPoolThread.LongPoolServerObject()
            s.__dict__.update(d)
            return s

        def __init__(self, k = '', t = '', s = '', T = ''):
            self.key = k
            self.ts = t
            self.server = s
            self.timeout = T


        def format(self):
            mode = 64 + 32 + 8 + 2
            # return "https://" + self.server + "?act=a_check&key=" + self.key +\
            #        "&ts=" + self.ts + "&wait=" + self.timeout + \
            #     "&mode=%d&version=1" % mode

            return 'https://%s?act=a_check&key=%s&ts=%s&wait=%d&mode=%d&version=1' %(\
                self.server, self.key, self.ts, int(self.timeout), mode
            )


    lpso = LongPoolServerObject()
    exitFlag = 0

    def __init__(self, account):
        self.account = account
        threading.Thread.__init__(self)
        self.threadID = random.randint(0, 1000)
        self.name = "[LP-%s] " %  (self.account.first_last())

    # Custom print func that prints username
    def print(self, text):
        print('[LP] [%s] %s' % (self.account.first_last(), text))

    def run(self):
        print('[LP] run()')
        self.print("Getting LongPoolServerObject...")
        # Getting VK API Instance...
        api = vk.API(vk.Session(access_token=self.account.token))
        # Getting VK Long pool server
        lpserver = api.messages.getLongPollServer()
        # Getting LongPoolServerObject from response
        self.lpso = LongPoolThread.LongPoolServerObject.from_json(lpserver)
        self.lpso.timeout = self.timeout
        self.print("OK")

        while self.enabled:
            # Getting server request url
            rurl = self.lpso.format()
            # Getting Response
            resp = json.loads(requests.get(rurl).text)
            # Processing VK updates
            self.on_response(resp['updates'])
            # Updating LongPoolServerObject
            self.lpso.ts = resp['ts']
            pass

    def on_response(self, resp):
        bot_header.LP_REQUESTS_DONE+=1
        #[[4, 197360, 8209, 2000000010, 1487278352, 'Топовые', 'ок',
        #  {'from': '177651854'}], [80, 2, 0], [7, 2000000010, 197359]]

        for event in resp:
            evid = event[0]
            # Load events logic in ./long_pool_events/
            LongPoolEvent.process(evid, event, self)
        pass


