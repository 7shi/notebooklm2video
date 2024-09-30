import sys

args = sys.argv[1:]
if len(args) != 3 or args[0] != "-o":
    print(f"Usage: python {sys.argv[0]} -o dstdir srcdir", file=sys.stderr)
    sys.exit(1)

from pathlib import Path
from PIL import Image

dstdir = Path(args[1])
srcdir = Path(args[2])

def resize_and_crop(input_path, output_path, width=800, height=600):
    with Image.open(input_path) as img:
        # アスペクト比を保ちながら横幅800pxにリサイズ
        img.thumbnail((width, width * 10), Image.LANCZOS)
        
        # 画像の新しいサイズを取得
        img_width, img_height = img.size
        
        # 縦幅が600pxになるように中央からクロップ
        left = 0
        top = (img_height - height) / 2
        right = width
        bottom = top + height
        
        img_cropped = img.crop((left, top, right, bottom))
        
        # 保存
        img_cropped.save(output_path)

if not dstdir.exists():
    dstdir.mkdir(parents=True)

images = sorted(srcdir.glob("*.png"))
for i, image in enumerate(images):
    input_image  = str(image)
    output_image = str(dstdir / image.name)
    print(f"{i+1}/{len(images)}: {input_image} -> {output_image}")
    resize_and_crop(input_image, output_image)
