#!/usr/bin/env python3
"""
Create a panorama using OpenCV's high-level Stitcher API.

Run (from the panorama directory):
  python panorama.py panorama ../resolution/*.png
Outputs:
  result.jpg (in the panorama directory)
"""

import sys
import glob
import cv2 as cv
import numpy as np



def expand_inputs(args):
    """Expand any wildcard patterns (globs) into concrete file paths."""
    paths = []
    for a in args:
        # Expand wildcards like ../resolution/*.png
        matches = glob.glob(a)
        if matches:
            paths.extend(matches)
        else:
            paths.append(a)
    # Keep a stable order (important for panoramas)
    return sorted(paths)

def stitch_once(images, mode):
    stitcher = cv.Stitcher_create(mode)
    return stitcher.stitch(images)


def hierarchical_stitch(imgs, mode, group_size=3):
    stitched = []

    # Step 1: stitch small groups
    for i in range(0, len(imgs), group_size):
        group = imgs[i:i+group_size]
        if len(group) == 1:
            stitched.append(group[0])
            continue

        status, pano = stitch_once(group, mode)
        print(f"Group {i//group_size} size={len(group)} status={status}")

        if status == cv.Stitcher_OK and pano is not None:
            stitched.append(pano)
        else:
            stitched.extend(group)

    # Step 2: stitch merged results
    if len(stitched) < 2:
        return cv.Stitcher_ERR_NEED_MORE_IMGS, None

    status, pano = stitch_once(stitched, mode)
    print(f"Final merge chunks={len(stitched)} status={status}")
    return status, pano

#Before the images are processed we must validate the inputs, in order to stitch, we have to make sure we have all the data needed
def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python panorama.py panorama <images...>")
        print("Example:")
        print("  python panorama.py panorama ../resolution/*.png")
        sys.exit(1)

    mode_arg = sys.argv[1].lower()
    if mode_arg not in ("panorama", "scans"):
        print("Mode must be 'panorama' or 'scans'")
        sys.exit(1)

#There are two modes of stitching: panorama and scans
    mode = cv.Stitcher_PANORAMA if mode_arg == "panorama" else cv.Stitcher_SCANS

    image_args = sys.argv[2:]
    image_paths = expand_inputs(image_args)

    if len(image_paths) < 2:
        print("Need at least 2 images.")
        print("Got:", image_paths)
        sys.exit(1)

# Here the images are being loaded
    imgs = []
    for p in image_paths:
        img = cv.imread(p)
        if img is None:
            print("Could not read:", p)
            sys.exit(1)
        imgs.append(img)

#stitching
    stitcher = cv.Stitcher_create(mode)

#lower confidence level until it works
    if hasattr(stitcher, "setPanoConfidenceThresh"):
        stitcher.setPanoConfidenceThresh(0.4)   
        print("Set pano confidence threshold to 0.4")
    else:
        print("This OpenCV build doesn't expose setPanoConfidenceThresh()")

  #  img = cv.resize(img, None, fx=0.5, fy=0.5)

#automatic stitching
    status, pano = stitcher.stitch(imgs)

#check status
    if status != cv.Stitcher_OK:
        print("Stitching failed. OpenCV status code:", status)
        sys.exit(1)

    import numpy as np  

    gray = cv.cvtColor(pano, cv.COLOR_BGR2GRAY)

# darker areas are more likely to be background
    _, mask = cv.threshold(gray, 10, 255, cv.THRESH_BINARY)

# Clean small specks so they don't prevent cropping
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (9, 9))
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    mask = cv.morphologyEx(mask, cv.MORPH_CLOSE, kernel)

# Flood-fill background from corners
    h, w = mask.shape[:2]
    ff = cv.copyMakeBorder(mask, 1, 1, 1, 1, cv.BORDER_CONSTANT, value=0)

# floodFill requires a separate mask of size (H+2, W+2) for the image being flood-filled
    flood_mask = np.zeros((h + 4, w + 4), dtype=np.uint8)

    cv.floodFill(ff, flood_mask, (0, 0), 255)
    cv.floodFill(ff, flood_mask, (w + 1, 0), 255)
    cv.floodFill(ff, flood_mask, (0, h + 1), 255)
    cv.floodFill(ff, flood_mask, (w + 1, h + 1), 255)

# Background is now 255; invert to get content
    ff = ff[1:-1, 1:-1]
    content = cv.bitwise_not(ff)

# Find contours of the content
    ys, xs = np.where(content > 0)
    if len(xs) and len(ys):
        x0, x1 = xs.min(), xs.max()
        y0, y1 = ys.min(), ys.max()
        pano = pano[y0:y1+1, x0:x1+1]

#saving result.jpg
    out_file = "result.jpg"
    cv.imwrite(out_file, pano)
    print("✅ Panorama saved as:", out_file)

if __name__ == "__main__":
    main()