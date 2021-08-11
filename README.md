# Toyhou.se thumbnail maker

Creates thumbnail and, if asked, a resized version of the original image ready for upload to toyhou.se.

### Requirements:
Requires a compiled version of libcairo to be available.
If on linux, install whatever cairo package you get.
If on windows, I cannot help you (trust me, I tried).

### Usage:
```
usage: thumbnailer.py [-h] [--stamp [STAMP]] [-d [DIMENSION]] [in_file]

Toyhouse image processor

positional arguments:
  in_file               The file to process

optional arguments:
  -h, --help            show this help message and exit
  --stamp [STAMP]       The image to superimpose for the thumbnail (SVG)
  -d [DIMENSION], --dimension [DIMENSION]
                        The maximum dimension the image should have
```

Recommended to use in combination with `find`.

