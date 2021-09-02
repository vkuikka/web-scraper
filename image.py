#!/usr/bin/python3
from PIL import Image, ImageFilter, ImageEnhance
from sklearn.preprocessing import normalize, MinMaxScaler
import pickle
import numpy as np

def rgb(minimum, maximum, value):
	minimum, maximum = float(minimum), float(maximum)
	ratio = 2 * (value - minimum) / (maximum - minimum)
	b = int(max(0, 255*(1 - ratio)))
	r = int(max(0, 255*(ratio - 1)))
	g = 255 - b - r
	return r, g, b

def main():
	file = open("cache", "rb")
	data = file.read()
	data = pickle.loads(data)

	image_size = 8000
	arr = np.zeros(shape=(image_size, image_size), dtype=int)
	skipped = 0
	lat_floor = 57
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
		if lon < lon_min:
			lon_min = lon
		if lon > lon_max:
			lon_max = lon
		if lat < lat_min:
			lat_min = lat
		if lat > lat_max:
			lat_max = lat
	print(lon_min)
	print(lat_min)
	print(lon_max)
	print(lat_max)

	for each in data:
		d = data[each]
		if d.lat == 0.0 or d.lon == 0.0:
			continue
		if d.lat < lat_floor or d.lon < lon_floor:
			continue
		lon = d.lon - lon_floor
		lat = d.lat - lat_floor
		lon = (lon - lon_min) / (lon_max - lon_min)
		lat = (lat - lat_min) / (lat_max - lat_min)
		lat = 1 - lat
		lon *= image_size
		lat *= image_size

		if lon < image_size and lat < image_size and lon > 10 and lat > 10 and d.price != None and d.price > 0 and d.price < 1000000000:
			arr[int(lat)][int(lon)] = int(float(d.price))
		# if lon < image_size and lat < image_size and lon > 10 and lat > 10 and d.year != None and int(float(d.year)) > 0:
		# 	arr[int(lat)][int(lon)] = int(float(d.year))
			# print(str(d.lon) + ", " + str(d.lat) + " p: " + str(d.price))
		else:
			print("ARR TOO SMALL: " + d.address + " " + str(lon)  + ", " + str(lat))
			skipped += 1

	print("skipped " + str(skipped))

	# norm = np.linalg.norm(arr[np.nonzero(arr)])
	# arr = arr[np.nonzero(arr)] / norm * 255
	# arr = normalize(arr, norm='max')

	minval = np.amin(arr[np.nonzero(arr)])
	for each in arr:
		each[each == 0] = minval
		
	scaler = MinMaxScaler()
	arr = scaler.fit_transform(arr)


	arr *= 255;
	# pxl = []
	# for i in range(image_size):
	# 	pxl.append([])
	# 	for j in range(image_size):
	# 		pxl[i].append(rgb(0, 255, arr[i][j]))
	# im2 = Image.new(mode="RGB", size=(image_size, image_size))
	# im2.putdata([pxl[x][y] for x in range(image_size) for y in range(image_size)])
	# im2.show()

	im = Image.fromarray(np.uint8(arr), 'L')
	im.show()
	# im.save('price_no_blur.png')

	blurred = im.filter(ImageFilter.GaussianBlur(2))
	im = blurred

	enhancer = ImageEnhance.Brightness(im)

	factor = 5
	bright = enhancer.enhance(factor)
	bright.show()
	# bright.save('img/price_blurred.png')

if __name__ == "__main__":
    main()


	# norma = normalize(arr, 0, 255)
	# im = Image.fromarray(np.uint8(norma), 'L')
	# im.save('test.png')
