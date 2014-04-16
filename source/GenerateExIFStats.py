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
    print('No directories specified')
    sys.exit()

for directory in sys.argv[1:]:
    if not os.path.exists(directory):
        print('Invalid directory: ' + directory)
        sys.exit()

print('All folders found')

exif = list()
for directory in sys.argv[1:]:
    print('Processing ' + directory)

    dir_list = map(lambda x: os.path.join(directory, x), os.listdir(directory))
    files = filter(lambda x: os.path.isfile(x), dir_list)

    if len(files) < 1:
        print('No image files found in ' + directory)
        sys.exit()

    for file_path in files:
        name, extension = os.path.splitext(file_path)
        if extension in ('.jpg', '.JPG', '.jpeg', '.JPEG'):
            img = Image.open(os.path.join(directory, file_path))
            exif.append([name, img._getexif()])

# Write csv to cross-platform Desktop folder (for now)
home = expanduser('~')
csvFile = os.path.join(home, 'Desktop', 'exifData.csv')

with open(csvFile, 'w') as results_file:

    results_file.write('Filename,CameraMake,CameraModel,Lens,ShutterSpeed,Aperture,ISO,FocalLength,FullFrameFocalLength,ISOSensType,ExposureProg,ExposureMode,Metering,WhiteBalance,Time\n')

    for filename, data in exif:

        if data is None:
            data = dict()

        # extract metadata from exif info
        cameraMake   = str(data.get(exif_fields['cameraMake']))
        cameraModel  = str(data.get(exif_fields['cameraModel']))
        exposureMode = str(data.get(exif_fields['exposureMode']))
        exposureProg = str(data.get(exif_fields['exposureProg']))
        ffFocalLen   = str(data.get(exif_fields['fullFrameFocalLen']))
        iso          = str(data.get(exif_fields['iso']))
        isoSensType  = str(data.get(exif_fields['isoSensType']))
        lensModel    = str(data.get(exif_fields['lensModel']))
        metering     = str(data.get(exif_fields['metering']))
        shotTime     = str(data.get(exif_fields['shotTime']))
        whiteBalance = str(data.get(exif_fields['whiteBal']))

        _shutterSpd = data.get(exif_fields['shutterSpeed'])
        if _shutterSpd is not None:
            shutterSpeed = str(_shutterSpd[0]) + '/' + str(_shutterSpd[1])
        else:
            shutterSpeed = ''

        _ap = data.get(exif_fields['aperture'])
        if _ap is not None:
            aperture = str(float(_ap[0]) / _ap[1])
        else:
            aperture = ''

        _focalLen = data.get(exif_fields['focalLen'])
        if _focalLen is not None:
            focalLength = str(_focalLen[0] / _focalLen[1])
        else:
            focalLength = ''

        # write metadata to new CSV row

        results_file.write(filename + ',')

        results_file.write(cameraMake + ',')
        results_file.write(cameraModel + ',')
        results_file.write(lensModel + ',')
        results_file.write(shutterSpeed + ',')
        results_file.write(aperture + ',')
        results_file.write(iso + ',')
        results_file.write(focalLength + ',')
        results_file.write(ffFocalLen + ',')
        results_file.write(isoSensType + ',')
        results_file.write(exposureProg + ',')
        results_file.write(exposureMode + ',')
        results_file.write(metering + ',')
        results_file.write(whiteBalance + ',')
        results_file.write(shotTime + ',')
        results_file.write('\n')

# TEST CODE ONLY ###############################################################
# This code will print out every single exif field between 0x0 and 0xfe59
# To see which fields are used, run 'grep -iv none' on the output file; the results are the used fields
#for i in range(0x00, 0xfe59):
#   file.write(hex(i) + '\t' + str(exif[0].get(i, 'None')) + '\n')
#print('First set done')
################################################################################
