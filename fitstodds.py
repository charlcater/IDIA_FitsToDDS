# Slice .fits datacube to a series of .tifs
# and write list of files to a text file

from astropy.io import fits
import glob
import os
import os.path
from PIL import Image
import subprocess
import sys


def slice(fitsfile):

    print('\n')
    print('+ + + + + FITS cube to DDS utility + + + + +\n')
    print('converting {}'.format(fitsfile))

    # filename = 'testimg.fits'
    head_tail = os.path.split(fitsfile)
    saveas = head_tail[1].replace('.fits', '')
    subdirectory = head_tail[0] + '/' + saveas + '_sliced'

    os.makedirs(subdirectory, exist_ok=True)

    print('... saving fits cube to TIFF planes')

    with fits.open(fitsfile) as hdulist:
        scidata = hdulist[0].data
        print('Fits file shape: {}'.format(scidata.shape))

        if len(scidata.shape) > 3:
            print('Fits file has more than 3 axes: {}'.format(len(scidata.shape)))
            #exit()

            for i in range(scidata.shape[0]):
                scidata = hdulist[0].data[i,:,:,:]

                for j in range(len(scidata[:])):
                    image_array = scidata[j, :, :]
                    im = Image.fromarray(image_array)
                    im = im.transpose(Image.FLIP_TOP_BOTTOM)  # correct for array flip

                    name = saveas + '_slice_' + str(j).zfill(3) + '_' + str(i) + '.tiff'
                    completeName = os.path.join(subdirectory, name)
                    im.save(completeName, format='tiff')

                    print('saving slice {} of {}'.format(j, len(scidata[:])-1), end="\r")

                print()
        
        else:
            for i in range(len(scidata[:])):
                image_array = scidata[i, :, :]
                im = Image.fromarray(image_array)
                im = im.transpose(Image.FLIP_TOP_BOTTOM)  # correct for array flip

                name = saveas + '_slice_' + str(i).zfill(3) + '.tiff'
                completeName = os.path.join(subdirectory, name)
                im.save(completeName, format='tiff')

                print('saving slice {} of {}'.format(i, len(scidata[:])-1), end="\r")
            
            print()

    # ------
    # write a list of all generated tiffs
    extension = '*.tiff'
    path = os.path.join(subdirectory, extension)

    listname = 'filelist.txt'
    fulllistname = os.path.join(subdirectory, listname)

    with open(fulllistname, 'w') as f:

        print('... writing file list {}'.format(fulllistname))

        files = glob.glob(path)

        filelist = []
        i = 0

        for file in files:
            filename = file.replace(subdirectory + '/', '')
            filelist.append(filename)
            i += 1

        filelist.sort()

        for filename in filelist:            
            f.write(filename)
            f.write('\r\n')

    # ------
    # assemble images into a 3D texture
    # feed to texassemble as 'texassemble volume -o testimg.dds -flist testimg_sliced/filelist.txt'

    print('... converting to DDS')
    saveasdds = fitsfile.replace('.fits', '.dds')

    try:
        convertDDS = subprocess.run(["texassemble volume -o {} -flist {}".format(saveasdds, fulllistname)], capture_output=False, check=False, shell=True)
        print('Shell output: {}\n'.format(convertDDS))

    except Exception as e:
        raise e

    if(convertDDS.returncode == 0):
            try:
                # delete the imtermediate tiff files
                delTIFF = subprocess.run(["rm {}/*.tiff".format(subdirectory)], capture_output=False, check=False, shell=True)
                print('Shell output: {}\n'.format(delTIFF))

            except Exception as e:
                raise e

            print('Output saved to {}'.format(saveasdds))
            print('Done')
    else:
        print('Conversion failed!')



if __name__ == '__main__':

    if len(sys.argv) < 2:
        print('Usage: python3 fitstodds.py <path/to/cube.fits>')
        exit(1)

    fitsfile = str(sys.argv[1])

    slice(fitsfile)
