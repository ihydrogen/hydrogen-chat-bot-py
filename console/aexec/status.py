import bot_header

def main(c):
    if bot_header.AUTO_EXEC_THREAD_INSTANCE is not None:
        print("Alive: %s rules loaded, interval: %s" % (len(bot_header.AUTO_EXEC_THREAD_INSTANCE.aexec_rules), bot_header.AUTO_EXEC_THREAD_INSTANCE.interval))
    else:
        print("Dead. Run it using 'aexec start'")