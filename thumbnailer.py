import argparse

from PIL import Image
import io
import cairosvg
import math


def load_thumbnail(file: str, width: int, height: int) -> Image:
    smallest_parent_dimension = min(width, height)

    if file.endswith('.svg'):
        out = io.BytesIO()
        # render square thumbnail
        # TODO: handle non-square svg
        cairosvg.svg2png(url=file, output_width=smallest_parent_dimension, output_height=smallest_parent_dimension, write_to=out)
        return Image.open(out)

def calc_anchor(width: int, height: int):
    if width > height:
        gap = int((width - height) / 2)
        return (gap, 0)
    else:
        gap = int((height - width) / 2)
        return (0, gap)

def main():
    parser = argparse.ArgumentParser(description='Toyhouse image processor')
    parser.add_argument('in_file', help='The file to process')
    parser.add_argument('--stamp', nargs='?', default='stamp.svg',
                        help='The image to superimpose for the tumbnail (SVG)')
    parser.add_argument('-d', '--dimension', nargs='?', default=None, type=int,
                        help='The maximum dimension the image should have')

    args = parser.parse_args()

    # trim last extension
    filename_root = ".".join(args.in_file.split('.')[:-1])

    # convert to RGBA for compositing
    in_image: Image = Image.open(args.in_file).convert('RGBA')

    width, height = in_image.width, in_image.height

    scaling = 1
    # scale image only if asked
    if args.dimension is not None:
        max_dimension = max(width, height)
        # only scale if target dimensions is smaller
        if args.dimension < max_dimension:
            scaling = args.dimension / max_dimension
            in_image = in_image.resize((math.floor(width * scaling), math.floor(height * scaling)))

    # load thumbnail (may be svg)
    # same size as uploaded image as required by toyhou.se
    thumbnail = load_thumbnail(args.stamp, in_image.width, in_image.height)

    # generate position required for centering
    position = calc_anchor(in_image.width, in_image.height)

    #in_image.paste(thumbnail, position, thumbnail)
    if args.dimension is not None:
        # save resized image
        in_image.save(filename_root + '_resized.png', 'PNG')
    # generate stamped thumbnail
    in_image.alpha_composite(thumbnail, position)
    in_image.save(filename_root + '_thumbnail.png', 'PNG')


if __name__ == '__main__':
    main()
