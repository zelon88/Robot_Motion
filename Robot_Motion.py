# APPLICATION NAME
#   Robot_Motion.py

# APPLICATION INFORMATION
#   Written by Daniel Grimes & Justin Grimes.
#   https://github.com/zelon88/Robot_Motion
#   Version v4.3, October 27th, 2022
#   Licensed Under GNU GPLv3

# APPLICATION DESCRIPTION
#   An application to control Raspberry Pi Robots!
#   Turns a Raspberry Pi computer into a dual motor Electronic Speed Control (ESC)!

# APPLICATION NOTES
#   This application emulates the signal behavior of a simple MOSFET-style Electronic Speed Control (ESC).
#   This application must be run as root in order to access the GPIO pins.
#   This application tries to accomodate for CPU speed & performance.
#   This application will provide full motor power if the CPU or GPIO cannot achieve the specified frequency.
#   This application provides variable speed motor control for two motor channels.
#   Motor count is arbitrary. Each channel can support multiple motors if the supply relays are adequate.

# HARDWARE NOTES: 
#   Tested with an RPi2 Model B & an RPi4 Model B.
#   Compatible with all RPi boards with 40 pin GPIO headers.
#   Compatible with Brushed DC Electric Motors.
#   Not to be used to directly power motors from RPi GPIO pins!
#   Damage will result from connecting a DC motor directly to the GPIO pins of an RPi!
#   Traditional MOSFET ESC's are capable of powering the motor directly from their output.
#   GPIO output to relays or non-ESC motor controller is required.
#   Compatible with Non-ESC Brushed DC Motor Controllers or standard relays.
#   Made to control tank-style robots with skid-steer drive configuirations.
#   The quality of relays or motor controllers used will determine overall performance.
#   Relays or motor controllers with high switching frequencies work best.
#   An RPi with a faster CPU & GPIO will allow for higher frequencies.

# DEFAULT GPIO PIN CONFIGURATION
#   Numbering Style:  BCM
#    Speaker
#      Pin 36, GPIO 16, Red, Positive
#      Pin 20, GND, Black, Negative
#    Motor Relay 1
#      Pin 37, GPIO 26, Red, Positive, M1A
#      Pin 35, GPIO 19, Orange, Negative, M1B
#    Motor Relay 2
#      Pin 38, GPIO 20, Brown, Positive, M2A
#      Pin 40, GPIO 21, Black, Negative, M2B
#--------------------

#--------------------
# Initialize required variables for the messaging environment.
def InitializeMessageCache():
  LastMessage, MessageText = 'Init', 'Message'
  return LastMessage, MessageText
#--------------------

#--------------------
# Print a static message to the console.
def PrintText(Text):
  print('\n'+str(Text))
#--------------------

#--------------------
# Print a message to the console without duplicating the last message.
def PrintMessage(LastMessage, MessageText):
  if not str(LastMessage) == str(MessageText):
    print('\n'+str(MessageText))
    LastMessage = MessageText
  return(LastMessage)
#--------------------

#--------------------
# Initialize required variables for the loop tracking environment.
def InitializeLoopTracker():
  LoopCounter, LoopTracker = 0, 0
  return LoopCounter, LoopTracker
#--------------------

#--------------------
# Track the number of iterations of the main loop for debugging purposes.
def TrackLoops(LastMessage, LoopCounter, LoopTracker, LoopAnnouncementInterval, MaxLoopCount, Debug):
  BreakLoop = False
  LoopAnnouncementInterval = LoopAnnouncementInterval
  CurrentLoop = LoopTracker + LoopCounter
  if LoopCounter == LoopAnnouncementInterval:
    LoopTracker = CurrentLoop
    LoopCounter = 0
    if Debug == True:
      LastMessage = PrintMessage(LastMessage, 'Execution has reached '+str(LoopTracker)+' cycles of the main loop.')
  if MaxLoopCount != 0:
    if CurrentLoop >= MaxLoopCount:
      if Debug == True:
        LastMessage = PrintText('Execution has reached '+str(CurrentLoop)+' cycles. The maximum number of cycles allowed by configuration is '+str(MaxLoopCount)+' cycles. This application will now terminate.')
      BreakLoop = True 
  return LastMessage, LoopCounter, LoopTracker, BreakLoop
