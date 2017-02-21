###
# THIS PARAMS IS REQUIRED:
module_name = "Test Module"
module_version = "1.0"
module_author = "HydroGen"
###

# defines description of modules
module_description = "This is test module"
# defines entry point function of modules e.g. main() or modules() or tm() like this
module_entry = "tm"
# Note: ENTRY POINT MUST HAVE (message, lpt) arguments
# @message - message object parsed from long-pool thread
# @lpt - long-pool thread

def tm(message, lpt):
    # checking that message is not out and his body is equal to 'ping'
    if not message.is_out() and message.body.lower() == 'ping':
        # send 'OK' to peer
        return "OK"

