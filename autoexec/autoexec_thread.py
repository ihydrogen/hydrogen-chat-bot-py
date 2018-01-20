from threading import Thread
from time import sleep
from utils import time_utils

import bot_header
from autoexec.autoexec_rules_manager import AutoexecRulesManager
from autoexec.autoexec import AutoexecRule
from autoexec.autoexec_action_type import AutoexecActionType

class AutoexecThread(Thread):
    aexec_rules = []
    enabled = True
    interval = 1
    exec_py_code = False
    mgr = AutoexecRulesManager()

    def stop(self):
        self.print("Stopping AutoExec thread...")
        self.enabled = False
        bot_header.AUTO_EXEC_THREAD_INSTANCE = None


    def print(self, text):
        print("[::AEXEC] %s" % text)

    def v(self, text):
        bot_header.v("[::AEXEC] %s" % text)

    def update_rules_list(self, q=False):
        if not q:
            self.print("Updating rules list...")
        self.aexec_rules = self.mgr.get_all_rules()


    def __init__(self, interval='1s', exec_py_code=False):
        super().__init__()
        self.interval = time_utils.parse_time(interval)
        self.exec_py_code = exec_py_code


    def run(self):
        self.v("run()")
        self.print("Getting rules...")
        while self.enabled:
            for rule in self.aexec_rules:
                rule = AutoexecRule.from_json(rule)

                if rule.ticks == None:
                    rule.ticks = 0

                if rule.time_when != None and rule.ticks >= rule.time_when:
                    self.exec_rule(rule)
                    self.mgr.remove(rule.id)

                elif rule.time_each != None and rule.ticks >= rule.time_each:
                    self.exec_rule(rule)
                    rule.ticks = 0
                    self.mgr.replace(rule.id, rule)
                else:
                    rule.ticks += self.interval
                    self.mgr.replace(rule.id, rule)

            sleep(self.interval)
            self.update_rules_list(q=True)

    def exec_rule(self, rule):
        try:
            print("Executing rule #%s" % rule.id)
            if rule.action is not None:
                if rule.action == AutoexecActionType.ACTION_HC_CONSOLE:
                    if rule.action_value is not None:
                        from console import bot_console
                        bot_console.Console().run(rule.action_value)
                    else:
                        print("Bad rule #%s (No action value)")
            else:
                print("Bad rule #%s (No action)")
            pass
        except Exception as e:
            print(e)
            pass
