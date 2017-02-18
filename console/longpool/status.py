import bot_header

def main(c):
    if bot_header.LONG_POOL_THREAD_INSTANCE is not None:
        print("Alive: %s requests sent, timeout: %s" % (bot_header.LP_REQUESTS_DONE, bot_header.LONG_POOL_THREAD_INSTANCE.timeout))
    else:
        print("Dead. Run it using 'longpool start'")