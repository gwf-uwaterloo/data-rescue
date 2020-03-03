This is the repo for converting pdf tabular data into a machine readable (csv) format.

ocr.py ---> The main file for converting numbers and station names of a pdf page into csv file.


get_stations.py ----> Used in ocr.py to convert station names into machine readable text using image segmentation and tesseract.


convert_table_to_csv.py ----> A wrapper file to convert pdf files of all the years available to csv. It iterates over all the files and for each one calls the ocr.py to convert that page's data into csv format. It is used by search.py file to search the data for a particular station.


search.py ------> This file is used to get data for all the years available for a particular station and save the data into csv file for different years.


reformat_data.py ------> This file converts the data generated from search.py into the required format i.e. (location, id, date, data).


convert_tiff_to_pdf.py -------> Convert multiple tiff images to a single pdf file.