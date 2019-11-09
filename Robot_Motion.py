# Robot_Motion.py

# A program to control Raspberry Pi Robots! 
# Written by Daniel Grimes & Justin Grimes.
# Licensed Under GNU GPLv3
# November 9th, 2019
# Version v1.1

#--------------------
# Inport the Raspberry Pi GPIO Library.
# Designed with an RPi 2 Model B 
import RPi.GPIO as GPIO
import time
#--------------------

#--------------------
# Set the numbering mode for GPIO pins to BCM style.
GPIO.setmode(GPIO.BCM)
#--------------------

#--------------------
# Set the amount of time for each command to last, in seconds.
ExecutionDuration = 0.5
#--------------------

#--------------------
# Set the mode for output GPIO pins used.
 # Motor 1
  # Red, M1A
  GPIO.setup(26, GPIO.OUT)
  # Orange, M1B
  GPIO.setup(19, GPIO.OUT)
 # Motor2
  # Brown, M2A
  GPIO.setup(20, GPIO.OUT)
  # Black, M2B
  GPIO.setup(21, GPIO.OUT)
 # Speaker
  # Red, Positive
  GPIO.setup(16, GPIO.OUT)
#--------------------

#--------------------
# Turn off motor one.
def Beep():
  GPIO.output(16, GPIO.HIGH)
  time.sleep(.2)
  GPIO.output(16, GPIO.LOW)
#--------------------

#--------------------
# Turn off motor one.
def MotorOneStop():
  GPIO.output(26, GPIO.LOW)
  GPIO.output(19, GPIO.LOW)
#--------------------

#--------------------
# Turn off motor two.
def MotorTwoStop():
  GPIO.output(20, GPIO.LOW)
  GPIO.output(21, GPIO.LOW)
#--------------------

#--------------------
# Turn off all motors.
def StopAllMotors():
  MotorOneStop()
  MotorTwoStop()
#--------------------

#--------------------
# Power motor one forwards.
def MotorOneForward():
  MotorOneStop()
  GPIO.output(26, GPIO.HIGH)
#--------------------

#--------------------
# Power motor two forwards.
def MotorTwoForward():
  MotorTwoStop()
  GPIO.output(20, GPIO.HIGH)
#--------------------

#--------------------
# Power motor one backwards.
def MotorOneReverse():
  MotorOneStop()
  GPIO.output(19, GPIO.HIGH)
#--------------------

#--------------------
# Power motor two backwards.
def MotorTwoReverse():
  MotorTwoStop()
  GPIO.output(21, GPIO.HIGH)
#--------------------

#--------------------
# Print some welcome text at the start of the program.
def PrintWelcomeText():
  print("\nA program to control Raspberry Pi Robots! \nWritten by Daniel Grimes & Justin Grimes.\nLicensed Under GNU GPLv3. \nNovember 9th, 2019. \n")
#--------------------

#--------------------
# Print some welcome text at the start of the program.
def PrintGoodbyeText():
  print("\nThanks for playing, Have a nice day! :) \n")
#--------------------


#--------------------
# The main logic of the program.
PrintWelcomeText()

KeyPress = ''

while KeyPress != 'q':

  KeyPress = input('\nEnter a command...')
  
  if KeyPress == 'w':
    MotorOneForward()
    MotorTwoForward()
  
  if KeyPress == 's':
  	MotorOneReverse()
  	MotorTwoReverse()
  
  if KeyPress == 'a':
  	MotorOneForward()
  	MotorTwoReverse()
  
  if KeyPress == 'd':
  	MotorTwoForward()
  	MotorOneReverse()
  
  time.sleep(ExecutionDuration)
  
  StopAllMotors()
  
  Beep()

PrintGoodbyeText()
#--------------------

  