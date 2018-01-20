import inspect
import os
import random
import sys
from time import sleep

import mpm_manager
from utils import config_file

FORMAT_PID_STR = "longpool format peer id"

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from vk_api.api import get_api
from vk_api.api import Message
from vk_api.api import api_request
from vk_api.api import vapi

import bot_header

# THIS METHOD EXECUTING WHEN USER SENT A MESSAGE TO YOU
# calling from main()
def on_message_received(message, lpt):
    e = message.extra
    # Getting list of modules
    manager = mpm_manager.ModuleManager()
    modules = manager.get_modules()

    # Exec each modules and get result
    for module in modules:
        result = module.execute_module(message, lpt)
        if result is not None:
            return result

    pass

# entry point of MESSAGE_SEND event of long pool server
# calling from long_pool_event.py
def main(resp, lp_thread_ins):
    #
    # Getting message from response
    message = Message()
    message = Message.from_long_pool(message, resp)
    #

    if message.is_out():
        bot_header.LP_MESSAGES_RECEIVED += 1
    else:
        bot_header.LP_MESSAGES_SENT += 1

    # Printing message to std out
    if message.is_loopback():
        sep = "<->"
    elif message.is_out():
        sep = "->"
    else:
        sep = "<-"

    fpid = False
    fpid = config_file.get_field(FORMAT_PID_STR) != "0"

    if fpid:
        u = vapi("users.get", "user_ids=%s" % message.pid)[0]
        lp_thread_ins.print("%s [%s]: %s" % (sep, "%s %s" % (u["first_name"], u["last_name"]), message.body))
    else:
        lp_thread_ins.print("%s [%s]: %s" % (sep, str(message.pid), message.body))

    #

    response_to_user = on_message_received(message, lp_thread_ins)
    if response_to_user is not None:
        send_response(lp_thread_ins, message, response_to_user)


def send_response(lp_thread_ins, message, response_to_user):
    # send response to vk_api user
    # getting api instance
    api = get_api(lpt=lp_thread_ins)
    # looking at config file
    make_typing = config_file.has("typing")
    # checking typing filed in config file
    if make_typing:
        read_message_before_typing = config_file.has("read before typing")
        ###
        # sets speed of typing (in seconds)
        # from time
        typing_speedf = config_file.get_field("typing speed from")
        # to time
        typing_speedt = config_file.get_field("typing speed to")
        # e.g: from 1 sec to 5 sec
        ###
        # don;t use random. use only typing_speedt
        static_typing = config_file.has("typing static")

        # getting random typing speed (by default)
        typing_time = random.randint(1, 5)
        # checking that typing_speedf and typing_speedt is number
        if str.isnumeric(typing_speedf) and str.isnumeric(typing_speedt):
            # checking static typing is enabled
            if not static_typing:
                # get random typing time
                typing_time = random.randint(int(typing_speedf), int(typing_speedt))
            else:
                # get time only from typing_speedt
                typing_time = int(typing_speedt)

        if read_message_before_typing:
            result = api_request(api, "messages.markAsRead", "message_ids=%s, peer_id=%s" % (message.mid, message.pid))
            lp_thread_ins.v("Marking '%s' as read... %s" % (message.body, str(result)))

        # sleep each 5 secs until end of typing duration
        def typing(typing_time, stime=1):
            i = 0
            while i < typing_time:
                result = api_request(api, "messages.setActivity", "peer_id=%s, type='typing'" % message.pid)
                # result = api.messages.setActivity(peer_id=message.pid, type="typing")
                lp_thread_ins.v("making typing request for %s... %s" % (message.body, str(result)))
                sleep(stime)
                i += stime

        typing(typing_time)

    # let's fucking do this!
    # sending message to peer
    random_id = random.randint(0, 100000)
    peer_id = message.pid
    messaget = response_to_user
    msendresult = api_request(api, "messages.send", "random_id=%s, peer_id=%s, message=\"%s\"" % (
        random_id, peer_id, messaget
    ))
    lp_thread_ins.v("sending %s to %s... %s" % (response_to_user, message.body, str(msendresult)))
