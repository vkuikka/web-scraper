#!/usr/bin/python3
from data_block import data_block
from bcolor import bcol
import requests
from geopy.geocoders import Nominatim
import pickle
import time
from threading import Thread

def parse(line, geolocator, saved_data, last_time):

	block = data_block(line)

	if block.address not in saved_data:
		while time.time() - last_time < 1.4:
			time.sleep(0.01)
		geo_address = block.address.split(" ")
		geo_address = geo_address[:-2] + geo_address[-1:]
		geo_address = " ".join(geo_address)
		try:
			location = geolocator.geocode(str(geo_address))
		except KeyboardInterrupt:
			exit()
		except:
			print(bcol.FAIL + "geocode error with address: " + str(geo_address) + bcol.ENDC)
			return float(time.time())
		if location != None:
			block.set_coordinates(location)
		print(bcol.OKBLUE + 'adding new: ' + bcol.ENDC + block.address + " " + str(block.lon) + ", " + str(block.lat))
		saved_data[block.address] = block
		return float(time.time())
	else:
		if block.address in saved_data:
			block.lon = saved_data[block.address].lon
			block.lat = saved_data[block.address].lat
		saved_data[block.address] = block
		print(bcol.OKGREEN + 'skipping: ' + bcol.ENDC + block.address)
	return last_time

def	save_cache(saved_data, path):
	f = open(path, "wb")
	serial_data = pickle.dumps(saved_data)
	f.write(serial_data)
	f.close()


def	page_amount(url, curlheader):
	req = requests.get(url + '1', curlheader)
	splitted = req.text.split('button\">')
	first = []
	for line in splitted:
		add = line.split('<')[0]
		if add != '':
			first.append(add)
	return int(first[-1:][0])

def main():
	url = 'https://www.etuovi.com/myytavat-asunnot?haku=M1718964015&sivu='
	curlheader = open("header.txt", "r").read()
	file = open("cache", "rb")
	saved_data = pickle.loads(file.read())
	file.close()
	geolocator = Nominatim(user_agent="etuovi_mapmaker")
	startpage = 1
	pages = page_amount(url, curlheader) + 1
	for i in range(startpage, pages):
		reponse = requests.get(url + str(i), curlheader)
		splitted = reponse.text.split("location\":\"")
		del splitted[0]
		time_last = 0
		for line in splitted:
			time_last = float(parse(line, geolocator, saved_data, time_last))
		print(bcol.WARNING + 'saving cache ' + str(i) + " / " + str(pages))
		t = Thread(target=save_cache, args=(saved_data, "cache"))
		t.start()
		t.join()

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		exit()
