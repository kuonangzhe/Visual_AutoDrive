#encoding:utf-8
from matplotlib.patches import Ellipse, Circle
from matplotlib import animation
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math 
import csv
import random

list = []

with open('ultrasonic_data10.csv','rb') as csvfile:
	reader = csv.reader(csvfile)
	for i,rows in enumerate(reader):
		if i == 0:
			continue
		list.append(rows)

plt.ion() #开启interactive mode
fig = plt.figure(figsize=(18,15))

for i in range(len(list)):
#for i in range(300):
	print list[i], i
	sensor_data = list[i]
	x1,x2,x3,x6,x7,x8 = [],[],[],[],[],[]
	y1,y2,y3,y4,y5,y6,y7,y8,y9,y10,y11 = [],[],[],[],[],[],[],[],[],[],[]
	
	
	if float(sensor_data[0]) < 30.7:
		x1.append(-7.5-float(sensor_data[0])*math.sqrt(2)/2)#red point
		y1.append(12.5+float(sensor_data[0])*math.sqrt(2)/2)
		x6.append(-7.5-float(sensor_data[0])*math.sqrt(2)/2)#red line
		y6.append(12.5+float(sensor_data[0])*math.sqrt(2)/2)
	elif float(sensor_data[0]) < 53:
		x2.append(-7.5-float(sensor_data[0])*math.sqrt(2)/2)#blue point
		y2.append(12.5+float(sensor_data[0])*math.sqrt(2)/2)
		y9.append(12.5+float(sensor_data[0])*math.sqrt(2)/2)#green line
	else:
#		x2.append(-7.5-100*math.sqrt(2)/2)
#		y2.append(12.5+100*math.sqrt(2)/2)
		y3.append(99)#green line
	
	if float(sensor_data[2]) < 30.7:
		x1.append(7.5+float(sensor_data[2])*math.sqrt(2)/2)#red point
		y1.append(12.5+float(sensor_data[2])*math.sqrt(2)/2)
		x7.append(7.5+float(sensor_data[2])*math.sqrt(2)/2)#red line
		y7.append(12.5+float(sensor_data[2])*math.sqrt(2)/2)
	elif float(sensor_data[2]) < 53:
		x2.append(7.5+float(sensor_data[2])*math.sqrt(2)/2)#blue point
		y2.append(12.5+float(sensor_data[2])*math.sqrt(2)/2)
		y10.append(12.5+float(sensor_data[2])*math.sqrt(2)/2)#green line
	else:
#		x2.append(-7.5+100*math.sqrt(2)/2)
#		y2.append(12.5+100*math.sqrt(2)/2)
		y4.append(99)#green line

	if float(sensor_data[1]) < 32.5:
		x1.append(0)#red point
		y1.append(12.5+float(sensor_data[1]))
		y8.append(12.5+float(sensor_data[1]))#red line
	elif float(sensor_data[1]) < 100:
		x2.append(0)#blue point
		y2.append(12.5+float(sensor_data[1]))		
		y11.append(12.5+float(sensor_data[1]))#green line
	else:
		x2.append(0)
		y2.append(99)
		y5.append(99)

		
	ax = fig.add_subplot(111,facecolor='black')
	cir1 = Circle(xy = (0.0, 0.0), radius=45, alpha=0.3, color='white')
	ax.add_patch(patches.Rectangle((-7.5, -12.5), 15, 25))
	ax.add_patch(cir1)
	plt.plot([-15,-15,-15],[-100,0,100],color = 'white', lw = 3)
	plt.plot([15,15,15],[-100,0,100],color = 'white', lw = 3)
	plt.plot([45,45,45],[-100,0,100],color = 'white', lw = 3)
	plt.plot([-45,-45,-45],[-100,0,100],color = 'white', lw = 3)
	if len(y3) > 0:
		plt.plot([-45,-30,-15],[y3[0],y3[0],y3[0]],color = '#ADFF2F', lw = 3)
	if len(y4) > 0:
		plt.plot([15,30,45],[y4[0],y4[0],y4[0]],color = '#ADFF2F', lw = 3)
	if len(y5) > 0:
		plt.plot([-15,0,15],[y5[0],y5[0],y5[0]],color = '#ADFF2F', lw = 3)		
	if len(y6) > 0:
		plt.plot([-40,-30,-20],[y6[0],y6[0],y6[0]],color = 'red', lw = 3)		
	if len(y7) > 0:
		plt.plot([20,30,40],[y7[0],y7[0],y7[0]],color = 'red', lw = 3)		
	if len(y8) > 0:
		plt.plot([-10,0,10],[y8[0],y8[0],y8[0]],color = 'red', lw = 3)		
	if len(y9) > 0:
		plt.plot([-45,-30,-15],[y9[0],y9[0],y9[0]],color = '#ADFF2F', lw = 3)		
	if len(y10) > 0:
		plt.plot([15,30,45],[y10[0],y10[0],y10[0]],color = '#ADFF2F', lw = 3)		
	if len(y11) > 0:
		plt.plot([-15,0,15],[y11[0],y11[0],y11[0]],color = '#ADFF2F', lw = 3)		

	plt.axis('scaled')
	#plt.axis('equal') 	
	plt.axis([-75,75,-100,100])
	plt.axis([-75,75,-100,100])

	plt.scatter(x1,y1,marker='x',color='red')
	plt.scatter(x2,y2)
	filename = "%d.png" %i
	plt.savefig(filename)
	plt.draw()
	plt.pause(0.01)
	plt.clf()