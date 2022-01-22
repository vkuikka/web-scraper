# Web scraper
Scrapes and visualizes data from [Etuovi](https://www.etuovi.com/) using [Geopy](https://geopy.readthedocs.io/en/stable/)

## How to use:
- ```cache_init.py``` creates a cache file that will be storing all your queried data.
- ```query.py``` adds to the cache file with more data found from etuovi and queried from geopy.
- ```image.py``` creates images from the data saved in cache file.
- You need to make a file called header.txt and add the header needed for etuovi.com request.

## Optional:
- ```cache_read.py``` reads and outputs all the data saved in cache file.
	- Without a flag it will output all data.
	- ```-d``` flag will add address to output.
	- ```-y``` flag will add year of construction to output.
	- ```-p``` flag will add price to output.
	- ```-r``` flag will add area to output in square meters.
	- ```-n``` flag will add seller name to output. (Usually the real estate agency)

## Notes:
Image.py needs some work. The data could be visualized a lot better and it could have options other than the ones in the comments I added.

## Example:
In the images below price per square meter is visualized in whole Finland and Helsinki area.   
(blue = cheap, red = expensive)

<img src="/img/price_colors.png" width="100%"/>

<img src="/img/helsinki.png" width="100%"/>
