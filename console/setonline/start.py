import bot_header
from vk_api.set_online import OnlineThread

def main(cmd):
    print("Starting thread...")
    bot_header.SET_ONLINE_THREAD_INSTANCE = OnlineThread(account=bot_header.CURRENT_ACCOUNT, lpt=bot_header.LONG_POOL_THREAD_INSTANCE)
    bot_header.SET_ONLINE_THREAD_INSTANCE.setDaemon(True)
    bot_header.SET_ONLINE_THREAD_INSTANCE.start()