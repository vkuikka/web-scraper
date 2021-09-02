#!/usr/bin/python3

class	data_block:
	seller_name = ""
	address = ""
	publish_time = 0	# unix epoch
	price = 0	# euro
	area = 0	# m^2
	year = 0
	lon = 0
	lat = 0

	def	__init__(self, line):
		if line == "":
			return
		try:
			self.address = line.split('"')[0]
		except:
			self.address = None
		try:
			price_line = line.split('Price":')
			self.price = int(float(price_line[1].split(",")[0]))
		except:
			self.price = None
		try:
			self.seller_name = line.split('name":"')[1].split('",')[0]
		except:
			self.seller_name = "private"
		try:
			self.year = int(float(line.split('constructionFinishedYear":')[1].split(',')[0]))
		except:
			self.year = None
		try:
			self.area = float(line.split('area":')[1].split(',')[0])
		except:
			self.area = None
		try:
			self.publish_time = int(float(line.split('publishingTime":')[1].split(',')[0]))
		except:
			self.publish_time = None

	def	set_coordinates(self, location):
		self.lat = location.latitude
		self.lon = location.longitude