# kinect4
An exercise in computer vision and the Internet of Crap Things. 

The basic premise of kinect4 is simple - a connect-4 game has a clearly defined grid board, and distinctly colored pieces. This lends itself well to computer vision - a single-board computer (rpi, beaglebone) with a camera can divide the board into sections and identify the colours in a section. This can then be represented as a simple data structure, and transmitted to another SBC that controls a bunch of LEDs to reproduce the game in real-time on a larger board. Blinkenlichten at building scale, for example. 