#--------------------

#--------------------
# Specify all the libraries to be loaded & the handles to use them.
def ImportLibraries(LastMessage):
  # Set somg error flags to default values.
  LibErrorA, LibErrorB = '', False
  # Import the Raspberry Pi GPIO Library.
  try:
    import RPi.GPIO as GPIO
  except ModuleNotFoundError as LibErrorA:
    LibErrorB = True
    if Debug == True:
      PrintMessage(LastMessage, 'Captured Exception: '+str(LibErrorA))
  # Import the Time Library.
  try:
    import time as Time
  except ModuleNotFoundError as LibErrorA:
    LibErrorB = True
    if Debug == True:
      PrintMessage(LastMessage, 'Captured Exception: '+str(LibErrorA))
  # Import the Keyboard Library.
  try:
    import keyboard as KB
  except ModuleNotFoundError as LibErrorA:
    LibErrorB = True
    if Debug == True:
      PrintMessage(LastMessage, 'Captured Exception: '+str(LibErrorA))
  # Consolidate error flags to determine if any errors happened.
  if LibErrorB != False:
    PrintMessage(LastMessage, 'Error 1: Could Not Import Required Libraries. \nThis application will now terminate.')
    exit()
  return LastMessage, GPIO, Time, KB
#--------------------

#--------------------
# Initialize the software operating environment.
def InitializeSoftwareEnvironment(Debug):
  LastMessage, MessageText = InitializeMessageCache()
  if Debug == True:
    LastMessage = PrintMessage(LastMessage, 'Initializing Software Operating Environment.')
  LoopCounter, LoopTracker = InitializeLoopTracker()
  LastMessage, GPIO, Time, KB = ImportLibraries(LastMessage)
  if Debug == True:
    LastMessage = PrintMessage(LastMessage, 'Software Operating Environment Initialized.')
  return LastMessage, MessageText, LoopCounter, LoopTracker, GPIO, Time, KB
#--------------------

#--------------------
# Initialize the GPIO environment for a 40 pin Raspberry Pi.
def InitializeGPIO(GPIO, GPIOMode, GPIOWarnings, SpeakerGPIO, MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO, MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO):
  # Set a flag to indicate that the GPIO is not initialized yet.
  GPIOStarted = False
  # Set the GPIO warning level.
  if GPIOWarnings == True:
    GPIO.setwarnings(True)
  else:
    GPIO.setwarnings(False)
  # Set the numbering mode for GPIO pins.
  if GPIOMode == 'BCM':
    GPIO.setmode(GPIO.BCM)
  if GPIOMode == 'BOARD':
    GPIO.setmode(GPIO.BOARD)
  # Set the GPIO pin to use for controlling the speaker.
  #  Red, Positive
  GPIO.setup(SpeakerGPIO, GPIO.OUT)
  # ANY GROUND PIN
  #  Black, Negative
  # Set the GPIO pins to use for controlling Motor Relay 1.
  # Motor Relay 1
  #  Red, Positive, M1A
  GPIO.setup(MotorRelayOnePositiveGPIO, GPIO.OUT)
  #  Orange, Negative, M1B
  GPIO.setup(MotorRelayOneNegativeGPIO, GPIO.OUT)
  # Set the GPIO pins to use for controlling Motor Relay 2.
  # Motor Relay 2
  #  Brown, Positive, M2A
  GPIO.setup(MotorRelayTwoPositiveGPIO, GPIO.OUT)
  #  Black, Negative, M2B
  GPIO.setup(MotorRelayTwoNegativeGPIO, GPIO.OUT)
  # Set a flag to indicate that the GPIO is fully initialized.
  GPIOStarted = True
  # Return the flag to the calling code as a sanity check.
  return GPIOStarted, GPIO
