#!/usr/bin/env python3

import argparse
from typing import Optional

from PIL import Image
import io
import cairosvg
import math
from os import listdir
from os.path import isfile, join


def load_thumbnail(file: str, width: int, height: int) -> Image:
    smallest_parent_dimension = min(width, height)

    if file.endswith('.svg'):
        out = io.BytesIO()
        # render square thumbnail
        # TODO: handle non-square svg
        cairosvg.svg2png(url=file, output_width=smallest_parent_dimension, output_height=smallest_parent_dimension,
                         write_to=out)
        return Image.open(out)


def calc_anchor(width: int, height: int):
    if width > height:
        gap = int((width - height) / 2)
        return gap, 0
    else:
        gap = int((height - width) / 2)
        return 0, gap


def process(filename: str, stamp: str, dimension: int = 1280):
    # trim last extension
    filename_root = ".".join(filename.split('.')[:-1])

    # convert to RGBA for compositing
    try:
        in_image: Image = Image.open(filename).convert('RGBA')
    except:
        raise ValueError("could not convert image")

    width, height = in_image.width, in_image.height

    scaling = 1
    # scale image only if asked
    if dimension is not None:
        max_dimension = max(width, height)
        # only scale if target dimensions is smaller
        if dimension < max_dimension:
            scaling = dimension / max_dimension
            in_image = in_image.resize((math.floor(width * scaling), math.floor(height * scaling)))

    # load thumbnail (may be svg)
    # same size as uploaded image as required by toyhou.se
    thumbnail = load_thumbnail(stamp, in_image.width, in_image.height)

    # generate position required for centering
    position = calc_anchor(in_image.width, in_image.height)

    # in_image.paste(thumbnail, position, thumbnail)
    if dimension is not None:
        # save resized image
        in_image.save(filename_root + '_resized.png', 'PNG')
    # generate stamped thumbnail
    in_image.alpha_composite(thumbnail, position)
    in_image.save(filename_root + '_thumbnail.png', 'PNG')


def main():
    parser = argparse.ArgumentParser(description='Toyhouse image processor')
    parser.add_argument('in_file', nargs='?', default=None, type=str, help='The file to process')
    parser.add_argument('--stamp', nargs='?', default='stamp.svg',
                        help='The image to superimpose for the thumbnail (SVG)')
    parser.add_argument('-d', '--dimension', nargs='?', default=1280, type=int,
                        help='The maximum dimension the image should have')

    args = parser.parse_args()

    if args.in_file is None:
        files = [file for file in listdir() if isfile(file)]
        for file in files:
            try:
                process(file, args.stamp, dimension=args.dimension)
            except:
                pass
    else:
        process(args.in_file, args.stamp, dimension=args.dimension)


if __name__ == '__main__':
    main()
