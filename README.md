# IDIA – Convert Fits datacubes to DDS

Scripts to convert spectroscopic datacubes to DDS format for use in VR and other visualisation environments.

**slice.py** uses [Astropy](http://www.astropy.org) and [PIL](https://pypi.python.org/pypi/Pillow/4.2.1)

The **makedds** command relies on the *[texassemble](https://github.com/Microsoft/DirectXTex/wiki/Texassemble)* utility included in [DirectXTex](https://github.com/Microsoft/DirectXTex). It takes a series of .tiff images as input and outputs a 3-dimensional DDS file of the same bit-depth as the input images.

*Texassemble.exe* has to be built with Visual Studio 17 or clang for Windows v9. Adding the executable to the Windows PATH makes is executable from anywhere.
