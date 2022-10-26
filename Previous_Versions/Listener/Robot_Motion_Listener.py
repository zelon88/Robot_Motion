# Robot_Motion_Listener.py

# A program to control Raspberry Pi Robots! 
# Written by Daniel Grimes & Justin Grimes.
# Licensed Under GNU GPLv3
# November 9th, 2019
# Version v1.2

# This version of the program listens for keyboard inputs
# with pynput.

# Designed with an RPi 2 Model B 

#--------------------
# Import the Raspberry Pi GPIO Library.
import RPi.GPIO as GPIO
# Import the time library.
import time
# Import the keyboard module from the pynput library.
from pynput import keyboard
#--------------------

#--------------------
# Set the numbering mode for GPIO pins to BCM style.
GPIO.setmode(GPIO.BCM)
#--------------------

#--------------------
# Set the amount of time for each command to last, in seconds.
ExecutionDuration = 0.5
#--------------------

# -------------------
ValidKeys = ['w', 's', 'a', 'd', 'q']
# -------------------

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
# Start the keyboard listener using the pynput library.
def ListenForKeys():
  keyboard.Listener(on_press = On_Press, on_release = On_Release).start()
#--------------------

#--------------------
# Listen for when keys are pressed.
def On_Press(Key):
  # Listen for the w key to be pressed.
  # Powers all motors forwards.
  if Key == 'w':
    MotorOneForward()
    MotorTwoForward()
  # Listen for the s key to be pressed.
  # Powers all motors backwards.
  if Key == 's':
    MotorOneReverse()
    MotorTwoReverse()
  # Listen for the a key to be pressed.
  # Powers motor one forwards.
  # Powers motor two backwards.
  if Key == 'a':
    MotorOneForward()
    MotorTwoReverse()
  # Listen for the d key to be pressed.
  # Powers motor one backwards.
  # Powers motor two forwards.
  if Key == 'd':
    MotorTwoForward()
    MotorOneReverse()
  if Key == 'q':
    StopAllMotors()
    keyboard.Listener.stop
    PrintGoodbyeText()
    sys.exit(0)
#--------------------

#--------------------
# Listen for when keys are released.
def On_Release(Key):
  if Key in ValidKeys:
    StopAllMotors()
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

ListenForKeys()

while True:
  On_Press(Key)
  On_Release(Key)
#--------------------

  
