import bot
import bot_header
import vk_auth
from console import bot_console


def main(cmd):
    if not "chacc" in cmd:
        return None
    print("Exiting all threads...")
    # Before changing accs, close all threads
    con = bot_console.Console()
    if bot_header.LONG_POOL_THREAD_INSTANCE is not None:
        con.run("longpool stop")
    if bot_header.SET_ONLINE_THREAD_INSTANCE is not None:
        con.run("setonline stop")
    bot_header.CURRENT_ACCOUNT = None
    # Restart it
    bot.bot_entry()
