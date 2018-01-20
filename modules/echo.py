# Echo module
# Used for testing module system
# Sends back messages that starts with "echo "

###
# THIS PARAMS IS REQUIRED:
module_name = "ECHO Module"
module_version = "0.0"
module_author = "HydroGen"
###
# defines description of modules
module_description = "This is test module"
# defines entry point function of modules e.g. main() or modules() or tm() like this
module_entry = "echomain"

def echomain(msg, lpt):
        body = msg.body
        fo = body.split("+")[0]
        so = body.split("+")[1]
        ffo = int(fo)
        sso = int(so)
        return "Your result: %s" % (str(ffo + sso))
