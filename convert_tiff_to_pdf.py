import img2pdf
import os
from PIL import Image 

directory = "lat_lon_1992"
files_list = []
for file in os.listdir(directory):
	if "tif" not in file:
		continue
	files_list.append(directory + "/" + file)

files_list.sort()
print(files_list)

with open('lat_lon.pdf', 'a') as f:
		#image = Image.open("")
	pdf_bytes = img2pdf.convert(files_list)  
		#image.close()
	f.write(pdf_bytes)