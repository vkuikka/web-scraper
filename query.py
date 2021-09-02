#!/usr/bin/python3
from data_block import data_block
from bcolor import bcol
import requests
from geopy.geocoders import Nominatim
import numpy as np
import pickle
import time

def parse(line, geolocator, saved_data, since_last):

	block = data_block(line)

	if block.address not in saved_data:
		while time.time() - since_last < 1.25:
			time.sleep(0.01)
		address = block.address.split(" ")
		address = address[:-2] + address[-1:]
		address = " ".join(address)
		location = geolocator.geocode(address)
		if location != None:
			block.set_coordinates(location)
		saved_data[block.address] = block
		print(bcol.OKBLUE + 'adding: ' + bcol.ENDC + block.address + " " + str(block.lon) + ", " + str(block.lat))
	else:
		print(bcol.OKGREEN + 'skipping: ' + bcol.ENDC + block.address)
	return float(time.time())

def main():
	curlheader = {
		# add
	}
	url = 'https://www.etuovi.com/myytavat-asunnot?haku=M1718964015&sivu='

	file = open("cache", "rb")
	saved_data = pickle.loads(file.read())
	file.close()
	geolocator = Nominatim(user_agent="what")
	startpage = 0
	pages = 2000

	for i in range(startpage, pages):
		req = requests.get(url + str(i), curlheader)
		splitted = req.text.split("location\":\"")
		del splitted[0]
		time_last = 0
		for line in splitted:
			time_last = float(parse(line, geolocator, saved_data, time_last))
		
		print(bcol.WARNING + 'saving cache ' + str(i) + " / " + str(pages))
		file = open("cache", "wb")
		serial_data = pickle.dumps(saved_data)
		file.write(serial_data)
		file.close()

if __name__ == "__main__":
    main()

	# lat = location.latitude - 60
	# lon = location.longitude - 20
	# lat = int(lat * 1000)
	# lon = int(lon * 1000)
	# if lon < image_size and lat < image_size:
	# 	arr[lon][lat] += price
	# 	print (str(lon) + ", " + str(lat) + " = " + str(price))
	# else:
	# 	return "ARR TOO SMALL" + block.address

	# norma = normalize(arr, 0, 255)
	# im = Image.fromarray(np.uint8(norma), 'L')
	# im.save('test.png')


	# url = 'https://www.etuovi.com/myytavat-asunnot?haku=M1718964015&sivu=1' \
	# -H 'authority: www.etuovi.com' \
	# -H 'sec-ch-ua: "Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"' \
	# -H 'accept: */*' \
	# -H 'sec-ch-ua-mobile: ?0' \
	# -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36' \
	# -H 'sec-fetch-site: same-origin' \
	# -H 'sec-fetch-mode: no-cors' \
	# -H 'sec-fetch-dest: empty' \
	# -H 'accept-language: fi-FI,fi;q=0.9,en;q=0.8' \
	# -H 'cookie: XSRF-TOKEN=8176bb17-5e22-46b8-bf6b-f52326fb8a77; uuidc=c579df1d-14fb-4bf5-87f0-834257614bfa; sammio-bsid=8d021e25-ea4e-4c22-877e-c403c33a6e7b; ALMA_DATA_PRIVACY_SETTINGS_1=eyJwZXJtaXNzaW9ucyI6eyJjb29raWVzIjp0cnVlLCJnZW8iOlsiVEFSR0VURURfQ09OVEVOVCIsIkFEUyIsIldFQVRIRVIiXSwiZG1wIjp7fX19; sammio-init-time=2021-08-30T15:52:48.782Z' \
	# -H 'if-none-match: W/"58f0e-IWMYFeAs6KjfgMByXvbZCAB3ue4"' \
	# --compressed ;
	# curl 'https://www.etuovi.com/static/icons-v1/manifest.json' \
	# -H 'sec-ch-ua: "Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"' \
	# -H 'Accept: */*' \
	# -H 'Referer: https://www.etuovi.com/myytavat-asunnot?haku=M1718964015&sivu=1' \
	# -H 'sec-ch-ua-mobile: ?0' \
	# -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36' \
	# --compressed

