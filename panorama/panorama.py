#!/usr/bin/env python
'''
Stiching sample
==================
Show how to use Stitcher API from python in a simple way to stich panoramas
or scans.
'''

# Python 2/3 compatability
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

#Expanding *.png also assures it is working
def expand_inputs(args):
    """Expand any wildcard patterns (globs) into concrete file paths."""
    paths = []
    for a in args:
        matches = glob.glob(a)
        if matches:
            paths.extend(matches)
        else:
            paths.append(a)
    return sorted(paths)

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

#Convert
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

# This code below is essentially the most important line of code 
# This is where the stitching happens 
    stitcher = cv.Stitcher_create(mode)
    status, pano = stitcher.stitch(imgs)

#Checking to see if fails
    if status != cv.Stitcher_OK:
        print("Stitching failed. OpenCV status code:", status)
        print("Tips: use more overlap, same exposure, rotate in place, avoid moving objects.")
        sys.exit(1)

    out_file = "result.jpg"
    cv.imwrite(out_file, pano)
    print("✅ Panorama saved as:", out_file)


if __name__ == "__main__":
    main()