#!/usr/bin/python

import sys
import os
from os.path import expanduser
from PIL import Image
import argparse

def generatePieChart(chartName, chartDataArray):
    '''generatePieChart will generate and display a pie chart using the provided data and title'''
    # Generate pie chart
    from pylab import figure, axes, pie, title, show

    # Get total number of data points
    total = len(chartDataArray)
    slices = []

    # Generate list of data "slices" and the quantity associated with each
    for item in chartDataArray:
        isNew = True
        for element in slices:
            if element[0] == item:
                element[1] += 1
                isNew = False
                break
        if isNew:
            slices.append([item, 1])

    # make a square figure and axes
    figure(1, figsize=(6,6))
    ax = axes([0.1, 0.1, 0.8, 0.8])

    # The slices will be ordered and plotted counter-clockwise.
    labels = [ str(x[0]) for x in slices ]
    fracs = [ 1.0 * x[1] / total for x in slices ]
    explode = []
    for x in range(len(slices)):
        explode.append(0.05)

    # Create and show the pie chart
    pie(fracs, labels=labels, explode=explode, autopct='%1.1f%%', shadow=True, startangle=90)
    title(chartName, bbox={'facecolor':'0.8', 'pad':5})
    show()

# Parse supplied arguments
# Parser expects mandatory path to images folder, optional arg specifying pie chart to be created
parser = argparse.ArgumentParser()
parser.add_argument("path", type=str, help="Path to the folder of pictures to be processed")
parser.add_argument("-p", "--piechart", type=str, choices=['camera', 'exposureMode', 'exposureProg', 'focalLengthFF', 'iso', 'lensModel', 'metering', 'shutterSpeed', 'aperture', 'focalLength'], help="Draw a pie chart using the data from the specified metric")
parser.add_argument("--destination", "-d", type=str, help='Creates a CSV of the relevant ExIF data at the specified location')
args = parser.parse_args()

# Make sure the specified path exists
if not os.path.exists(args.path):
    print('Invalid directory: ' + args.path)
    sys.exit(1)

# Create path for the csv file
home = expanduser('~')
csvFile = ''
destFolder = ''
# Make sure the destination path exists, if specified
if args.destination:
    destFolder = os.path.join(home, args.destination)
    csvFile = os.path.join(destFolder, 'exifData')
    if not os.path.exists(destFolder):
        print('Invalid destination directory: ' + destFolder)
        sys.exit(2)

# Don't overwrite existing files, so append a count to end of the file name
i = 0
initLen = len(csvFile)
baseCSVFile = csvFile
while os.path.exists(csvFile + '.csv'):
    i += 1
    csvFile = baseCSVFile[:initLen] + str(i)
csvFile += '.csv'

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

exif = list()
badFiles = list()
directory = args.path
print('Processing ' + directory)

dir_list = map(lambda x: os.path.join(directory, x), os.listdir(directory))
files = filter(lambda x: os.path.isfile(x), dir_list)

# Make sure that we have at least one image to process
if len(files) < 1:
    print('No image files found in ' + directory)
    sys.exit(1)

for file_path in files:
    name, extension = os.path.splitext(file_path)
    if extension.lower() in ('.jpg', '.jpeg'):
        try:
                img = Image.open(os.path.join(directory, file_path))
                exif.append([name, img._getexif()])
        except:
            print "File unable to be processed: ", name + extension
            badFiles.append(name + extension)
if len(badFiles) > 0:
    print "Errors in %s files: " % (str(len(badFiles)))
for bf in badFiles:
    print "\t" + bf

# Init metadata arrays
filenameArray = []
cameraMakeArray = []
cameraModelArray = []
exposureModeArray = []
exposureProgArray = []
ffFocalLenArray = []
isoArray = []
isoSensTypeArray = []
lensModelArray = []
meteringArray = []
shotTimeArray = []
whiteBalanceArray = []
shutterSpeedArray = []
apertureArray = []
focalLengthArray = []

