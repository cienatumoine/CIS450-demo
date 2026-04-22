# Author: Ciena Tumoine - Final Project Template
# Course: CIS 450
# Final Project Template
#
# to build:   docker build -t app .      
# to run:     docker run -p 80:80 app
# in browser: http://localhost

"""
Project: Final Docker + Flask + OpenCV Image Processing App
app.py - Sketch Generator
Description: This file implements a Flask app that allows users to upload an image "Choose File"; then
accepts user input for sketch strength and export size. It'll call the OpenCV sketch algorithm to transform the image and resize the final sketch for export.
Lastly, it'll return the generated sketch image back to the browser. This app will run in a Docker container to make sure it is consistent when
running in different environments. It also provides an HTML interface for image upload and sketch controls.

Flask is used to create the web interface and handle image uploads.
werkzeug.utils is used for secure filename handling.
OpenCV (cv2) is used for image processing to convert the uploaded image into a pencil sketch.
os module is used for interacting with the operating system, such as file paths and directories.
Numpy is used for numerical operations on image data.
"""
# to build:   docker build -t app .     
# to run:     docker run -p 80:80 app
# in browser: http://localhost


from flask import Flask, request, send_file, render_template_string
from werkzeug.utils import secure_filename
import os
import cv2
import numpy as np

    # Initialize Flask app
app = Flask(__name__)

    # Upload and output folders
UPLOAD_FOLDER = "/tmp/uploads"
OUTPUT_FOLDER = "/tmp/outputs"

    # Create upload and output directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


"""Converts input image into a pencil sketch by:
 loading image, convert to grayscale, invert grayscale, apply Gaussian blur
blend original grayscale image with blurred inverse, extract edges, 
combine edges + sketch"""
def generate_sketch(image_path, strength=45):
    # Load image from disk
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Invalid image uploaded")

    # Convert to grayscale (removes color)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Invert image (creates pencil shading base)
    invert = cv2.bitwise_not(gray)

    # Determine kernel size for Gaussian blur
    k = max(3, strength)
    if k % 2 == 0:
        k += 1

    # Blur inverted image (controls sketch softness)
    blur = cv2.GaussianBlur(invert, (k, k), 0)

    # Blend grayscale with blur (core pencil effect)
    sketch = cv2.divide(gray, 255 - blur, scale=256)

    # Detect edges (adds sketch definition)
    edges = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY,
        9,
        8
    )
    # Combine sketch shading + edges
    final = cv2.bitwise_and(sketch, edges)

    return final

"""Resize the final sketch image, 'original' returns image unmodified, 
small scales to 40% of original size,
medium scales to 70% of original size.
large keeps 100% size
Uses cv2.INTER_AREA for best quality when shrinking images.
"""
def resize_for_export(image, size_option):
    if size_option == "original":
        return image

    # Get current dimensions
    h, w = image.shape[:2]

    scale_map = {
        "small": 0.4,
        "medium": 0.7,
        "large": 1.0
    }

    # Get scaling factor
    scale = scale_map.get(size_option, 1.0)

    # Calculate new dimensions
    new_w = int(w * scale)
    new_h = int(h * scale)

    # Resize image
    return cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_AREA)


# =========================
# HTML UI
# =========================
"""
Provides:
- Image upload control
- Slider to control sketch strength (darkness/detail)
- Dropdown to select export size
- Submit button to trigger sketch generation
This UI is returned on every GET request to the root route.
"""

HTML = """
<!doctype html>
<title>Pencil Sketch Generator</title>

<h2>Pencil Sketch Generator</h2>

<form method="post" enctype="multipart/form-data">
  <input type="file" name="file" required><br><br>

  <label>Sketch Strength (1-50):</label><br>
  <input type="range" name="strength" min="1" max="50" value="45"><br><br>

  <label>Export Size:</label><br>
  <select name="size">
    <option value="original">Original</option>
    <option value="small">Small</option>
    <option value="medium">Medium</option>
    <option value="large">Large</option>
  </select><br><br>

  <input type="submit" value="Generate Sketch">
</form>

<p>Lower strength = more detail | Higher = darker lines</p>
"""


# =========================
# ROUTE
# =========================
"""
    Main application route.
    GET:
        Renders the HTML interface for the user.
    POST:
        1. Validates uploaded image file
        2. Reads sketch strength and export size from form
        3. Saves the uploaded image to disk for processing
        4. Calls generate_sketch() to create pencil sketch
        5. Resizes the sketch for export
        6. Saves and returns the final PNG image to the browser
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":

        # Validate and process uploaded file
        file = request.files.get("file")
        if not file or file.filename == "":
            return "No file uploaded", 400

        # Validate sketch strength and size option
        strength = int(request.form.get("strength", 45))
        size_option = request.form.get("size", "original")

        # Secure the filename
        filename = secure_filename(file.filename)

        # Define input and output paths
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        output_path = os.path.join(OUTPUT_FOLDER, f"sketch_{filename}.png")

        # Create output directory if it doesn't exist
        os.makedirs(OUTPUT_FOLDER, exist_ok=True)

        file.save(input_path)

        # generate sketch
        result = generate_sketch(input_path, strength)

        # resize export
        result = resize_for_export(result, size_option)

        cv2.imwrite(output_path, result)

        return send_file(output_path, mimetype="image/png")

    # IMPORTANT: always return something for GET
    return render_template_string(HTML)



"""
Starts the Flask server.
- host='0.0.0.0' allows Docker/browser access
"""
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)