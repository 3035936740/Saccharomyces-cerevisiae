from os import path
import sys
from sc_config import TEST_MODE, INIT_MESSAGE

print(INIT_MESSAGE)

if TEST_MODE:
    local_dir = '/'.join(path.dirname(path.abspath(__file__)).replace('\\', '/').split('/')[:-1])
else:
    local_dir = path.dirname(path.abspath(sys.executable)).replace('\\', '/')