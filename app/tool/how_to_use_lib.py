import sys
# different directory.
sys.path.append("../../lib")
import lib
from lib.date import *

# same directory.
import lib_in_same_dir


print(lib.date.getYesterday())
print(getToday())
print(lib_in_same_dir.hello())