import json as j

from utils import config_file
from vk_api.api import Account

# Name for key of acc list
ACCOUNT_LIST = "account list"


class AccountManager:

    def __init__(self, location=config_file.CONF_FILE):
        self.location = location

    # location of file with users
    location = config_file.CONF_FILE

    def get_account_list_raw(self, accs):
        if accs == None:
            return []
        accs = accs.replace("'", '"')
        result = []
        json = j.loads(accs)

        for object in json:
            result.append(j.loads(str(object).replace("'", '"'), object_hook=Account.from_json))

        return result

    def add_account_raw(self, acc, list):
        for _acc in list:
            list[list.index(_acc)] = _acc.__dict__
        list.append(acc.__dict__)
        jsonchik = j.dumps(list)
        return jsonchik

    def get_account_list(self):
        config_file.init_field(ACCOUNT_LIST, '[]', self.location)
        accs = config_file.get_field(ACCOUNT_LIST, self.location)
        return self.get_account_list_raw(accs)

    def add_account(self, acc):
        list = self.get_account_list()
        config_file.set_field(ACCOUNT_LIST, self.add_account_raw(acc, list), self.location)

