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

# Final Project
## Description

For my final project I have decided to design to create a Sketch generator. My plan is to convert a photo into a pencil sketch. I chose to do this for my project because it is not a previous project that I've done and would love to see the result. The user will upload a photo (any image), it will process the image, looking at the shapes, edges, and details. It will focus on lines, shadows, and contours, rather than colors and textures. Output = pencil sketch! 

## Design

## Design

This project is currently in the prototyping phase. My goal is to create a sketch generator that converts a regular image into a pencil sketch. The program will take a user-uploaded image, detect edges, contours, and shadows, and transform the image into a grayscale sketch emphasizing lines rather than colors. I plan to use Python with OpenCV to process the image by converting it to grayscale, applying Gaussian blur, detecting edges, and using image blending techniques to create the sketch effect.

To understand how to implement this, I found two online resources to learn about image processing techniques in OpenCV. These resources helped me understand how edge detection, thresholding, and image inversion work together to produce a sketch-like result.

Resources used:
- https://opencv.org/
- https://www.geeksforgeeks.org/python/convert-image-into-sketch/


I also used ChatGPT to help me understand how to structure the Python code, how OpenCV functions work, and how to combine multiple image filters to create the sketch effect. I asked questions about grayscale conversion, Gaussian blur, edge detection, and blending images to achieve the final sketch appearance. I will continue updating this README as the project develops.