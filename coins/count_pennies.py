import cv2
import numpy as np
import os

def count_pennies(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Cannot open image: {image_path}")

    output = image.copy()

    # Convert to HSV for copper detection
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([5, 80, 50])
    upper = np.array([25, 255, 255])
    copper_mask = cv2.inRange(hsv, lower, upper)

    # Remove noise
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
    copper_mask = cv2.morphologyEx(copper_mask, cv2.MORPH_OPEN, kernel)
    copper_mask = cv2.morphologyEx(copper_mask, cv2.MORPH_CLOSE, kernel)

    # Find contours
    contours, _ = cv2.findContours(copper_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    penny_count = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 500:  # ignore tiny blobs
            continue

        # Approximate circularity
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)
        if radius <= 0:
            continue
        circularity = area / (np.pi * (radius ** 2))
        if circularity < 0.6:  # ignore non-circular shapes
            continue

        # Count as penny
        penny_count += 1
        cv2.circle(output, (int(x), int(y)), int(radius), (0, 255, 0), 2)

    # Save annotated image
    out_path = os.path.join(os.path.dirname(image_path), "pennies_detected.png")
    cv2.imwrite(out_path, output)

    return penny_count, out_path

if __name__ == "__main__":
    image_file = "coins.png"  # make sure this is correct
    count, out_image = count_pennies(image_file)
    print(f"Number of pennies detected: {count}")
    print(f"Annotated image saved as: {out_image}")