import sys
path = "E:/tweet"
if path not in sys.path:
	sys.path.insert(0,path)
from run import app as application