#--------------------

#--------------------
# Craft a beep for the speaker, part 1.
def Be(SpeakerGPIO, BeDuration, Time):
  GPIO.output(SpeakerGPIO, GPIO.HIGH)
  Time.sleep(BeDuration)
  GPIO.output(SpeakerGPIO, GPIO.LOW)
#--------------------

#--------------------
# Craft a beep for the speaker, part 2.
def Ep(SpeakerGPIO, BeDuration, EpDuration, Time):
  Time.sleep(EpDuration)
  GPIO.output(SpeakerGPIO, GPIO.HIGH)
  Time.sleep(BeDuration)
  GPIO.output(SpeakerGPIO, GPIO.LOW)
#--------------------

#--------------------
# Command the speaker to beep.
def Beep(SpeakerGPIO, BeDuration, EpDuration, Time):
  Be(SpeakerGPIO, BeDuration, Time)
  Ep(SpeakerGPIO, BeDuration, EpDuration, Time)
#--------------------

#--------------------
# Update the speed setting for the motors.
def UpdateSpeed(RequestedSpeed, ExecDuration, DwellDuration, DefaultSensitivity):
  RequestedSpeed = int(RequestedSpeed)
  if RequestedSpeed > 9:
    RequestedSpeed = 0
  if RequestedSpeed == 0:
    ExecDuration = DwellDuration
  if RequestedSpeed > 0 and RequestedSpeed <= 9:
    ExecDuration = RequestedSpeed * RequestedSpeed
    ExecDuration = ExecDuration / DefaultSensitivity
  return ExecDuration, RequestedSpeed
#--------------------

#--------------------
# Initialize the hardware operating environment.
def InitializeHardwareEnvironment(LastMessage, GPIO, GPIOWarnings, SpeakerGPIO, MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO, MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO, DefaultSpeed, DefaultExecutionDuration, DefaultDwellDuration, DefaultSensitivity, Debug):
  if Debug == True:
    LastMessage = PrintMessage(LastMessage, 'Initializing Hardware Operating Environment.')
  GPIOStarted, GPIO = InitializeGPIO(GPIO, GPIOMode, GPIOWarnings, SpeakerGPIO, MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO, MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO)
  ExecutionDuration, CurrentSpeed = UpdateSpeed(DefaultSpeed, DefaultExecutionDuration, DefaultDwellDuration, DefaultSensitivity)
  DwellDuration = DefaultDwellDuration
  return LastMessage, ExecutionDuration, CurrentSpeed, DwellDuration
#--------------------

#--------------------
# Initialize the entire operational environment for the application & attached hardware.
def InitializeEnvironment(SpeakerGPIO, MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO, MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO, DefaultSpeed, DefaultExecutionDuration, DefaultDwellDuration, DefaultSensitivity, Debug):
  BreakLoop = False
  LastMessage, MessageText, LoopCounter, LoopTracker, GPIO, Time, KB = InitializeSoftwareEnvironment(Debug)
  LastMessage, ExecutionDuration, CurrentSpeed, DwellDuration = InitializeHardwareEnvironment(LastMessage, GPIO, GPIOWarnings, SpeakerGPIO, MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO, MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO, DefaultSpeed, DefaultExecutionDuration, DefaultDwellDuration, DefaultSensitivity, Debug)
  return LastMessage, MessageText, LoopCounter, LoopTracker, ExecutionDuration, CurrentSpeed, DwellDuration, BreakLoop, GPIO, Time, KB
#--------------------

#--------------------
# Command motor channel one to stop.
def MotorOneStop(MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO):
  GPIO.output(MotorRelayOnePositiveGPIO, GPIO.LOW)
  GPIO.output(MotorRelayOneNegativeGPIO, GPIO.LOW)
#--------------------

#--------------------
# Command motor channel two to stop.
def MotorTwoStop(MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO):
  GPIO.output(MotorRelayTwoPositiveGPIO, GPIO.LOW)
  GPIO.output(MotorRelayTwoNegativeGPIO, GPIO.LOW)
