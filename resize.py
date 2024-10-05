import argparse
from pathlib import Path

parser = argparse.ArgumentParser(description="Resize and crop images.")
parser.add_argument("-W", "--width", type=int, default=800, help="Width of the output image")
parser.add_argument("-H", "--height", type=int, default=600, help="Height of the output image")
parser.add_argument("-o", "--output", required=True, help="Output directory")
parser.add_argument("srcdir", help="Source directory containing images")

args = parser.parse_args()
width = args.width
height = args.height
dstdir = Path(args.output)
srcdir = Path(args.srcdir)

from PIL import Image

def resize_and_crop(input_path, output_path, width, height):
    with Image.open(input_path) as img:
        # Resize to `width`px while maintaining aspect ratio
        img.thumbnail((width, width * 10), Image.LANCZOS)
        
        # Crop from the center to make the `height`px
        left = 0
        top = (img.height - height) // 2
        right = width
        bottom = top + height
        
        img_cropped = img.crop((left, top, right, bottom))
        img_cropped.save(output_path)

if not dstdir.exists():
    dstdir.mkdir(parents=True)

images = sorted(srcdir.glob("*"))
for i, image in enumerate(images):
    if image.suffix.lower() in [".png", ".jpg", ".jpeg"]:
        input_image  = str(image)
        output_image = str(dstdir / (image.stem + ".png"))
        print(f"{i+1}/{len(images)}: {input_image} -> {output_image}")
        resize_and_crop(input_image, output_image, width, height)
