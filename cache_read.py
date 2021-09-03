#!/usr/bin/python3
import pickle
import sys
import locale

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')

def	print_all(x, address_len, price_len, name_len):
	res_str = ''
	res_str += str(x.address)
	for i in range(1, address_len - len(str(x.address))):
		res_str += ' '
	res_str += str(x.year) + '\t'

	if x.price is not None:
		price = str(locale.currency(int(x.price), grouping=True))
		price = price[2:]
		price = price[:len(price) - 3]
		res_str += str(price) + ' €'
		for i in range(1, price_len - len(str(x.price))):
			res_str += ' '
	else:
		res_str += "None\t"

	if x.area is not None:
		res_str += str(int(float(x.area))) + ' m\u00b2\t'
	else:
		res_str += "None\t"
	res_str += str(x.seller_name) + '\t'
	# for i in range(1, name_len - len(str(x.seller_name))):
	# 	res_str += ' '
	print(res_str)

def	print_flags(x, address_len, price_len, name_len, flag):
	res_str = ''
	if 'd' in flag:
		res_str += str(x.address)
		for i in range(1, address_len - len(str(x.address))):
			res_str += ' '
	if 'y' in flag:
		res_str += str(x.year) + '\t'
	if 'p' in flag:
		if x.price is not None:
			price = str(locale.currency(int(x.price), grouping=True))
			price = price[2:]
			price = price[:len(price) - 3]
			res_str += str(price) + ' €'
			for i in range(1, price_len - len(str(x.price))):
				res_str += ' '
		else:
			res_str += "None\t"
	if 'r' in flag:
		if x.area is not None:
			res_str += str(int(float(x.area))) + ' m\u00b2\t'
		else:
			res_str += "None\t"
	if 'n' in flag:
		res_str += str(x.seller_name) + '\t'
		# for i in range(1, name_len - len(str(x.seller_name))):
		# 	res_str += ' '
	print(res_str)

def main():
	flag = ""
	if len(sys.argv) < 2:
		print("give cache file as argument")
		return
	elif len(sys.argv) == 3:
		flag = sys.argv[2]
	file = open(sys.argv[1], "rb").read()
	x = pickle.loads(file)
	try:
		address_len = 0
		name_len = 0
		price_len = 0
		for each in x:
			if len(str(x[each].address)) > address_len:
				address_len = len(x[each].address)
			if len(str(x[each].seller_name)) > name_len:
				name_len = len(str(x[each].seller_name))
			if x[each].price is not None:
				price = str(locale.currency(int(x[each].price), grouping=True))
				price = price[2:]
				price = price[:len(price) - 3]
				if len(str(price)) > price_len:
					price_len = len(str(price))
		if address_len > 70:
			address_len = 70
		for each in x:
			if flag == '-dump':
				print(x[each].__dict__)
			elif flag == '':
				print_all(x[each], address_len, price_len, name_len)
			else:
				print_flags(x[each], address_len, price_len, name_len, flag)

	except:
		print(x.__dict__)
		print("\nDUMPED")

if __name__ == "__main__":
    main()
