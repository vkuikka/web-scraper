#!/usr/bin/python3
import pickle
import sys

def main():
	if len(sys.argv) != 2:
		print("give cache file as argument")
		return
	file = open(sys.argv[1], "rb")
	data = file.read()
	x = pickle.loads(data)
	try:
		for each in x:
			print(each)
			print(x[each].__dict__)
			print("")
	except:
		print(x.__dict__)

if __name__ == "__main__":
    main()