# Assemble exif data into arrays
for filename, data in exif:

    if data is None:
        data = dict()

    filenameArray.append(filename)
    cameraMakeArray.append(str(data.get(exif_fields['cameraMake'])))
    cameraModelArray.append(str(data.get(exif_fields['cameraModel'])))
    exposureModeArray.append(str(data.get(exif_fields['exposureMode'])))
    exposureProgArray.append(str(data.get(exif_fields['exposureProg'])))
    ffFocalLenArray.append(str(data.get(exif_fields['fullFrameFocalLen'])))
    isoArray.append(str(data.get(exif_fields['iso'])))
    isoSensTypeArray.append(str(data.get(exif_fields['isoSensType'])))
    lensModelArray.append(str(data.get(exif_fields['lensModel'])))
    meteringArray.append(str(data.get(exif_fields['metering'])))
    shotTimeArray.append(str(data.get(exif_fields['shotTime'])))
    whiteBalanceArray.append(str(data.get(exif_fields['whiteBal'])))

    # Do some special data handling for a few fields
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

    shutterSpeedArray.append(shutterSpeed)
    apertureArray.append(aperture)
    focalLengthArray.append(focalLength)





# Write csv to destination if specified
if args.destination:
    with open(csvFile, 'w') as results_file:

        # Write column headers to CSV
        results_file.write('Filename,CameraMake,CameraModel,Lens,ShutterSpeed,Aperture,ISO,FocalLength,FullFrameFocalLength,ISOSensType,ExposureProg,ExposureMode,Metering,WhiteBalance,Time\n')

        for i in range(len(cameraMakeArray)):
            # write metadata to new CSV row
            write = lambda x: results_file.write(x + ',')

            write(filenameArray[i])
            write(cameraMakeArray[i])
            write(cameraModelArray[i])
            write(lensModelArray[i])
            write(shutterSpeedArray[i])
            write(apertureArray[i])
            write(isoArray[i])
            write(focalLengthArray[i])
            write(ffFocalLenArray[i])
            write(isoSensTypeArray[i])
            write(exposureProgArray[i])
            write(exposureModeArray[i])
            write(meteringArray[i])
            write(whiteBalanceArray[i])
            write(shotTimeArray[i])

            results_file.write('\n')

if args.piechart:
    pc = args.piechart
    chartInfo = []
    # Switch on pie chart data set
    if pc == 'camera':
        chartInfo = ['Camera Model', cameraModelArray]
    elif pc == 'exposureMode':
        chartInfo = ['Exposure Mode', exposureModeArray]
    elif pc == 'exposureProg':
        chartInfo = ['Exposure Program', exposureProgArray]
    elif pc == 'focalLengthFF':
        chartInfo = ['Full Frame Focal Length', ffFocalLenArray]
    elif pc == 'iso':
        chartInfo = ['ISO', isoArray]
    elif pc == 'lensModel':
        chartInfo = ['Lens Model', lensModelArray]
    elif pc == 'metering':
        chartInfo = ['Metering', meteringArray]
    elif pc == 'shutterSpeed':
        chartInfo = ['Shutter Speed', shutterSpeedArray]
    elif pc == 'aperture':
        chartInfo = ['Aperture', apertureArray]
    elif pc == 'focalLength':
        chartInfo = ['Focal Length', focalLengthArray]
    else:
        print "Invalid pie chart specified; valid values: camera, exposureMode, exposureProg, focalLengthFF, iso, lensModel, metering, shutterSpeed, aperture, focalLength"
        sys.exit(-1)

    # Draw pie chart
    generatePieChart(chartInfo[0], chartInfo[1])

# TEST CODE ONLY ###############################################################
# This code will print out every single exif field between 0x0 and 0xfe59
# To see which fields are used, run 'grep -iv none' on the output file; the results are the used fields
#for i in range(0x00, 0xfe59):
#   file.write(hex(i) + '\t' + str(exif[0].get(i, 'None')) + '\n')
#print('First set done')
################################################################################
