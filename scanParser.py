
#takes in a string, chops off start and end tags, and splits it into data
#TODO: make sure string starts with S, ends with E and isnt 2 commands long
def scanParser(scanString):
	scanString = scanString[2:-2]
	scan = scanString.split(' ')
	for i,each in enumerate(scan):
		scan[i] = int(each)
	print(scan)
	return (scan)
	
# Example usage:
print(scanParser("S 22 -40 13 -45 15 E"))
print(scanParser("S -12 -40 13 -45 15 E"))



