#OVERVIEW

This is an implementation of Minimax algorithm and OpenCV's Hough Circle Transform to create an autonomously tictactoe playing robotic arm.

- Minimax Algorithm http://cwoebker.com/posts/tic-tac-toe
- Hough Circle Transform http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_houghcircles/py_houghcircles.html

#CALIBRATION
CAMERA<br />
<br />
1. Run
```
python robo_tictactoe/calibration/camera/calibrate.py
```

2. Place a circle on the top-left corner of your Tictactoe box and get the coordinates printed on the command line.

3. Edit
```
sudo nano robo_tictactoe/main/main.py
```
edit line 182
```python
regions = regions.Regions(x,width,height,y,3,3)
```
where:<br />
x      = x coordinate from calibration <br />
y      = y coordinate from calibration <br />
width  = width of Tictactoe box in pixels <br />
height = width of Tictactoe box in pixels <br />


ROBOTIC ARM<br />
<br />
1. Install node modules
```
cd robo_tictactoe/calibration/arm/
sudo npm install
```

2. Run the server
```
node server.js
```

3. Move the sliders

4. Define all servo positions
```
sudo nano robo_tictactoe/main/arm.py
```

#USAGE
Run
```
python /robo_tictactoe/main/main.py
```