#--------------------

#--------------------
# Command all motor channels to stop.
def StopAllMotors(MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO, MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO):
  MotorOneStop(MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO)
  MotorTwoStop(MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO)
#--------------------

#--------------------
# Command motor channel one to rotate forward.
def MotorOneForward(MotorRelayOnePositiveGPIO):
  GPIO.output(MotorRelayOnePositiveGPIO, GPIO.HIGH)
#--------------------

#--------------------
# Command motor channel two to rotate forward.
def MotorTwoForward(MotorRelayTwoPositiveGPIO):
  GPIO.output(MotorRelayTwoPositiveGPIO, GPIO.HIGH)
#--------------------

#--------------------
# Command motor channel one to rotate backward.
def MotorOneReverse(MotorRelayOneNegativeGPIO):
  GPIO.output(MotorRelayOneNegativeGPIO, GPIO.HIGH)
#--------------------

#--------------------
# Command motor channel two to rotate backward.
def MotorTwoReverse(MotorRelayTwoNegativeGPIO):
  GPIO.output(MotorRelayTwoNegativeGPIO, GPIO.HIGH)
#--------------------

#--------------------
# Command all motor channels to rotate forward.
def ForwardAllMotors(MotorRelayOnePositiveGPIO, MotorRelayTwoPositiveGPIO):
  MotorOneForward(MotorRelayOnePositiveGPIO)
  MotorTwoForward(MotorRelayTwoPositiveGPIO)
#--------------------

#--------------------
# Command all motor channels to rotate backward.
def BackwardAllMotors(MotorRelayOneNegativeGPIO, MotorRelayTwoNegativeGPIO):
  MotorOneReverse(MotorRelayOneNegativeGPIO)
  MotorTwoReverse(MotorRelayTwoNegativeGPIO)
#--------------------

#--------------------
# Detect when a speed update is required.
def DetectSpeedChange(LastMessage, ExecDuration, DwellDuration, DefaultSensitivity, CurrentSpeed, KB, Debug):
  OriginalSpeed = CurrentSpeed
  if KB.is_pressed('1'):
    ExecDuration, CurrentSpeed = UpdateSpeed(1, ExecDuration, DwellDuration, DefaultSensitivity)
  if KB.is_pressed('2'):
    ExecDuration, CurrentSpeed = UpdateSpeed(2, ExecDuration, DwellDuration, DefaultSensitivity)
  if KB.is_pressed('3'):
    ExecDuration, CurrentSpeed = UpdateSpeed(3, ExecDuration, DwellDuration, DefaultSensitivity)
  if KB.is_pressed('4'):
    ExecDuration, CurrentSpeed = UpdateSpeed(4, ExecDuration, DwellDuration, DefaultSensitivity)
  if KB.is_pressed('5'):
    ExecDuration, CurrentSpeed = UpdateSpeed(5, ExecDuration, DwellDuration, DefaultSensitivity)
  if KB.is_pressed('6'):
    ExecDuration, CurrentSpeed = UpdateSpeed(6, ExecDuration, DwellDuration, DefaultSensitivity)
  if KB.is_pressed('7'):
    ExecDuration, CurrentSpeed = UpdateSpeed(7, ExecDuration, DwellDuration, DefaultSensitivity)
  if KB.is_pressed('8'):
    ExecDuration, CurrentSpeed = UpdateSpeed(8, ExecDuration, DwellDuration, DefaultSensitivity)
  if KB.is_pressed('9'):
    ExecDuration, CurrentSpeed = UpdateSpeed(9, ExecDuration, DwellDuration, DefaultSensitivity)
  if KB.is_pressed('0'):
    ExecDuration, CurrentSpeed = UpdateSpeed(0, ExecDuration, DwellDuration, DefaultSensitivity)
  if OriginalSpeed != CurrentSpeed:
    if Debug == True:
      LastMessage = PrintMessage(LastMessage, 'Command Detected. Update Speed to '+str(CurrentSpeed)+'.\nThe Execution Duration is '+str(ExecDuration)+'.\nThe Dwell Duration is '+str(DwellDuration)+'.')
  return LastMessage, ExecDuration, CurrentSpeed
