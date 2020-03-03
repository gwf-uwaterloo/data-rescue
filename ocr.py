import os
from PIL import Image
#import pytesseract
import argparse
import cv2
import csv
from get_stations import get_station_names
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR")
ap.add_argument("-o", "--output", required=True,
	help="path to output of OCR")
ap.add_argument("-f", "--filename", required=False,
	help="name of the csv file")
args = vars(ap.parse_args())

# def get_first_number_index(content, i):
# 	#print(content[i],i)
# 	while i < len(content):
# 		if len(content[i]) <= 6:
# 			i += 1
# 			continue
# 		temp = content[i].split(' ')
# 		flag = 0
# 		if(temp[0] == "1"):
# 			#print("Next: " + str(i))
# 			return i
# 		for j in range(len(temp[0])):
# 			if temp[0][j] == "0" or temp[0][j] == "2" or temp[0][j] == "3" or temp[0][j] == "4" or temp[0][j] == "5" or temp[0][j] == "6" or temp[0][j] == "7" or temp[0][j] == "8" or temp[0][j] == "9":
# 				flag = 2
# 				break
# 			if temp[0][j] == "1" and flag == 1:
# 				flag = 2
# 				break
# 			if temp[0][j] == "1":
# 				flag = 1
# 		if flag != 2:
# 			return i
# 		i += 1
# 	return -1


filename = args["output"] + ".txt"
command = "tesseract " + args["image"] + " " + args["output"] + " -c tessedit_char_whitelist=0123456789.-\")\"\"(\" -c tosp_min_sane_kn_sp=5 --oem 0 --psm 6"
os.system(command)



data = []
pg_no = -1
with open(filename) as f:
	content = f.readlines()
	counter = 1
	ind = 0
	i = 0
	try:
		pg_no = content[i]
	except:
		pg_no = -1
	flag = 0
	while i < len(content):
		if len(content[i]) == 0:
			i += 1
			continue
		temp = content[i].split()
		if temp[0] == "1":
			flag = 1
			break
		elif temp[0] == "2":
			i -= 1
			break
		elif temp[0] == "3":
			i -= 2
		 	break
		
		i += 1
	if i== len(content):
		i = 7
	if i != -1:
		
		data_temp = []
		while i<len(content):
			if(len(content[i]) == 0) :
				i += 1
				continue
			temp = content[i].split()

			string = ""
			cnt = 0
			for num in temp:
				string_ind = ""
				if len(num) == 1 and (num[0] == "."):
					continue;
				for char in num:
					if char != "-":
						string_ind += char
				if counter == 32 and cnt == 0:
					string_ind = "Sum"
				elif counter == 33 and cnt == 0:
					string_ind = "Mean"
				string = string + string_ind + ","
				cnt += 1
			data_temp.append(string[:-1])
			counter += 1
			i+=1
			if counter == 34:
				data.append(data_temp)
				data_temp = []
				counter = 1
				ind += 1
				flag = 0
				cnt = 0
				while i < len(content):
					if len(content[i]) == 0:
						i += 1
						continue
					temp = content[i].split()
					try:
						if temp[0] == "1":
							flag = 1
							break
						elif temp[0] == "2":
							i -= 1
							break
						elif temp[0] == "3":
							i -= 2
							break
						elif temp[0] == "4":
							i -= 3
							break
						i += 1
						cnt += 1
					except:
						break
				if i == len(content):
					i = i - cnt + 7

			

stations_list = get_station_names(args["image"], args["output"], data)
with open("results/" + args["filename"] + '.csv', mode='a') as ocr_out:
    ocr_writer = csv.writer(ocr_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    input_name = args["image"]

    try:
    	file_name = input_name.split('.')[0].split("/")[-1]
    	pg_no = file_name
    except:
	    pg_no = "Page N/A"
    ocr_writer.writerow([pg_no])
    ocr_writer.writerow(["\n"])
    for dt, station in zip(data, stations_list):
    	ocr_writer.writerow(station.split(','))
    	for line in dt:
    		ocr_writer.writerow(line.split(','))
    	ocr_writer.writerow(["\n"])
