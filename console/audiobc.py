import bot_header
from vk_api.api import get_api
from vk_api.api import api_request

CNAME = "audiobc"


def main(command):
    args = command.replace(CNAME, "").strip()
    msg = args
    if not msg:
        raise Exception("Usage: audiobc 'OID_AID'")
    api = get_api(account=bot_header.CURRENT_ACCOUNT)
    r = api_request(api, "audio.setBroadcast", "audio=\"%s\"" % (msg))
    return r

