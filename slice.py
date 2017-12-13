# Slice .fits datacube to a series of .tifs
# and write list of files to a text file


def slice():
    from astropy.io import fits
    import glob
    import os
    from PIL import Image


    filename = 'testimg.fits'
    saveas = filename.replace('.fits', '')
    subdirectory = saveas + '_sliced'

    os.makedirs(subdirectory, exist_ok=True)

    with fits.open(filename) as hdulist:
        scidata = hdulist[0].data
        print('Fits file shape: {}'.format(scidata.shape))

        # shape of the data will probably change for differently generated fits
        for i in range(len(scidata[:])):
            image_array = scidata[i, :, :]
            im = Image.fromarray(image_array)
            im = im.transpose(Image.FLIP_TOP_BOTTOM)  # correct for array flip

            name = saveas + 'slice_' + str(i).zfill(3) + '.tiff'
            completeName = os.path.join(subdirectory, name)
            im.save(completeName, format='tiff')

            # # print('saving slice {}'.format(i))

    # write a list of all generated tiffs
    extension = '*.tiff'
    path = os.path.join(subdirectory, extension)

    listname = 'filelist.txt'
    listnameComplete = os.path.join(subdirectory, listname)

    with open(listnameComplete, 'w') as f:

        files = glob.glob(path)

        for file in files:
            filename = file.replace(subdirectory + '/', '')
            f.write(filename)
            f.write('\r\n')

        print('File list written')


if __name__ == '__main__':
    slice()
