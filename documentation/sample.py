from map_reduce import map_reduce
import struct
import math
import requests
import sys
import tempfile

out = sys.stdout
data = ''
with tempfile.NamedTemporaryFile() as temp:
    sys.stdout = temp
    help(sys)
    data = temp.read()
sys.stdout = out
print(data)
