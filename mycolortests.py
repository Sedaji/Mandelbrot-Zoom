#! /usr/bin/python3

#TODO: optimize code for speed via numpy 
#		Check and see if modulo for colors will work.
#			ffmpeg video slow down via copy and pasting certain frames. 
from PIL import Image, ImageDraw
import time,os
import numpy as np
from datetime import date

start_time=time.time()
# Image size (pixels)
frames= 1300  # frames - startframe = total frames. 
startframe= -1 # [frame -1: frame 0], can change start frame to anything to start at a zoomed in spot.

width = 1900 # change to smaller dimensions for fast render times
height = 1080

m = 1	 # MULTIPLIER
m2 = (m / (width/height))

# Our plane on which we plot the points
zoomout = 1
 
realNeg = (-1.991520264499989) * zoomout # -1.991520264499989 awesome rainbow swirl
realPos = realNeg + (3 * zoomout)
imagiNeg = (-1.000000036503305) * zoomout # -1.000000036503305
imagiPos = imagiNeg + (2 * zoomout)

realPlots = [None] * width
imagiPlots = [None] * height

imageinfo = (f"{width}x{height}")

dateFolder=str(date.today())
dir = os.path.join(dateFolder)
if not os.path.exists(dir):
        os.mkdir(dir)
def colorme(n):
	if n in range(1,25):
		draw.point(([i,j]), ( int((n-1)*2.25) , int((n-1)*0.125) , int((n-1)*2.79167) ) )  	
	if n in range(25,int(.5*tests)):
		color = int(((n-25) * .5714))
		draw.point(([i,j]), (r+color,g+color,b+color))
	if n in range(int(.5*tests),int(.6*tests)):
		color = int(((n-340) * rgbIncrement))
		draw.point(([i,j]), (104,226,226-color))	
	if n in range(int(.6*tests),int(.7*tests)):
		color = int(((n-430) * rgbIncrement))
		draw.point(([i,j]), (104+color,226,104))	
	if n in range(int(.7*tests),int(.8*tests)):
		color = int(((n-520) * rgbIncrement))
		draw.point(([i,j]), (226,226-color,104))	
	if n in range(int(.8*tests),int(.9*tests)):
		color = int(((n-610) * rgbIncrement))
		draw.point(([i,j]), (226,104,104+color))	
	if n in range(int(.9*tests), int(tests-tests/tests) ):
		color = int(((n-700) * rgbIncrement))
		draw.point(([i,j]), (226-color,104,226))

def mandelbrot(c):
	for n in range(1,tests):
		z[n] = z[n-1]**2 + c
		# If it's distance is greater than 2 from (0,0) NOT part of set
		if abs(z[n]) > 2:
			return n
	# Big n = Close to mandelbrot
	# Small n = Background / fading to black
	return n	

for x in range(frames):
	# Divide our plane into the number of pixels
	realIncrement = (realPos - realNeg) / width
	imagiIncrement = (imagiPos - imagiNeg) / height
	# Store all complex numbers and their corresponding pixels into a list
	if x > startframe: # Change to 0 to skip rendering of first frame
		start_timeX=time.time()
		for i in range(width):
			realPlots[i] = realNeg + realIncrement*i
		for i in range(height):
			imagiPlots[i] = imagiNeg + imagiIncrement*i
		tests = 200 #increase number of tests to 500 for better quality
		z=[None] * tests
		z[0]=0

		canvas = 0 
		im = Image.new('RGB', (width, height), (canvas, canvas, canvas))

		rgbIncrement = 1.3555	
		r,g,b = 94 , 3 , 94 # color for pink
		draw = ImageDraw.Draw(im)
		# ZOOM IN CODE
		for i in range(width):
			for j in range(height):
				n = mandelbrot(complex(realPlots[i],imagiPlots[j]))
				colorme(n)			
			print(f"{i}/{width}",end='\r')							
		im.save(f'./{dateFolder}/colortest.mandel_{imageinfo}_frame{x}.png', 'PNG')
		print(f"--- mandel_{imageinfo}_frame {x}/{frames} ---")
	realNeg += realIncrement * m
	realPos -= realIncrement * m
	imagiNeg += imagiIncrement * m2 
	imagiPos -= imagiIncrement * m2


# encode into a video format:
# ffmpeg -r 25 -f image2 -s 1920x1080 -i mandel_1920x1080_frame%d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p test.mp4
