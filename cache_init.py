#!/usr/bin/python3
from data_block import data_block
from bcolor import bcol
import pickle

def main():
	if input(bcol.WARNING + "Reset cache? " + bcol.ENDC) == 'y':
		file = open("cache", "wb")
		d = {}
		for i in range(0, 1):
			test = data_block("")
			test.address = "address_" + str(i)
			test.price = 0
			test.lon = 0
			test.lat = 0
			d["key_" + str(i)] = test
		serial_data = pickle.dumps(d)
		file.write(serial_data)
	else:
		print(bcol.OKGREEN + "cancelled")

if __name__ == "__main__":
    main()
