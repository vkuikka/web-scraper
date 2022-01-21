#!/usr/bin/python3
from PIL import Image, ImageFilter, ImageEnhance
from sklearn.preprocessing import normalize, MinMaxScaler
import pickle
import math
import numpy as np

def rgb(minimum, maximum, value):
	minimum, maximum = float(minimum), float(maximum)
	ratio = 2 * (value - minimum) / (maximum - minimum)
	b = int(max(0, 255*(1 - ratio)))
	r = int(max(0, 255*(ratio - 1)))
	g = 255 - b - r
	if b == 255:
		b = 0
	return int(r), int(g), int(b)

def main():
	file = open("cache", "rb")
	data = file.read()
	data = pickle.loads(data)

	image_size = 2000
	arr = np.zeros(shape=(image_size, image_size), dtype=int)
	lat_floor = 53
	lon_floor = 15
	# lat_floor = -10
	# lon_floor = -30

	lon_min = 999999999
	lat_min = 999999999
	lon_max = 0
	lat_max = 0
	for each in data:
		d = data[each]
		if d.lat == 0.0 or d.lon == 0.0:
			continue
		if d.lat < lat_floor or d.lon < lon_floor:
			continue
		lon = d.lon - lon_floor
		lat = d.lat - lat_floor
		lon_min = min(lon_min, lon)
		lon_max = max(lon_max, lon)
		lat_min = min(lat_min, lon)
		lat_max = max(lat_max, lon)
	print('longtitude: ' + str(lon_min) + ' - ' + str(lon_max))
	print('lattitude:  ' + str(lat_min) + ' - ' + str(lat_max))
	print('')
	total = 0
	used = 0
	skipped = 0
	under_limit = 0

	for each in data:
		total += 1
		d = data[each]
		if d.lat == 0.0 or d.lon == 0.0:
			skipped += 1
			continue
		if d.lat < lat_floor or d.lon < lon_floor:
			skipped += 1
			continue
		lon = d.lon - lon_floor
		lat = d.lat - lat_floor
		lon = (lon - lon_min) / (lon_max - lon_min)
		lat = (lat - lat_min) / (lat_max - lat_min)
		lat = 1 - lat
		lon *= image_size
		lat *= image_size

		# Pixel brightness corresponds to the price per square meter
		if lon < image_size and lat < image_size and lon > 0 and lat > 0 and d.area != None and float(d.area) > 10 and d.price != None and d.price > 0:
			if d.price < 50000:
				under_limit += 1
			else:
				new = int(float(d.price) / float(d.area))
				if new > arr[int(lat)][int(lon)]:
					arr[int(lat)][int(lon)] = new
					used += 1
				else:
					skipped += 1

		# # Brightness corresponds to the age of the house. Prefer older and cap at 1950
		# if lon < image_size and lat < image_size and lon > 0 and lat > 0 and d.year != None and int(float(d.year)) > 0:
		# 	if (int(float(d.year)) > arr[int(lat)][int(lon)] and arr[int(lat)][int(lon)] != 0):
		# 		under_limit += 1
		# 	else:
		# 		if int(float(d.year)) < 1950:
		# 			arr[int(lat)][int(lon)] = 1950
		# 		else:
		# 			arr[int(lat)][int(lon)] = int(float(d.year))
		# 		used += 1

		# if lon < image_size and lat < image_size and lon > 0 and lat > 0 and d.area != None and float(d.area) > 10 and d.price != None and d.price > 0:
		# 	if lon < image_size and lat < image_size and lon > 0 and lat > 0 and d.year != None and int(float(d.year)) > 0:
		# 		if d.price < 50000 or int(float(d.year)) < 1800:
		# 			under_limit += 1
		# 		else:
		# 			arr[int(lat)][int(lon)] = int(float(d.price) / float(d.area) / float(d.year))
		# 			used += 1
		# 	else:
		# 		skipped += 1
	print("under limit: " + str(under_limit))
	print("skipped: " + str(skipped))
	print("used: " + str(used))
	print("total: " + str(total))
	print('')

	minval = np.amin(arr[np.nonzero(arr)])
	maxval = np.amax(arr[np.nonzero(arr)])
	print(str(minval) + " - " + str(maxval))
	for each in arr:
		each[each == 0] = minval
	minval = np.amin(arr)
	maxval = np.amax(arr)
	print(str(minval) + " - " + str(maxval))
		
	scaler = MinMaxScaler()
	arr = scaler.fit_transform(arr)

	minval = np.amin(arr)
	maxval = np.amax(arr)
	print(str(minval) + " - " + str(maxval))
	arr *= 255

	# # Colored image takes more time to generate
	# pxl = []
	# for i in range(image_size):
	# 	pxl.append([])
	# 	for j in range(image_size):
	# 		pxl[i].append(rgb(0, 255, arr[i][j]))
	# im2 = Image.new(mode="RGB", size=(image_size, image_size))
	# im2.putdata([pxl[x][y] for x in range(image_size) for y in range(image_size)])
	# im2.show()
	# im2 = im2.filter(ImageFilter.GaussianBlur(0.9))
	# enhancer = ImageEnhance.Brightness(im2)
	# im2 = enhancer.enhance(2)
	# im2.show()

	im = Image.fromarray(np.uint8(arr), 'L')
	im.show()
	# im.save('price_no_blur.png')
	im = im.filter(ImageFilter.GaussianBlur(0.9))
	enhancer = ImageEnhance.Brightness(im)
	im = enhancer.enhance(2)
	im.show()
	# im.save('img/img.png')

if __name__ == "__main__":
    main()
