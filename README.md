
## Table of Contents
- [Requirement](#requirement)
- [Usage](#usage)
- [Animated sprays](#animated-sprays)
- [Static sprays](#static-sprays)
- [Multi Mipmap/Layer sprays](#multi-mipmaplayer-sprays)
- [Build](#build)
- [Disclaimer](#disclaimer)
## Requirement
REQUIREMENT: Nvidia Texture Tools installed in C:\\Program Files\\NVIDIA Corporation\\NVIDIA Texture Tools\\nvcompress.exe or set up in environment variables.


## Usage
Drag the picture/GIF over the exe or use command line with picture/GIF as argument. Vtf file will appear in the same folder as source picture.

## Animated sprays
The program will output 3 vtf files 128x128, 256x256 and 512x512. Choose whatever you want from them.
Frame limit per resolution: 
- 128x128: 55 frames
- 256x256: 15 frames
- 512x512: 3 frames
  
If there are more frames than each number, the program will trim frames to make it under the limit.

Vtf compression uses DXT1 with 1 alpha bit.
![Animated sprays](./bunny.gif)
## Static sprays
This program converts common format images (jpg, png etc) from any resolution to vtf 1024x1020. If the image is not square, the program will center the image and make the background transparent.

Vtf compression uses DXT1 with 1 alpha bit.

![Static 1024x1024 sprays](./queen.gif)

## Multi Mipmap/Layer sprays
You can now drag more than one picture over the exe to make a multi mipmap/layer spray.
Tested with 3 pictures(mipmaps). Theoretically could work with up to 10, but anything after 32x32 mipmap will not look very detailed
- 512x512
- 256x256
- 128x128
- 64x64
- 32x32 etc

The order of the mipmaps will reflect the order the files are sorted in "Windows Explorer" (story by date/name etc).
The compression uses DXT1 With 1 Alpha Bit. This method sacrifices quality over transparency and maintaining the aspect ratio.
![Multi mipmap sprays](./spray_mipmaps.gif)
## Build
You can build the binary yourself with the command from command.txt or use the precompiled one (vtf.exe)

## Disclaimer
This program is mainly used to automate L4D2 spray making and not in any way configurable to make different kinds of textures with different parameters and encodings.




