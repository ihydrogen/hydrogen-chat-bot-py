import json
import os,sys,inspect

import requests
import vk

from long_pool.long_pool_event import LongPoolEvent
# set current path to root of project
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

import bot_header
import vk_api
import random
import threading
import time

from console import bot_console

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
        bot_header.LONG_POOL_THREAD_INSTANCE = None

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
        self.name = "[::LP-%s] " %  (self.account.first_last())

    # Custom print func that prints username
    def print(self, text, from_module=None):
        if from_module is None:
            print('[::LP] [%s] %s' % (self.account.first_last(), text))
        else:
            name = from_module.replace("modules.", "")
            import mpm_manager
            mname = mpm_manager.ModuleManager().get_module_from_file(name)
            if mname is not None:
                print('[::LP:%s] [%s] %s' % (mname.module_name, self.account.first_last(), text))
            else:
                print(text)

    def v(self, text):
        bot_header.v('[::LP] [%s] %s' % (self.account.first_last(), text))

    def run(self):
        print('[::LP] run()')
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
            # Cancel response processing if thread is stopped
            if self.enabled:
                # Processing VK updates
                if "updates" in resp:
                    self.on_response(resp['updates'])
                    # Updating LongPoolServerObject
                    self.lpso.ts = resp['ts']
                else:
                    print("cant find updates, restartin' thread")
                    console = bot_console.Console()
                    console.run("longpool restart")
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


