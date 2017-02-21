# Prints id of current acc to console
import bot_header


def main(cmd):
    acc = bot_header.CURRENT_ACCOUNT
    if acc is not None:
        print("Current account id: %s" % acc.user_id)