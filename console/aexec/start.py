import bot
import bot_header
from autoexec import autoexec_thread

def main(c):
    print("Staring AutoExec Thread...")
    bot_header.AUTO_EXEC_THREAD_INSTANCE = autoexec_thread.AutoexecThread()
    bot_header.AUTO_EXEC_THREAD_INSTANCE.setDaemon(True)
    bot_header.AUTO_EXEC_THREAD_INSTANCE.start()

