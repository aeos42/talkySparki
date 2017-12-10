from sparkiConnection import sparkiConnection

import time




sparkiOne = sparkiConnection("/dev/cu.ArcBotics-DevB", 9600)

while True:

	print(sparkiOne.receiveCommand())

