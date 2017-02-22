import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir)

from utils.config_file import *

# Create config, write some data and read it.
CONF_FILE = "test.conf"
# Create config
touch(CONF_FILE)

# Set field 'test filed' in file to 'test'
set_field("test field", "test", CONF_FILE)

# Read previous result
test = get_field("test field", CONF_FILE)

# Check it!
assert test == "test"