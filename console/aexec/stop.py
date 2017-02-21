import bot_header


def main(c):
    if bot_header.AUTO_EXEC_THREAD_INSTANCE is not None:
        bot_header.AUTO_EXEC_THREAD_INSTANCE.stop()
    else:
        raise Exception("Nothing to stop")