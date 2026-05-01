from PIL import Image
import os
from pathlib import Path

input_folder = "large_images"
output_folder = "tiles"

tile_size = 800
overlap = 0.20   # use 0 if you do not want overlap

os.makedirs(output_folder, exist_ok=True)

for image_path in Path(input_folder).glob("*.*"):
    if image_path.suffix.lower() not in [".jpg", ".jpeg", ".png", ".tif", ".tiff"]:
        continue

    img = Image.open(image_path)

    # Get original DPI (fallback to 1200 if not present)
    original_dpi = img.info.get("dpi", (1200, 1200))

    w, h = img.size
    step = int(tile_size * (1 - overlap))

    tile_id = 0

    for y in range(0, h, step):
        for x in range(0, w, step):

            right = min(x + tile_size, w)
            bottom = min(y + tile_size, h)

            tile = img.crop((x, y, right, bottom))

            tile_name = f"{image_path.stem}_tile_{tile_id}_x{x}_y{y}.jpg"

            tile.save(
                os.path.join(output_folder, tile_name),
                quality=95,
                dpi=original_dpi   # ✅ preserve original DPI
            )

            tile_id += 1

    print(f"{image_path.name}: {tile_id} tiles saved with DPI {original_dpi}")