#--------------------

#--------------------
# Detect a request to stop all motors.
def DetectStopRequest(LastMessage, KB, MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO, MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO, Debug):
  CheckOne, CheckTwo = False, False
  if not KB.is_pressed('w') and not KB.is_pressed('s') and not KB.is_pressed('a') and not KB.is_pressed('d'):
    CheckOne = True
  if not KB.is_pressed('q') and not KB.is_pressed('z') and not KB.is_pressed('e') and not KB.is_pressed('c'):
    CheckTwo = True
  if CheckOne == True and CheckTwo == True:
    StopAllMotors(MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO, MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO)
    if Debug == True:
      LastMessage = PrintMessage(LastMessage, 'Command Detected. All Motors Stop Moving.')
  return LastMessage
#--------------------

#--------------------
# Detect a request to rotate all motors forward.
def DetectForwardRequest(LastMessage, KB, MotorRelayOnePositiveGPIO, MotorRelayTwoPositiveGPIO, Debug):
  LastMessage = LastMessage
  Moving = False
  if KB.is_pressed('w'):
    if not KB.is_pressed('s') and not KB.is_pressed('d') and not KB.is_pressed('c'):
      MotorOneForward(MotorRelayOnePositiveGPIO)
      Moving = True
    if not KB.is_pressed('s') and not KB.is_pressed('a') and not KB.is_pressed('z'):
      MotorTwoForward(MotorRelayTwoPositiveGPIO)
      Moving = True
    if Debug == True and Moving == True:
      LastMessage = PrintMessage(LastMessage, 'Command Detected. All Motors Moving Forward.')
  return LastMessage
#--------------------

#--------------------
# Detect a request to rotate all motors backward.
def DetectReverseRequest(LastMessage, KB, MotorRelayOneNegativeGPIO, MotorRelayTwoNegativeGPIO, Debug):
  Moving = False
  if KB.is_pressed('s'):
    if not KB.is_pressed('w') and not KB.is_pressed('a') and not KB.is_pressed('e'):
      MotorOneReverse(MotorRelayOneNegativeGPIO)
      Moving = True
    if not KB.is_pressed('w') and not KB.is_pressed('d') and not KB.is_pressed('q'):
      MotorTwoReverse(MotorRelayTwoNegativeGPIO)
      Moving = True
    if Debug == True and Moving == True:
      LastMessage = PrintMessage(LastMessage, 'Command Detected. All Motors Moving Backward.')
  return LastMessage
#--------------------

#--------------------
# Detect a request to rotate all motors left.
def DetectLeftRequest(LastMessage, KB, MotorRelayOnePositiveGPIO, MotorRelayTwoNegativeGPIO, Debug):
  if KB.is_pressed('a'):
    if not KB.is_pressed('w') and not KB.is_pressed('s') and not KB.is_pressed('d') and not KB.is_pressed('c') and not KB.is_pressed('q'):
      if Debug == True: 
        LastMessage = PrintMessage(LastMessage, 'Command Detected. All Motors Moving Left.')
      MotorOneForward(MotorRelayOnePositiveGPIO)
      MotorTwoReverse(MotorRelayTwoNegativeGPIO)
  return LastMessage
#--------------------

#--------------------
# Detect a request to rotate all motors right.
def DetectRightRequest(LastMessage, KB, MotorRelayTwoPositiveGPIO, MotorRelayOneNegativeGPIO, Debug):
  if KB.is_pressed('d'):
    if not KB.is_pressed('w') and not KB.is_pressed('s') and not KB.is_pressed('a') and not KB.is_pressed('z') and not KB.is_pressed('e'):
      MotorTwoForward(MotorRelayTwoPositiveGPIO)
      MotorOneReverse(MotorRelayOneNegativeGPIO)
      if Debug == True:
        LastMessage = PrintMessage(LastMessage, 'Command Detected. All Motors Moving Right.')
  return LastMessage
