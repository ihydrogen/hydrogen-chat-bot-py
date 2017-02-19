import bot_header
from vk_api.set_online import OnlineThread

def main(cmd):
    print("Stopping thread...")
    bot_header.SET_ONLINE_THREAD_INSTANCE.stop()