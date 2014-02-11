#!/usr/bin/python

import sys
import os
from PIL import Image

lensModel=0xa434
shutterSpeed=0x829a
aperture=0x829d
iso=0x8827
focalLen=0x920a
fullFrameFocalLen=0xa405
isoSensType=0x8830
exposureProg=0x8822
exposureMode=0xa402
metering=0x9207
whiteBal=0xa403
shotTime=0x9003

#eComp=0x9204
#lensMake=0xa433

if len(sys.argv) < 2:
	print("No directories specified")
	sys.exit()

for i in range(1, len(sys.argv)):
	if not os.path.exists(sys.argv[i]):
		print("Invalid directory: " + sys.argv[i])
		sys.exit()

print("All folders found")

exif = []
for i in range(1, len(sys.argv)):
	print("Processing " + sys.argv[i])
	#print(os.listdir(sys.argv[i]))
	files = [f for f in os.listdir(sys.argv[i]) if os.path.isfile(sys.argv[i] + "/" + f)]
	#print(files)
	if len(files) < 1:
		print("No image files found in " + sys.argv[i])
		sys.exit()
	for file in files:
		name, extension = os.path.splitext(file)
		if extension == '.jpg' or extension == '.jpeg':
			img = Image.open(sys.argv[i] + "/" + file)
			exif.append([name, img._getexif()])

file = open(sys.argv[i] + "/exifData.csv", "w")

file.write("Filename,Lens,ShutterSpeed,Aperture,ISO,FocalLength,FullFrameFocalLength,ISOSensType,ExposureProg,ExposureMode,Metering,WhiteBalance,Time\n")
for image in exif:
	file.write(image[0] + ",")
	file.write(image[1][lensModel] + ",")
	file.write(str(image[1][shutterSpeed][0]) + "/" + str(image[1][shutterSpeed][1]) + ",")
	ap = float(image[1][aperture][0]) / image[1][aperture][1]
	file.write(str(ap) + ",")
	file.write(str(image[1][iso]) + ",")
	fl = image[1][focalLen][0] / image[1][focalLen][1]
	file.write(str(fl) + ",")
	file.write(str(image[1][fullFrameFocalLen]) + ",")
	file.write(str(image[1][isoSensType]) + ",")
	file.write(str(image[1][exposureProg]) + ",")
	file.write(str(image[1][exposureMode]) + ",")
	file.write(str(image[1][metering]) + ",")
	file.write(str(image[1][whiteBal]) + ",")
	file.write(str(image[1][shotTime]) + "\n")

# TEST CODE ONLY ###############################################################
# This code will print out every single exif field between 0x0 and 0xfe59
# To see which fields are used, run "grep -iv none" on the output file; the results are the used fields
#for i in range(0x00, 0xfe59):
#	file.write(hex(i) + "\t" + str(exif[0].get(i, "None")) + "\n")
#print("First set done")
################################################################################

file.close()
