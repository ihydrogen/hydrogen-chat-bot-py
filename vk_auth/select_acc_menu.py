
from utils import config_file


def select_acc(list, num):
    if num is not '-1' and str.isnumeric(num):
        val = int(num)
        if len(list) < val:
            print("This account is not exists")
            exit(1)

        acc = list[val]
        return acc
    else:
        for acc in list:
            print("[%d] %s %s" % (list.index(acc), acc.first_name, acc.last_name))
        cla = config_file.get_field("last acc")
        last = None
        if cla is not None:
            if str.isnumeric(cla):
                last = int(cla)
                if last > len(list) - 1:
                    last = None
                    config_file.set_field("last acc", "None")
                else:
                    print("Default is %s (Just press ENTER)" % list[last].first_last())
        id = input("Select Account: ")
        while not str.isnumeric(id):
            if not id and last is not None:
                id = last
                return list[id]

            id = input("Select Account: ")
            pass

        id = int(id)

        if id == 999:
            return None

        if len(list) <= id:
            print("This account is not exists")
            exit(1)

        acc = list[id]
        config_file.set_field("last acc", str(id))
        return acc

    pass