#!/usr/bin/python

import sys
import os
from os.path import expanduser
from PIL import Image

# ExIF data hex offsets

field_names = ['cameraMake',
               'cameraModel',
               'lensModel',
               'shutterSpeed',
               'aperture',
               'iso',
               'focalLen',
               'fullFrameFocalLen',
               'isoSensType',
               'exposureProg',
               'exposureMode',
               'metering',
               'whiteBal',
               'shotTime']

hex_offsets = [0x010f,
               0x0110,
               0xa434,
               0x829a,
               0x829d,
               0x8827,
               0x920a,
               0xa405,
               0x8830,
               0x8822,
               0xa402,
               0x9207,
               0xa403,
               0x9003]

exif_fields = dict(zip(field_names, hex_offsets))

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

# Write csv to cross-platform Desktop folder (for now)
home = expanduser("~")
csvFile = os.path.join(home, 'Desktop', 'exifData.csv')

with open(csvFile, "w") as results_file:

    results_file.write("Filename,CameraMake,CameraModel,Lens,ShutterSpeed,Aperture,ISO,FocalLength,FullFrameFocalLength,ISOSensType,ExposureProg,ExposureMode,Metering,WhiteBalance,Time\n")

    for image in exif:

        # extract metadata from exif info
        data = image[1]

        cameraMake   = str(data[exif_fields['cameraMake']])
        cameraModel  = str(data[exif_fields['cameraModel']])
        exposureMode = str(data[exif_fields['exposureMode']])
        exposureProg = str(data[exif_fields['exposureProg']])
        ffFocalLen   = str(data[exif_fields['fullFrameFocalLen']])
        iso          = str(data[exif_fields['iso']])
        isoSensType  = str(data[exif_fields['isoSensType']])
        lensModel    = str(data[exif_fields['lensModel']])
        metering     = str(data[exif_fields['metering']])
        shotTime     = str(data[exif_fields['shotTime']])
        whileBalance = str(data[exif_fields['whileBal']])

        _shutterSpd  = data[exif_fields['shutterSpeed']]
        shutterSpeed = str(_shutterSpd[0]) + "/" + str(_shutterSpd[1])

        _ap          = data[exif_fields['aperture']]
        aperture     = str(float(_ap[0]) / _ap[1])

        _focalLen    = data[exif_fields['focalLen']]
        focalLength  = str(_focalLen[0] / _focalLen[1])

        # write metadata to new CSV row

        results_file.write(image[0] + ",")

        results_file.write(cameraMake + ",")
        results_file.write(cameraModel + ",")
        results_file.write(lensModel + ",")
        results_file.write(shutterSpeed + ",")
        results_file.write(aperture + ",")
        results_file.write(iso + ",")
        results_file.write(focalLength + ",")
        results_file.write(ffFocalLen + ",")
        results_file.write(isoSensType + ",")
        results_file.write(exposureProg + ",")
        results_file.write(exposureMode + ",")
        results_file.write(metering + ",")
        results_file.write(whiteBalance + ",")
        results_file.write(shotTime + ",")

# TEST CODE ONLY ###############################################################
# This code will print out every single exif field between 0x0 and 0xfe59
# To see which fields are used, run "grep -iv none" on the output file; the results are the used fields
#for i in range(0x00, 0xfe59):
#   file.write(hex(i) + "\t" + str(exif[0].get(i, "None")) + "\n")
#print("First set done")
################################################################################
