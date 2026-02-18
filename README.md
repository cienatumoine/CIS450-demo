# CIS450-demo
## Introduction
This repo illustrates best practice README file generation
## Projects
Open-CV image processing demos
## Resources
  <img src="OpenCV_logo_black_.png" alt="OpenCV" width="100"/>

[OpenCV](https://opencv.org)

## Edge detection 
Edge detection focuses on pixel intensity and how it sharply changes. Gaussian blur is used to modify the image by smoothing it and limiting noise. Sobel operators detect changes in vertical and horizontal directions and Thresholding filters minor edges.
## Image Blending
Image blending merges two images into one result. The detected edges are layereed on the orginal image. In order for this to work, both images must share the same dimensions and color format.

## Instruction for HOW Plotting works
Plt.plot(x,y): this creates a 2D line plot that connects the (x,y) points and returns a list of matplotlib.lines.Line2D objects.
It uses the current Axes (pyplot.gca()) under the hood (pyplot.plot -> gca().plot -> Axes.plot -> Axes.add_line).
I also learned that x and y must have the same length.  
Below I am going to dive a little deeper into what this sequence means:
plt.plot(x,y) is explained above
gca().plot gets current Axes from the pyplot state machine, it returns an Axes instance
Axes.plot() is an object oriented method that creates Line2D artists from the given data and styling, it returns a lisst of Line 2D objects
Axes.add_line(line) registers a prebuilt Line2D artist with the Axes, it returns the added artist.
When plt.plot(x,y) is called, the interface forwars the call to current Axes, if not figure exists, one is automatically created. A Line2D obj is created using x & y data. Line is added to Axes obj, Axes updates its limits. Once plt.show() is executed the Figure calls its backend renderer. Then it is displayed.