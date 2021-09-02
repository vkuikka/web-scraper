#!/usr/bin/python3
import pickle

def main():
	file = open("cache", "rb")
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
