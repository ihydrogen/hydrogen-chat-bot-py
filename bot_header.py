# Import some modules
import requests, json

global CURRENT_ACCOUNT, LP_REQUESTS_DONE, LP_MESSAGES_RECEIVED, LP_MESSAGES_SENT, \
    LOG, API_REQUESTS,\
    FAILED_API_REQUESTS,\
    LONG_POOL_THREAD_INSTANCE,\
    SET_ONLINE_THREAD_INSTANCE,\
    verbose

VERBOSE = "---V---"
WARNING = "---W---"

def w(text):
    print("%s%s" % (WARNING, text))

def v(text):
    if verbose:
        print(text)