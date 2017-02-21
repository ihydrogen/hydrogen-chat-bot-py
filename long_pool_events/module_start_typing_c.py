import bot_header
from vk_api.api import User
from vk_api.api import api_request
from vk_api.api import get_api


# execute when user started typing.
def main(message, lpt):
    # get id of user
    typing_id = message[1]
    # get user from VK API by id
    user = User.from_json(api_request(get_api(lpt=lpt), "users.get", "user_ids=%s" % typing_id)[0])
    # print some message to inform user that someone started typing:)
    bot_header.v("%s started typing..." % user.first_last())
