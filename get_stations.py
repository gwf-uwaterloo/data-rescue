import cv2;
import numpy as np;
import argparse
import os
import subprocess
import PIL
from PIL import Image
import pytesseract
import matplotlib
from pytesseract import Output
from scipy import misc

def get_station_names(input_image, output, station_init):
      img = cv2.imread(input_image, 0);
      PILimg = Image.fromarray(img)
      old_height, old_width = PILimg.size
      #print("Pixels: " + str(PILimg.size[0]*PILimg.size[1]) + " " + str(PILimg.size[0]) + " " + str(PILimg.size[1]))
      h, w = img.shape[:2]
      kernel = np.ones((15,15),np.uint8)

      e = cv2.erode(img,kernel,iterations = 2)  
      d = cv2.dilate(e,kernel,iterations = 1)
      ret, th = cv2.threshold(d, 150, 255, cv2.THRESH_BINARY_INV)

      mask = np.zeros((h+2, w+2), np.uint8)
      cv2.floodFill(th, mask, (200,200), 255); # position = (200,200)
      out = cv2.bitwise_not(th)
      out= cv2.dilate(out,kernel,iterations = 3)
      _, cnt, h = cv2.findContours(out,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
      counter = 0
      min_area = -1
      table_stations = []
      stations = ""
      for i in range(len(cnt)):
                  area = cv2.contourArea(cnt[i])
                  if(area>100000):
                        print(area)
                        mask = np.zeros_like(img)
                        cv2.drawContours(mask, cnt, i, 255, -1)
                        x,y,w,h = cv2.boundingRect(cnt[i])
                        crop= img[y:h+y,x:w+x]
                        masked_img = cv2.bitwise_and(img, img, mask = mask)
                        masked_img[mask == 0] = 255
                        crop_left = img[y-200:y, x:w+x]
                        boxes = pytesseract.image_to_boxes(masked_img) # also include any config options you use

                        # draw the bounding boxes on the image
                        for b in boxes.splitlines():
                            b = b.split(' ')
                            masked_img = cv2.rectangle(masked_img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)
                        if counter == 0:
                          len_dict = []
                          max_count = 1
                          for j in range(20):
                            len_dict.append(0)
                          for j in station_init[len(station_init) - 1]:
                            len_dict[len(j.split(","))] += 1
                          for j in range(20):
                            if max_count < len_dict[j]:
                              max_count = len_dict[j]
                              length = j
                          #length = len(station_init[len(station_init)-1][len(station_init[len(station_init)-1])-1].split(","))
                        else:
                          len_dict = []
                          max_count = 1
                          for j in range(20):
                            len_dict.append(0)
                          for j in station_init[0]:
                            len_dict[len(j.split(","))] += 1
                          for j in range(20):
                            if max_count < len_dict[j]:
                              max_count = len_dict[j]
                              length = j
                          #length = len(station_init[len(station_init)-1][len(station_init[len(station_init)-1])-1].split(","))
                          #length = len(station_init[0][len(station_init[0])-1].split(","))
                        end = length + 1
                        if length < 8:
                          length = 10
                        width_cutoff = int(w/length)
                        
                        for i in range(1, end):
                            if i != 1:
                                start = (i-1)*width_cutoff - 50
                            else:
                              start = (i-1)*width_cutoff
                            s = crop_left[:, start: i*width_cutoff]
                            misc.imsave("temp/station"+str(i)+".tif", s)
                            #imageio.imwrite("temp/station"+str(i)+".tif", s)
                            extract_text_command = "tesseract " + "temp/station" + str(i) + ".tif temp/station_name -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-."
                            os.system(extract_text_command)

                            with open("temp/station_name.txt") as f:
                                content = f.readlines()
                                try:
                                  stations += content[0].strip() + ","
                                except:
                                  stations += "N/A," 

                        table_stations.append(stations)
                        stations = ""
                        counter += 1

      return table_stations[::-1]

                  #cv2.imshow('img', masked_img)
                  #cv2.waitKey(0)
                  #cv2.imwrite(args["outputDir"] + "/try" + str(counter) + ".png",masked_img)
                  #cv2.imwrite(args["outputDir"] + "/text" + str(counter) + ".tif",crop_left)
                  #cv2.imwrite(args["outputDir"] + "/numbers.tif",masked_img)
                  #img= PIL.Image.open(args["outputDir"] + "/text" + str(counter) + ".tif")
                  # PILimage = Image.fromarray(masked_img)
                  # #PILimage.resize((5961, 7452))
                  # #print("Pixels: " + str(PILimage.size[0]*PILimage.size[1]) + " " + str(PILimage.size[0]) + " " + str(PILimage.size[1]))

                  # PILimage.resize((PILimage.size[0],PILimage.size[1]), PIL.Image.ANTIALIAS)
                  # #img.save(args["outputDir"] + "/text" + str(counter) + ".png", dpi=(1200,1200))
                  # #size = 10000, 5000
                  # #im = Image.open(args["outputDir"] + "/numbers.png")
                  # #im_resized = im.resize(size, Image.ANTIALIAS)
                  # PILimage.save(args["outputDir"] + "/numbers.tif", dpi=(1200,1200))
                  # #matplotlib.image.imsave( args["outputDir"] + "/numbers.eps", crop)
                  # #cv2.imwrite(args["outputDir"] + "/numbers.tif",crop,[cv2.IMWRITE_JPEG_QUALITY, 100])
                  
                  # #extract_numbers_command = "tesseract " + args["outputDir"] + "/numbers.tif " + args["outputDir"] + "/temp -c tessedit_char_whitelist=0123456789. -c tosp_min_sane_kn_sp=10- --oem 0 --psm 6 --dpi 600 -l rus"
                  # extract_numbers_command = "tesseract " + args["outputDir"] + "/numbers.tif stdout -c tessedit_char_whitelist=0123456789.- -c tosp_min_sane_kn_sp=10 --oem 0 --psm 6"
                  # #proc = subprocess.check_output(['tesseract', args["outputDir"] + "/numbers.jpg", "stdout -c tessedit_char_whitelist=0123456789.- --oem 0 --psm 6"])
                  # #proc.wait()
                  # #print(proc)
                  # #print(extract_numbers_command)
                  # os.system(extract_numbers_command)
                  # #filename = args["outputDir"] + "/temp.txt"
                  # #with open(filename) as f:
                  # #  content = f.readlines()
                  # #  for i in range(2, len(content)):
                  # #      temp = content[i].split()
                  # #      print(temp)

                  # extract_text_command = "tesseract " + args["outputDir"] + "/text" + str(counter) + ".tif stdout -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-. -c tosp_min_sane_kn_sp=300 --oem 0 --psm 4"
                  # os.system(extract_text_command)
                  #tools = pyocr.get_available_tools()[0]
                  #text = pytesseract.image_to_boxes(Image.open(args["outputDir"] + "/numbers.tif"), config = '-c tessedit_char_whitelist=0123456789.- -c tosp_min_sane_kn_sp=10 --oem 0 --psm 4')
                  #print(text)
                  

#print("TEXT OUTPUT")

#os.system(extract_text_command)
