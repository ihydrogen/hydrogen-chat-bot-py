#!/usr/bin/python3
from termcolor import colored
import time
from optparse import OptionParser

import bot_header
import vk_auth.account_manager
import vk_auth.select_acc_menu
import vk_auth.vk_app
from console import bot_console
from utils import print_hook
from vk_auth.bot_auth import authorize

"""
THIS IS ENTRY FILE OF PROJECT
./bot.py -> bot_entry()
"""

# Name of keys of options[]
ACC_NUM_KEY = 'account-num'
LOG_FILE_KEY = 'log-file'
LONG_POOL_KEY = 'start-long-pool'
UNAME_KEY = 'username'
PASSWD_KEY = 'password'
V_KEY = 'verbose'
LONG_POOL_TIME_OUT_KEY = 'long-pool-timeout'
# Disable date printing
DD_KEY = 'disable-date'
AUTH_APP_KEY = 'auth-app'

apply_date_to_output = True
log = None
timeout = 20
verbose = False
bot_console_instance = None

auth_app = None

def get_options(parser):
    parser.add_option('-a', '--auth-app', dest=AUTH_APP_KEY,
                      help='Use specific auth application (APPLE_IPHONE, WIN, ANDROID)',
                      default="WIN"
                      )

    parser.add_option('-t', '--long-pool-timeout', dest=LONG_POOL_TIME_OUT_KEY,
                      help='set timeout of long-pool request (20 is recommenced)',
                      default=20
                      )

    parser.add_option('-n', '--acc-number', dest=ACC_NUM_KEY,
                      help='force set number of account',
                      default="-1"
                      )
    parser.add_option('-u', '--username', dest=UNAME_KEY,
                      help='force set auth username',
                      default=None
                      )
    parser.add_option('-p', '--password', dest=PASSWD_KEY,
                      help='force set auth password',
                      default=None
                      )
    parser.add_option('-l', '--log-file', dest=LOG_FILE_KEY,
                      help='set filename of log',
                      default=''
                      )
    parser.add_option("-L", "--long-pool", dest=LONG_POOL_KEY,
                      help='enable Long Pool',
                      default='False', action='store_true')

    parser.add_option("-v", "--verbose", dest=V_KEY,
                      help='verbose output',
                      default=False, action='store_true')

    parser.add_option("-D", "--date-disable", dest=DD_KEY,
                      help='Disable pasting current date and time in stdout',
                      default='True', action='store_false')

    pass


def apply_options(options):

    global CONF_FILE,\
        num,\
        log,\
        apply_date_to_output,\
        password,\
        username,\
        timeout,\
        verbose,\
        auth_app

    num = options[ACC_NUM_KEY]
    log = options[LOG_FILE_KEY]
    apply_date_to_output = options[DD_KEY]
    password = options[PASSWD_KEY]
    username = options[UNAME_KEY]
    timeout = options[LONG_POOL_TIME_OUT_KEY]
    verbose = options[V_KEY]
    app_name = options[AUTH_APP_KEY]
    try:
        auth_app = vk_auth.vk_app.VKApp[app_name]
        bot_header.v("Using app %s" % app_name)
    except KeyError:
        bot_header.w("app %s not exists. Using WIN app" % app_name)
        auth_app = vk_auth.vk_app.VKApp.WIN
    pass


def create_console(acc):
    global bot_console_instance
    try:
        bot_console_instance = bot_console.Console()
        bot_console_instance.acc = acc
        bot_console_instance.acc_number = num
        bot_console_instance.run_looped()
    except Exception as e:
        print(e)
        create_console(acc)

    pass


def select(acc):
    bot_header.CURRENT_ACCOUNT = acc
    print("selected: " + acc.first_last())
    create_console(acc)
    pass


def start_long_pool(acc):
    import long_pool.long_pool
    bot_header.LONG_POOL_THREAD_INSTANCE = long_pool.long_pool.LongPoolThread(acc)
    bot_header.LONG_POOL_THREAD_INSTANCE.timeout = timeout
    bot_header.LONG_POOL_THREAD_INSTANCE.setDaemon(True)
    bot_header.LONG_POOL_THREAD_INSTANCE.start()



# main method
def bot_entry():

    bot_header.LP_MESSAGES_RECEIVED = 0
    bot_header.LP_MESSAGES_SENT = 0
    bot_header.LP_REQUESTS_DONE = 0
    bot_header.API_REQUESTS = 0
    bot_header.FAILED_API_REQUESTS = 0
    bot_header.AUTO_EXEC_THREAD_INSTANCE = None


    #enable print hook
    def MyHookOut(text):
        rtext = text

        if text.strip() and apply_date_to_output:
            rtext = '[%s] ' % time.strftime("%c") + text

        if not ">>" in rtext:
            if "[::" in rtext and not "[LOG]" in rtext:
                rtext = rtext.replace("[::", "[")
                bot_header.LOG.append(rtext)
                if log:
                    with open(log, 'at') as logf:
                        logf.write(rtext + "\n")

                if bot_console_instance is not None:
                    a = bot_console_instance.get_message()
                    #return 1, 1, ("\r" + rtext), "text"

        if rtext.__contains__(bot_header.WARNING):
            rtext = rtext.replace(bot_header.WARNING, "")
            rtext = colored(rtext, "yellow")
        return 1, 1, ("\r" + rtext), None

    phOut = print_hook.PrintHook()
    phOut.Start(MyHookOut)

    # create OptionParser instance
    parser = OptionParser()

    # get specified options for parser
    get_options(parser)

    # get options
    (options, args) = parser.parse_args()
    options = options.__dict__
    # apply options to vars
    apply_options(options)
    # get list of available accounts
    am = vk_auth.account_manager.AccountManager()
    list = am.get_account_list()

    # checking for isEmpty
    if len(list) > 0:
        # select menu
        if num == '999':
            auth()
        # Enter select acc menu
        account = vk_auth.select_acc_menu.select_acc(list, num)
        # if user entered 999, adding new acc
        if account is None:
            auth()
            # Enter select acc menu again
            account = vk_auth.select_acc_menu.select_acc(list, num)
        if options[LONG_POOL_KEY] == True:
            start_long_pool(account)
        select(account)

    else:
        # auth
        print("You need to Log In to your account")
        auth()

    # The selected account logic is executing in select()

   # phOut.Stop()


def auth():
    authorize(username=username, password=password, type=auth_app)


# Start program entry point if script is executing from command line
if __name__ == '__main__':
    bot_header.LOG = []
    bot_header.LONG_POOL_THREAD_INSTANCE = None
    bot_header.SET_ONLINE_THREAD_INSTANCE = None
    bot_header.verbose = verbose
    try:
        bot_entry()
    except (KeyboardInterrupt, SystemExit):
        print("Exit...")
        # if bot_header.LONG_POOL_THREAD_INSTANCE is not None:
        #     print("Disabling Long Pool Thread...")
        #     bot_header.LONG_POOL_THREAD_INSTANCE.enabled = False
        #     print("... OK")

