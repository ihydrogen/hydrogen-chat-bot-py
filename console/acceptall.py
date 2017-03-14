import bot_header
from vk_api.api import api_request
from vk_api.api import get_api
from time import sleep

def main(C):
	print("this is horosho")
	# get API instance 
	api = get_api(account=bot_header.CURRENT_ACCOUNT)
	# get followers
	fws = api_request(api, "users.getFollowers", "")
	fwitems = fws['items']
	for item in fwitems:
		add(item, api)		

def add(item, api):
	try:
		sleep(3)
#		print("Trying 2 add %s ..." % item)
		addf = api_request(api, "friends.add", "user_id=%s" % item)
		print("Adding %s ... %s" % (item, str(addf)))
	except Exception as e:
		err = str(e)
		if "per second" in err.lower():
			sleep(1.5)
			add(item, api)
