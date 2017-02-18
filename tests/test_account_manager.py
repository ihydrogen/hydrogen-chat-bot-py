import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from vk_auth.account_manager import *

am = AccountManager()

raw_acc = Account()
raw_acc.first_name = "vasya"
raw_acc.last_name = "pupkin"
raw_acc.token = "..."
raw_acc.user_id = 123456

empty_list = am.get_account_list_raw("[]")
assert len(empty_list) == 0

am.add_account_raw(raw_acc, empty_list)

list_with_user = am.get_account_list_raw(str(empty_list))
assert list_with_user[0].first_name == raw_acc.first_name