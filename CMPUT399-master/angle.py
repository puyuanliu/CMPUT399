from time import sleep
from ev3dev.ev3 import *
#from move import *

from math import *
# Convert degree to radian
# Args: float
# Return: float
def deg_to_rad(d):
    return d*(pi/180)

def angle():
	# number 1 stands for the inner motor
	# number 2 stands for the outer motor
	motor_1 = LargeMotor(OUTPUT_A)
	motor_2 = LargeMotor(OUTPUT_B)
	lcd = Screen()
	ts = TouchSensor()
	motor_1.position = 0
	motor_2.position = 0
	#gear ratio
	gear_ratio = 56/24
	#length of the first(inner) arm link
	length_1 = 6.65
	#lenght of the 2nd(outer) arm link
	length_2 = 18.3
	#initialize a list that records the motor positons
	motor_coord = [] 
	btn = Button()
	counter = 0
	pressed_twice = False
	while not pressed_twice:
		if ts.is_pressed:
			motor_1_pos = deg_to_rad(motor_1.position)
			motor_2_pos = deg_to_rad(motor_2.position)
			counter +=1

			x_coord = length_2*cos((motor_1_pos/-gear_ratio)+motor_2_pos)+length_1*cos(motor_1_pos/-gear_ratio)
			y_coord = length_2*cos((motor_1_pos/-gear_ratio)+motor_2_pos)+length_1*cos(motor_1_pos/-gear_ratio)

			motor_coord.append(x_coord)
			motor_coord.append(y_coord)
			Sound.beep()
			print("x and y coordinate recorded")
			sleep(5)

		if counter == 3:
			pressed_twice = True
		sleep(1)
	first_point_x = motor_coord[0]
	print("first_point_x: ", first_point_x)
	first_point_y = motor_coord[1]
	print("first_point_y: ", first_point_y)
	second_point_x = motor_coord[2]
	print("second_point_x: ", second_point_x)
	second_point_y = motor_coord[3]
	print("second_point_y: ", second_point_y)
	third_point_x = motor_coord[4]
	print("third_point_x: ", third_point_x)
	third_point_y = motor_coord[5]
	print("third_point_y: ", third_point_y)

	d_1 = sqrt((second_point_x - first_point_x)**2 + (second_point_y - first_point_y)**2)
	print("distance between first_point and second_point: ",d_1)
	d_2 = sqrt((third_point_x - first_point_x)**2 + (third_point_y - first_point_y)**2)
	print("distance between first_point and third_point: ",d_2)
	#d_3 = sqrt((second_point_x - third_point_x)**2 + (third_point_y - second_point_x)**2)
	dot_product = (second_point_x*third_point_x)+(second_point_y*third_point_y)

	theta = acos(dot_product/(d_1*d_2))
	print(theta)
	theta_deg = theta*(180/pi)
	print("Theta in degrees",theta_deg)

	return theta
angle()



