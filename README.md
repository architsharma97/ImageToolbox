## About
This repository hosts a very basic Image Toolbox, which can perform the following two functions:
  - _Red-eye Reduction_: Given a front potrait color image, the toolbox will try to reduce the red-eye effect, typically caused by flash photography.
  - _Selective Blurring_: Given a color image and Rectangular Bounding Box, the toolbox will segment the object based on GrabCut algorithm and produce a motion-blur like effect for the background.

The functions come with a very basic self-explanatory GUI designed in Tkinter. It needs the following packages: **NumPy, PIL, OpenCV, Tkinter**. To run the application:
```
python main.py
```
