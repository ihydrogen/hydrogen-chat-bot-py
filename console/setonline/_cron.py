import bot
import bot_header
from vk_api.set_online import OnlineThread


def main(cmd):
    t = OnlineThread(bot_header.LONG_POOL_THREAD_INSTANCE)
    r = t.set_online(1)
    print("Setting online... %s" % r)
