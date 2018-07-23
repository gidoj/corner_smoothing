from Tkinter import *
from math import cos, sin, acos, asin, pi, sqrt

###super messy and ugly -- just testing an idea

###WINDOW STUFF###
root = Tk()
root.title("Smooth Test")

w = 500
h = 300

f = Frame(root)
f.pack()

c = Canvas(f, height=h, width=w, bg="white")
c.pack(side=LEFT, anchor=NW)

def slider_adjust(event):
	update()
	redraw()

def brush_adjust(event):
	global brush_size
	brush_size = brush_slider.get()
	redraw()

slider = Scale(f, from_=1, to=0, resolution=0.01, command=slider_adjust)
slider.set(1)
slider.pack()

brush_slider = Scale(f, from_=10, to=1, resolution=1, command=brush_adjust)
brush_slider.set(3)
brush_slider.pack()
###END WINDOW STUFF###

anchor_size = 6
anchors = [[w/4, 2*h/3], [w/2, h/3], [3*w/4, 2*h/3]]
anchor_abs_slope = 1.0*(anchors[0][1]-anchors[1][1])/(anchors[0][0]-anchors[1][0])
anchor_ly_int = 1.0*(anchors[1][1] - anchor_abs_slope*anchors[1][0])
anchor_ry_int = 1.0*(anchors[1][1] + anchor_abs_slope*anchors[1][0])
#anchor_length = sqrt((anchors[0][0] - anchors[1][0])**2 + (anchors[0][1] - anchors[1][1])**2)
abs_x_diff = anchors[1][0]-anchors[0][0]

marker_size = 4
marker_origin = anchors[1]
markers = [marker_origin[0], marker_origin[0], marker_origin[1]]#[x1, x2, y]

brush_size = 3
step_size = 1

####DRAWING FUNCTIONS#######

def redraw():
	c.delete("all")
	c.create_rectangle(0, 0, w, h, fill="white", outline="")
	draw_line(anchors[0][0], anchors[0][1], markers[0], markers[2], anchor_abs_slope, anchor_ly_int)
	#draw_line(markers[1], markers[2], anchors[2][0], anchors[2][1],  -1*anchor_abs_slope, anchor_ry_int)
	c.create_line(markers[1], markers[2], anchors[2][0], anchors[2][1])
	draw_curve()
	#c.create_line(markers[1], markers[2], anchors[2][0], anchors[2][1], fill="black")
	#draw_anchors()
	#draw_markers()

def draw_circle(x, y, r, col):
	c.create_oval(x-r/2, y-r/2, x+r/2, y+r/2, fill=col, outline="")

def draw_anchors():
	for i in range(len(anchors)):
		draw_circle(anchors[i][0], anchors[i][1], anchor_size, "gray")

def draw_markers():
	draw_circle(markers[0], markers[2], marker_size, "red")
	draw_circle(markers[1], markers[2], marker_size, "red")

def draw_line(x0, y0, x1, y1, slope, y_int):
	cx = x0
	cy = y0
	while cx < x1:
		draw_circle(cx, cy, brush_size, "black")
		cx += step_size
		cy = cx*slope + y_int


def draw_curve():
	'''
	a = 0.5*abs(markers[0]-markers[1])
	b = 0.5*sqrt((anchors[1][0]-markers[0])**2 + (anchors[1][1]-markers[2])**2)
	radius = -10
	if a - b != 0: radius = (a**2 - 0.5*b**2)/sqrt(abs(b**2 - a**2))
	xoff = anchors[1][0]
	yoff = anchors[1][1] + radius
	phi = asin(a/radius)
	theta = acos(a/radius)
	if radius == -10:
		phi = 0
		theta = 0
	'''
	b1 = markers[2]+markers[0]/anchor_abs_slope
	b2 = markers[2]-markers[1]/anchor_abs_slope
	nx = -0.5*anchor_abs_slope*(b2-b1)
	ny = -nx/anchor_abs_slope + b1
	radius = sqrt((markers[0]-nx)**2 + (markers[2]-ny)**2)
	theta = 0
	off = sqrt((markers[0]-anchors[1][0])**2 + (markers[2]-anchors[1][1])**2 + radius**2)
	xoff = anchors[1][0]
	yoff = anchors[1][1] + off
	phi = 0
	if off != 0: phi = acos(radius/off)
	theta = pi/2 - phi
	alpha = theta + 2*phi
	#draw_circle(nx, ny, brush_size, "green")
	while alpha > theta:
		cx = radius*cos(alpha) + xoff
		cy = -radius*sin(alpha) + yoff
		draw_circle(cx, cy, brush_size, "black")
		alpha -= 0.01
	
####END DRAWING FUNCTIONS#######

def update():
	global markers
	markers[0] = marker_origin[0] - abs_x_diff*(1 - slider.get())
	markers[1] = marker_origin[0] + abs_x_diff*(1 - slider.get())
	markers[2] = anchor_abs_slope*markers[0] + anchor_ly_int
	markers

update()
redraw()

root.mainloop()