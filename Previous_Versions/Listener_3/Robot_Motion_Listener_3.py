# Robot_Motion_Listener_3.py

# A program to control Raspberry Pi Robots! 
# Written by Daniel Grimes & Justin Grimes.
# Licensed Under GNU GPLv3
# October 22nd, 2022
# Version v1.0

# This version of the program listens for keyboard inputs
# with standard Python modules.

# Designed with an RPi 4 Model B 

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
# Set the Debug flag to True to enable additional output.
# Set the debug flag to False for optimal performance.
# This configuration entry has a significant impact on performance.
Debug = True
#--------------------

#--------------------
# Set the amount of time for each command to last, in seconds.
DefaultExecutionDuration = 1 / 1000
#--------------------

#--------------------
# Set the amount of time for each loop to last.
DefaultDwellDuration = 1 / 100
#--------------------

#--------------------
# Set the default speed to use before a speed has been specified.
DefaultSpeed = 0
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
  GPIO.output(16, GPIO.LOW)
#--------------------

#--------------------
# Update the speed setting for the motors.
def UpdateSpeed(RequestedSpeed, ExecDuration, DwellDuration, Debug):
  if Debug == True:
    print('\nCommand Detected. Updating Speed to '+str(RequestedSpeed)+'.')
  if RequestedSpeed == 0:
    ExecDuration = DwellDuration
  if RequestedSpeed > 0:
    ExecDuration = RequestedSpeed * RequestedSpeed
    ExecDuration = ExecDuration / 10000
  return ExecDuration
#--------------------

#--------------------
# Detect when a speed update is required.
def DetectSpeedChange(ExecDuration, DwellDuration, Debug):
  if keyboard.is_pressed('1'):
    ExecDuration = UpdateSpeed(1, ExecDuration, DwellDuration, Debug)
  if keyboard.is_pressed('2'):
    ExecDuration = UpdateSpeed(2, ExecDuration, DwellDuration, Debug)
  if keyboard.is_pressed('3'):
    ExecDuration = UpdateSpeed(3, ExecDuration, DwellDuration, Debug)
  if keyboard.is_pressed('4'):
    ExecDuration = UpdateSpeed(4, ExecDuration, DwellDuration, Debug)
  if keyboard.is_pressed('5'):
    ExecDuration = UpdateSpeed(5, ExecDuration, DwellDuration, Debug)
  if keyboard.is_pressed('6'):
    ExecDuration = UpdateSpeed(6, ExecDuration, DwellDuration, Debug)
  if keyboard.is_pressed('7'):
    ExecDuration = UpdateSpeed(7, ExecDuration, DwellDuration, Debug)
  if keyboard.is_pressed('8'):
    ExecDuration = UpdateSpeed(8, ExecDuration, DwellDuration, Debug)
  if keyboard.is_pressed('9'):
    ExecDuration = UpdateSpeed(9, ExecDuration, DwellDuration, Debug)
  if keyboard.is_pressed('0'):
    ExecDuration = UpdateSpeed(0, ExecDuration, DwellDuration, Debug)
  if Debug = True:
    print('\nThe Execution Duration is '+str(ExecDuration))
    print('\nThe Dwell Duration is '+str(DwellDuration))
  return ExecDuration
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
  #MotorOneStop()
  GPIO.output(26, GPIO.HIGH)
#--------------------

#--------------------
# Power motor two forwards.
def MotorTwoForward():
  #MotorTwoStop()
  GPIO.output(20, GPIO.HIGH)
#--------------------

#--------------------
# Power motor one backwards.
def MotorOneReverse():
  #MotorOneStop()
  GPIO.output(19, GPIO.HIGH)
#--------------------

#--------------------
# Power motor two backwards.
def MotorTwoReverse():
  #MotorTwoStop()
  GPIO.output(21, GPIO.HIGH)
#--------------------

#--------------------
def DetectMotion(Debug):
  if not keyboard.is_pressed('w') and not keyboard.is_pressed('s') and not keyboard.is_pressed('a') and not keyboard.is_pressed('d'):
    StopAllMotors()

  if keyboard.is_pressed('w'):
    if Debug == True:
      print('\nCommand Detected. Moving Forward.')
    if not keyboard.is_pressed('d'):
      MotorOneForward()
    if not keyboard.is_pressed('a'):
      MotorTwoForward()
    Beep()
    
  if keyboard.is_pressed('s'):
    if Debug == True:
      print('\nCommand Detected. Moving Backward.')
    if not keyboard.is_pressed('d'):
      MotorOneReverse()
    if not keyboard.is_pressed('a'):
      MotorTwoReverse()
    Beep()
  
  if keyboard.is_pressed('a') and not keyboard.is_pressed('w') and not keyboard.is_pressed('s'):
    if Debug == True: 
      print('\nCommand Detected. Moving Left.')
    MotorOneForward()
    MotorTwoReverse()
    Beep()
  
  if keyboard.is_pressed('d') and not keyboard.is_pressed('w') and not keyboard.is_pressed('s'):
    if Debug == True:
      print('\nCommand Detected. Moving Right.')
    MotorTwoForward()
    MotorOneReverse()
    Beep()
#--------------------

#--------------------
# Calculate the amount of sleep required to achieve the desired level of speed.
def PauseExecution(StartTime, FinishTime, ExecutionDuration, DefaultDwellDuration):
  ElapsedTime = StartTime - FinishTime
  if ElapsedTime <= ExecutionDuration:
    SleepDuration = ExecutionDuration - ElapsedTime
    #if Debug == True:
      #print('\nWaiting for '+str(SleepDuration)+' seconds.')
    time.sleep(SleepDuration)
  else:
    SleepDuration = 0
  DwellDuration = DefaultDwellDuration - SleepDuration
  if DwellDuration <= 0:
    DwellDuration = 0
  return DwellDuration
#--------------------

#--------------------
# Print some welcome text at the start of the program.
def PrintWelcomeText():
  print("\nA program to control Raspberry Pi Robots! \nWritten by Daniel Grimes & Justin Grimes.\nLicensed Under GNU GPLv3. \nJuly 10th, 2022. \nEnter a command...\n")
#--------------------

#--------------------
# Print some welcome text at the start of the program.
def PrintGoodbyeText():
  print("\nThanks for playing, Have a nice day! :) \n")
#--------------------

#--------------------
# The main logic of the program.
PrintWelcomeText()
ExecutionDuration = UpdateSpeed(DefaultSpeed, DefaultExecutionDuration, DefaultDwellDuration, Debug)
DwellDuration = DefaultDwellDuration

while not keyboard.is_pressed('esc'):

  StartTime = time.time()

  ExecutionDuration = DetectSpeedChange(ExecutionDuration, DwellDuration, Debug)

  DetectMotion(Debug)
  
  FinishTime = time.time()

  DwellDuration = PauseExecution(StartTime, FinishTime, ExecutionDuration, DefaultDwellDuration)

  StopAllMotors()
  
  time.sleep(DwellDuration)

PrintGoodbyeText()
#--------------------