#--------------------

#--------------------
# Detect a request to rotate left motors right.
def DetectLeftLimpRightRequest(LastMessage, KB, MotorRelayTwoPositiveGPIO, Debug):
  if KB.is_pressed('q'):
    if not KB.is_pressed('s') and not KB.is_pressed('a') and not KB.is_pressed('z') and not KB.is_pressed('c'):
      MotorTwoForward(MotorRelayTwoPositiveGPIO)
      if Debug == True:
        LastMessage = PrintMessage(LastMessage, 'Command Detected. Left Motors Moving Right.')
  return LastMessage
#--------------------

#--------------------
# Detect a request to rotate left motors left.
def DetectLeftLimpLeftRequest(LastMessage, KB, MotorRelayTwoNegativeGPIO, Debug):
  if KB.is_pressed('z'):
    if not KB.is_pressed('w') and not KB.is_pressed('d') and not KB.is_pressed('q'):
      MotorTwoReverse(MotorRelayTwoNegativeGPIO)
      if Debug == True:
        LastMessage = PrintMessage(LastMessage, 'Command Detected. Left Motors Moving Left.')
  return LastMessage
#--------------------

#--------------------
# Detect a request to rotate right motors left.
def DetectRightLimpLeftRequest(LastMessage, KB, MotorRelayOnePositiveGPIO, Debug):
  if KB.is_pressed('e'):
    if not KB.is_pressed('s') and not KB.is_pressed('d') and not KB.is_pressed('c'):
      MotorOneForward(MotorRelayOnePositiveGPIO)
      if Debug == True:
        LastMessage = PrintMessage(LastMessage, 'Command Detected. Right Motors Moving Left.')
  return LastMessage
#--------------------

#--------------------
# Detect a request to rotate right motors right.
def DetectRightLimpRightRequest(LastMessage, KB, MotorRelayOneNegativeGPIO, Debug):
  if KB.is_pressed('c'):
    if not KB.is_pressed('w') and not KB.is_pressed('a') and not KB.is_pressed('e'):
      MotorOneReverse(MotorRelayOneNegativeGPIO)
      if Debug == True:
        LastMessage = PrintMessage(LastMessage, 'Command Detected. Right Motors Moving Right.')
  return LastMessage
#--------------------

#--------------------
# Detect which motion is being requested & activate the corresponding motor command.
def DetectMotion(LastMessage, BeDuration, EpDuration, EnableSpeakerBeep, SpeakerGPIO, MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO, MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO, Time, KB, Debug):
  LastMessage = DetectStopRequest(LastMessage, KB, MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO, MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO, Debug)
  LastMessage = DetectForwardRequest(LastMessage, KB, MotorRelayOnePositiveGPIO, MotorRelayTwoPositiveGPIO, Debug)
  LastMessage = DetectReverseRequest(LastMessage, KB, MotorRelayOneNegativeGPIO, MotorRelayTwoNegativeGPIO, Debug)
  LastMessage = DetectLeftRequest(LastMessage, KB, MotorRelayOnePositiveGPIO, MotorRelayTwoNegativeGPIO, Debug)
  LastMessage = DetectRightRequest(LastMessage, KB, MotorRelayTwoPositiveGPIO, MotorRelayOneNegativeGPIO, Debug)
  LastMessage = DetectLeftLimpRightRequest(LastMessage, KB, MotorRelayTwoPositiveGPIO, Debug)
  LastMessage = DetectLeftLimpLeftRequest(LastMessage, KB, MotorRelayTwoNegativeGPIO, Debug)
  LastMessage = DetectRightLimpLeftRequest(LastMessage, KB, MotorRelayOnePositiveGPIO, Debug)
  LastMessage = DetectRightLimpRightRequest(LastMessage, KB, MotorRelayOneNegativeGPIO, Debug)
  if EnableSpeakerBeep == True:
    Beep(SpeakerGPIO, BeDuration, EpDuration, Time)
  return LastMessage
