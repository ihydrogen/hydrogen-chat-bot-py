import json, utils.config_file, autoexec.autoexec

AUTOEXEC = "autoexec"


class AutoexecRulesManager:

    def get_all_rules(self):
        result = []

        f = utils.config_file.get_field("autoexec")
        if not f:
            return result

        json_arr = json.loads(f)

        for rule in json_arr:
            result.append(autoexec.autoexec.AutoexecRule.from_json(rule).__dict__)

        return result

    def add_rule(self, rule):
        if self.get_by_id(rule.id) is not None:
            self.replace(rule.id, rule)
            return 0

        if type(rule) is not autoexec.autoexec.AutoexecRule:
            raise TypeError("value must be instance if AutoexecRule")

        rules = self.get_all_rules()
        rules.append(rule.__dict__)
        _json = json.dumps(rules)
        utils.config_file.set_field(AUTOEXEC, _json)

    def get_by_id(self, id):
        rules = self.get_all_rules()
        for rule in rules:
            if rule['id'] == id:
                return rule

    def remove(self, id):
        rule = self.get_by_id(id)
        if rule is None:
            raise Exception("No such rule")
        rules = self.get_all_rules()
        rules.remove(rule)
        _json = json.dumps(rules)
        utils.config_file.set_field(AUTOEXEC, _json)

    def replace(self, id, rule):
        self.remove(id)
        self.add_rule(rule)