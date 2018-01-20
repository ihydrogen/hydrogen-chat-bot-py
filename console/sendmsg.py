import bot_header
from vk_api.api import get_api
from vk_api.api import api_request


CNAME = "sendmsg"

def main(command):
	args = command.replace(CNAME, "").strip().split(" ", maxsplit=1)
	#print(args)
	if len(args) == 2:
		idstr = args[0]
		if str.isnumeric(idstr):
			idn = int(idstr)
			msg = args[1]
			api = get_api(account=bot_header.CURRENT_ACCOUNT)
			r = api_request(api, "messages.send", "peer_id=%s, message=\"%s\"" % (idn, msg))
			return ""
	else:
		raise Exception("Usage: sendmsg 'ID' 'MESSAGE'")