#--------------------

#--------------------
# Listen for requests from the user & call the appropriate procedure to accomplish it.
def ListenForRequests(LastMessage, ExecutionDuration, DwellDuration, DefaultSensitivity, CurrentSpeed, BeDuration, EpDuration, EnableSpeakerBeep, SpeakerGPIO, MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO, MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO, Time, KB, Debug):
  StartTime = Time.time()
  LastMessage, ExecutionDuration, CurrentSpeed = DetectSpeedChange(LastMessage, ExecutionDuration, DwellDuration, DefaultSensitivity, CurrentSpeed, KB, Debug)
  LastMessage = DetectMotion(LastMessage, BeDuration, EpDuration, EnableSpeakerBeep, SpeakerGPIO, MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO, MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO, Time, KB, Debug)
  FinishTime = Time.time()
  return LastMessage, StartTime, FinishTime, ExecutionDuration, CurrentSpeed
#--------------------

#--------------------
# Calculate the amount of sleep required to achieve the desired level of speed.
def PauseExecution(LoopCounter, LastMessage, StartTime, FinishTime, ExecutionDuration, DwellDuration, Time, CurrentSpeed):
  LoopCounter = LoopCounter + 1
  ElapsedTime = StartTime - FinishTime
  if ElapsedTime <= ExecutionDuration:
    SleepDuration = ExecutionDuration - ElapsedTime
    Time.sleep(SleepDuration)
  else:
    SleepDuration = 0
  DwellDuration = DwellDuration - SleepDuration
  if CurrentSpeed != 0:
    StopAllMotors(MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO, MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO)
  if DwellDuration > 0:
    Time.sleep(DwellDuration)
  return LoopCounter, LastMessage, DwellDuration
#--------------------

#--------------------
# The main logic of the application.

# Import the configuration variables located in Robot_Motion_Config.py.
try:
  from Robot_Motion_Config import *
except ModuleNotFoundError as ConfigError:
  PrintText('Captured Exception: '+str(ConfigError))
  PrintText('Error 2: Could Not Import Configuration File. \nThis application will now terminate.')
  exit()

# Print the start text.
PrintText(StartText)

# Initialize the operating environment.
LastMessage, MessageText, LoopCounter, LoopTracker, ExecutionDuration, CurrentSpeed, DwellDuration, BreakLoop, GPIO, Time, KB = InitializeEnvironment(SpeakerGPIO, MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO, MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO, DefaultSpeed, DefaultExecutionDuration, DefaultDwellDuration, DefaultSensitivity, Debug)

# Print the welcome text.
PrintText(WelcomeText)

# Start listening for requests from keyboard input.
# Break out of this loop if the max loop counter has been reached or if the Esc key is pressed.
while BreakLoop == False and not KB.is_pressed('esc'):

  # Listen for & process requests from user input.
  LastMessage, StartTime, FinishTime, ExecutionDuration, CurrentSpeed = ListenForRequests(LastMessage, ExecutionDuration, DwellDuration, DefaultSensitivity, CurrentSpeed, BeDuration, EpDuration, EnableSpeakerBeep, SpeakerGPIO, MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO, MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO, Time, KB, Debug)

  # Throttle the application according to configuration settings & compute performance.
  LoopCounter, LastMessage, DwellDuration = PauseExecution(LoopCounter, LastMessage, StartTime, FinishTime, ExecutionDuration, DefaultDwellDuration, Time, CurrentSpeed)

  # Track & control application execution for debugging purposes. 
  LastMessage, LoopCounter, LoopTracker, BreakLoop = TrackLoops(LastMessage, LoopCounter, LoopTracker, LoopAnnouncementInterval, MaxLoopCount, Debug)

# Print the goodbye text.
PrintText(GoodbyeText)
#--------------------