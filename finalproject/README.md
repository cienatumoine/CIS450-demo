# Final Project
## Description

For my final project I have decided to design to create a Sketch generator. My plan is to convert a photo into a pencil sketch. I chose to do this for my project because it is not a previous project that I've done and would love to see the result. The user will upload a photo (any image), it will process the image, looking at the shapes, edges, and details. It will focus on lines, shadows, and contours, rather than colors and textures. Output = pencil sketch! 

## Design


This project is currently in the prototyping phase. My goal is to create a sketch generator that converts a regular image into a pencil sketch. The program will take a user-uploaded image, detect edges, contours, and shadows, and transform the image into a grayscale sketch emphasizing lines rather than colors. I plan to use Python with OpenCV to process the image by converting it to grayscale, applying Gaussian blur, detecting edges, and using image blending techniques to create the sketch effect.

To understand how to implement this, I found two online resources to learn about image processing techniques in OpenCV. These resources helped me understand how edge detection, thresholding, and image inversion work together to produce a sketch-like result.

Resources used:
- https://opencv.org/
- https://www.geeksforgeeks.org/python/convert-image-into-sketch/


I also used ChatGPT to help me understand how to structure the Python code, how OpenCV functions work, and how to combine multiple image filters to create the sketch effect. I asked questions about grayscale conversion, Gaussian blur, edge detection, and blending images to achieve the final sketch appearance. I will continue updating this README as the project develops.

**Changes: I did make 1 change to my original final project design, and that was the ability to choose the size of your sketched image. 

AI Assistance:
During the development of this project, AI assisted with the following:
- Debugging Flask routing issues (missing return statements, incorrect function calls)
- Improving OpenCV image processing pipeline for better pencil sketch effects
- Designing export size functionality for image resizing
- Explaining Docker container networking and port mapping issues
I used AI as a learning assistant to help understand errors, improve code structure, and ensure the application runs reliably inside a Docker container.

Me: I need a pencil sketch generator...
AI: Got it — you want a true pencil sketch portrait look (face-focused, soft shading, not outlines or pixel effects).

To get that, we should switch to a portrait-style pipeline:

smooth facial tones (bilateral filter)
strong but soft pencil blending (color dodge)
slight facial contrast boost
NO noise, NO edges, NO thresholding

Me: I cannot see the face, they're basically white
AI: Good — that tells us exactly what’s wrong:
👉 your sketch has no proper tonal inversion balance, so skin areas are blowing out to white instead of forming graphite midtones.
We fix this by going back to a correct, stable pencil sketch formula + proper tone compression (no histogram equalization, no over-contrast tricks).

Me: make this app to where you can adjust the strength of the control of the image
AI: Make strength actually powerful

We’ll upgrade your generate_sketch() so strength controls:

blur intensity (softness)
edge intensity (detail amount)
contrast (darkness)
me: make this look more realistic
AI: Perfect — now we stop fighting OpenCV filters and move to a real artist-style pipeline.
What you actually want is:
✏️ structure → shading → stroke simulation → paper texture
not edge detection or grayscale filtering.
Below is a complete upgraded app.py that produces a much more hand-drawn graphite portrait look using a hybrid artist simulation pipeline.

Me: make the image a bit darker (more shading) dont make it look just black and white though
AI: You don’t want “more contrast” (that causes black/white).
You want deeper graphite mid-tones so the sketch looks shaded, not binary.
Add a mid-tone darkening pass after sharpening.

Me: this app.py, make an export option where the user can choose the size of the image
AI: You’re very close. The only thing missing is controlling the output resolution before saving.

Right now, you always save the sketch at the original size. We’ll add:
✅ A size selector (Small / Medium / Large / Original)
✅ A resize step right before saving the sketch
✅ No extra files, still one app.py

Me: i feel like i cant tell a difference in the sizes of the images
AI: Yeah—that’s because your current resizing logic is only changing width, and for many images the visual difference is subtle (especially in a browser when everything still fits on screen).

Also: “640 vs 1280 vs 1920” only feels different if you actually force a visible change in pixel density or download size, not just display.

## Test
Test Case 1: Uploaded Image
- Uploaded multiple image successfully and ran iwthout errors, I just wanted to adjust some things to make it look more realistic

Test Case 2: Strength Control
I found a way to be able to adjust the strength control of the images, this would result in darker and heavier lines, I did this because originally I couldn't see the faces that well 

Test Case 3: Ran into a few PORT problems
- There were few times the app would not run because it was not able to run on the same PORT as before but I changed to a working PORT and went back to the old PORT, it worked most of the time.

Test Case 4: Added Export option
I implemented a function that allows the user to choose the size of the image they wanted. It took me a while, I couldnt really see a difference between the sizes but with the help of AI I was able to fix it.

Test 5: Everything ran successfully