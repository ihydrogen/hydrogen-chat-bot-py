import bot_header


def main(c):
    if bot_header.LONG_POOL_THREAD_INSTANCE is not None:
        bot_header.LONG_POOL_THREAD_INSTANCE.stop()
    else:
        raise Exception("Nothing to stop")