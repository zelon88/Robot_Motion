# Robot_Motion_Listener.py

# A program to control Raspberry Pi Robots! 
# Written by Daniel Grimes & Justin Grimes.
# Licensed Under GNU GPLv3
# November 9th, 2019
# Version v1.0

# This version of the program listens for keyboard inputs
# with standard Python modules.

# Designed with an RPi 2 Model B 

#--------------------
# Import the Raspberry Pi GPIO Library.
import RPi.GPIO as GPIO
# Import the time library.
import time
# Import the keyboard module.
import keyboard
#--------------------

#--------------------
# Set the numbering mode for GPIO pins to BCM style.
GPIO.setmode(GPIO.BCM)
#--------------------

#--------------------
# Set the amount of time for each command to last, in seconds.
ExecutionDuration = 0.01
#--------------------

#--------------------
# Set the default speed to use before a speed has been specified.
DefaultSpeed = 9
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
# Send a beep to the speaker.
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
  print("\nA program to control Raspberry Pi Robots! \nWritten by Daniel Grimes & Justin Grimes.\nLicensed Under GNU GPLv3. \nNovember 9th, 2019. \nEnter a command...\n")
#--------------------

#--------------------
# Print some welcome text at the start of the program.
def PrintGoodbyeText():
  print("\nThanks for playing, Have a nice day! :) \n")
#--------------------

#--------------------
# The main logic of the program.
PrintWelcomeText()

while not keyboard.is_pressed('esc'):

  if not keyboard.is_pressed('w') and not keyboard.is_pressed('s') and not keyboard.is_pressed('a') and not keyboard.is_pressed('d'):
    StopAllMotors()
    
  if keyboard.is_pressed('w'):
    if not keyboard.is_pressed('d'):
      MotorOneForward()
    if not keyboard.is_pressed('a'):
      MotorTwoForward()
    Beep()
    
  if keyboard.is_pressed('s') :
    if not keyboard.is_pressed('d'):
      MotorOneReverse()
    if not keyboard.is_pressed('a'):
      MotorTwoReverse()
    Beep()
  
  if keyboard.is_pressed('a') and not keyboard.is_pressed('w') and not keyboard.is_pressed('s'):
    MotorOneForward()
    MotorTwoReverse()
    Beep()
  
  if keyboard.is_pressed('d') and not keyboard.is_pressed('w') and not keyboard.is_pressed('s'):
    MotorTwoForward()
    MotorOneReverse()
    Beep()
  
  #time.sleep(ExecutionDuration)

PrintGoodbyeText()
#--------------------
