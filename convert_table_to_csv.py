import os
##"1986", "1987", "1988", "1989", "1990", 
#years = ["1986", "1991"]
#directory = "/Volumes/Seagate_Backup_Plus_Drive/Solar_Radiation_and_Radiation_Balance_Data/"
directory = "TIFF/"
temp_dir = directory
for year in range(1980, 1992):
	directory = os.path.join(temp_dir, str(year))
	for month in os.listdir(directory):
		if month == ".DS_Store":
			continue
		print(month, year)
		new_path = os.path.join(directory,month)
		#new_path = os.path.join(new_path, "TIFF")
		new_path = os.path.join(new_path, "data")
		#print(new_path)
		for _ in os.walk(new_path):
			files = _
		#print(files[2])
		for filenames in files[2]:
			if "tif" in filenames:
				print(month,filenames)
				file_path = os.path.join(new_path, filenames)
				command = "python ocr.py -i " + file_path + " -o populate_num -f " + month + "_" + str(year)
					#print(command)
				os.system(command)
