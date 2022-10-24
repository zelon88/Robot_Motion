# APPLICATION NAME
#   Robot_Motion_Listener_4.py

# APPLICATION INFORMATION
#   Written by Daniel Grimes & Justin Grimes.
#   https://github.com/zelon88/Robot_Motion
#   Version v4.0, October 23rd, 2022
#   Licensed Under GNU GPLv3

# APPLICATION DESCRIPTION
#   A program to control Raspberry Pi Robots!
#   Turns a Raspberry Pi computer into an Electronic Speed Control (ESC) for dual motor robots!

# APPLICATION NOTES
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
#   Damage could result from connecting a DC motor directly to the GPIO pins of an RPi!
#   This application emulates the behavior of a simple MOSFET-style Electronic Speed Control (ESC).
#   Traditional MOSFET ESC's are capable of powering the motor directly from their output.
#   The RPi cannot power a motor directly from its GPIO pins. 
#   GPIO output to relays or non-ESC motor controller is required.
#   Compatible with Non-ESC Brushed DC Motor Controllers or standard relays.
#   Made to control tank-style robots with skid-steer drive configuirations.
#   The quality of relays or motor controllers used will determine overall performance.
#   Relays or motor controllers with high switching frequencies work best.
#   An RPi with a faster CPU & GPIO will allow for higher frequencies.

# GPIO PIN CONFIGURATION
#    Speaker
#      Pin 36, GPIO 16, Red, Positive
#      Pin 20, GND, Black, Negative
#    Motor 1
#      Pin 37, GPIO 26, Red, Positive, M1A
#      Pin 35, GPIO 19, Orange, Negative, M1B
#    Motor 2
#      Pin 38, GPIO 20, Brown, Positive, M2A
#      Pin 40, GPIO 21, Black, Negative, M2B
#--------------------



#--------------------
# Set a string containing the version of this application to display to the user.
VersionInfo = str('Version v4.0, October 23rd, 2022')
#--------------------

#--------------------
# Set the Debug flag to True to enable additional output.
# Set the Debug flag to False for optimal performance.
# This configuration entry has a significant impact on performance.
# Default is True.
# Once you have your robot fully configured change this to False.
Debug = bool(True)
#--------------------

#--------------------
# Set the number of iterations of the main loop to announce.
# Default is 100000. 
LoopAnnouncementInterval = int(100000)
#--------------------

#--------------------
# Set the maximum number of loops before the application terminates.
# Set to 0 to run an unlimited number of iterations until the Escape key is pressed.
# Default is 0.
MaxLoopCount = int(0)
#--------------------

#--------------------
# Set the amount of time for each loop to last.
# This controls how long each motor is unpowered during a move command.
# This controls the overall frequency of the speed control.
# This is basically controlling the MOSFET frequency in a traditional ESC.
# Must be smaller than the Execution Duration.
# Default is 1 / 100.
DefaultDwellDuration = float(1 / 100)
#--------------------

#--------------------
# Set the amount of time for each command to last, in seconds.
# This controls how long each motor is powered during a move command by default.
# This value is variable. The default value is only used during initialization.
# Must be larger than the Dwell Duration.
# Default is DefaultDwellDuration / 10.
DefaultExecutionDuration = float(DefaultDwellDuration / 10)
#--------------------

#--------------------
# Set the default speed to use before a speed has been specified.
# Default is 0.
DefaultSpeed = int(0)
#--------------------

#--------------------
# Set the default sensitivity for the speed controller.
# Faster boards means you can increase this number.
# Default is 10000.
DefaultSensitivity = int(10000)
#--------------------

#--------------------
# Set the welcome text that is displayed to the user when the program starts.
WelcomeText = str('A program to control Raspberry Pi Robots! \nWritten by Daniel Grimes & Justin Grimes.\nLicensed Under GNU GPLv3. \n'+str(VersionInfo)+'. \nEnter a command...\n')
#--------------------

#--------------------
# Set the goodbye text that is displayed to the user when the program closes.
GoodbyeText = str('Thanks for playing, Have a nice day! :) \n')
#--------------------

#--------------------
# Set whether or not to output an indicator beep to a simple speaker.
# Enabling speaker beep will reduce potential max frequency by BeepDuration.
EnableSpeakerBeep = bool(True)
#--------------------

#--------------------
# How long should indicator beeps last, in seconds.
# Default is DefaultExecutionTime / 100.
BeepDuration = float(100000 / 1)
#--------------------

#--------------------
# How long is the 'Bee' in the indicator beep?
BeDuration = float(BeepDuration / 3)
#--------------------

#--------------------
# How long is the 'Eep' in the indicator beep?
EpDuration = float(BeepDuration / 3)
#--------------------

#--------------------
# Print some welcome text at the start of the program.
def PrintWelcomeText(WelcomeText):
  print('\n'+WelcomeText)
#--------------------

#--------------------
# Print some welcome text at the start of the program.
def PrintGoodbyeText(GoodbyeText):
  print('\n'+GoodbyeText)
#--------------------

#--------------------
# Initialize required variables for the messaging environment.
def InitializeMessageCache():
  LastMessage, MessageText = 'Init', 'Message'
  return LastMessage, MessageText
#--------------------

#--------------------
# Initialize required variables for the loop tracking environment.
def InitializeLoopTracker():
  LoopCounter, LoopTracker = 0, 0
  return LoopCounter, LoopTracker
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
  if CurrentLoop >= MaxLoopCount:
    if Debug == True:
      LastMessage = PrintMessage(LastMessage, 'Execution has reached '+str(CurrentLoop)
        +' cycles. The maximum number of cycles allowed by configuration is '+str(MaxLoopCount)
        +' cycles. This application will now terminate.')
    BreakLoop = True 
  return LastMessage, LoopCounter, LoopTracker, BreakLoop
#--------------------

#--------------------
# Specify all the libraries to be loaded & the handles to use them.
def ImportLibraries(LastMessage):
  # Set somg error flags to indicate that no required libraries have been initialized yet.
  LibrariesLoaded, LibErrorA, LibErrorB = False, '', False

  # Import the Raspberry Pi GPIO Library.
  try:
    import RPi.GPIO as GPIO
  except ModuleNotFoundError as Err:
    LibErrorB = True
    if Debug == True:
      PrintMessage(LastMessage, 'Error Importing GPIO Library. '+str(LibErrorA))

  # Import the Time Library.
  try:
    import time as Time
  except ModuleNotFoundError as Err:
    LibErrorB = True
    if Debug == True:
      PrintMessage(LastMessage, 'Error Importing Time Library. '+str(LibErrorA))

  # Import the Keyboard Library.
  try:
    import keyboard as KB
  except ModuleNotFoundError as Err:
    LibErrorB = True
    if Debug == True:
      PrintMessage(LastMessage, 'Error Importing Keyboard Library. '+str(LibErrorA))

  # Consolidate error flags to determine if all required libraries have been fully initialized.
  if LibErrorB == False:
    LibrariesLoaded = True
  else:
    PrintMessage(LastMessage, 'Error Importing Required Libraries. Execution will now terminate. '+str(LibErrorA))
    exit()
  # Return the flag to the calling code as a sanity check.
  return LibrariesLoaded
#--------------------

#--------------------
# Initialize the software operating environment.
def InitializeSoftwareEnvironment(Debug):
  LastMessage, MessageText = InitializeMessageCache()
  if Debug == True:
    LastMessage = PrintMessage(LastMessage, 'Initializing Software Operating Environment.')
  LoopCounter, LoopTracker = InitializeLoopTracker()
  LibrariesLoaded = ImportLibraries(LastMessage)
  if Debug == True:
    LastMessage = PrintMessage(LastMessage, 'Software Operating Environment Initialized.')
  return LastMessage, MessageText, LoopCounter, LoopTracker
#--------------------

#--------------------
# Initialize the GPIO environment for a 40 pin Raspberry Pi.
def InitializeGPIO():
  # Set a flag to indicate that the GPIO is not initialized yet.
  GPIOStarted = False

  # Set the numbering mode for GPIO pins to BCM style.
  GPIO.setmode(GPIO.BCM)

  # Set the GPIO pin to use for controlling the speaker.
  #  Red, Positive
  GPIO.setup(16, GPIO.OUT)
  # ANY GROUNG PIN
  #  Black, Negative

  # Set the GPIO pins to use for controlling Motor 1.
  # Motor 1
  #  Red, Positive, M1A
  GPIO.setup(26, GPIO.OUT)
  #  Orange, Negative, M1B
  GPIO.setup(19, GPIO.OUT)

  # Set the GPIO pins to use for controlling Motor 2.
  # Motor 2
  #  Brown, Positive, M2A
  GPIO.setup(20, GPIO.OUT)
  #  Black, Negative, M2B
  GPIO.setup(21, GPIO.OUT)

  # Set a flag to indicate that the GPIO is fully initialized.
  GPIOStarted = True
  # Return the flag to the calling code as a sanity check.
  return GPIOStarted
#--------------------

#--------------------
# Craft a beep for the speaker, part 1.
def Be(BeDuration):
  GPIO.output(16, GPIO.HIGH)
  Time.sleep(BeDuration)
  GPIO.output(16, GPIO.LOW)
#--------------------

#--------------------
# Craft a beep for the speaker, part 2.
def Ep(BeDuration, EpDuration):
  Time.sleep(EpDuration)
  GPIO.output(16, GPIO.HIGH)
  Time.sleep(BeDuration)
  GPIO.output(16, GPIO.LOW)
#--------------------

#--------------------
# Command the speaker to beep.
def Beep(BeDuration, EpDuration, BeepDuration):
  Be(BeDuration)
  Ep(BeDuration, EpDuration)
#--------------------

#--------------------
# Update the speed setting for the motors.
def UpdateSpeed(RequestedSpeed, ExecDuration, DwellDuration, DefaultSensitivity, Debug):
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
def InitializeHardwareEnvironment(LastMessage, DefaultSpeed, DefaultExecutionDuration, DefaultDwellDuration, DefaultSensitivity, Debug):
  if Debug == True:
    LastMessage = PrintMessage(LastMessage, 'Initializing Hardware Operating Environment.')
  GPIOStarted = InitializeGPIO()
  ExecutionDuration, RequestedSpeed = UpdateSpeed(DefaultSpeed, DefaultExecutionDuration, DefaultDwellDuration, DefaultSensitivity, Debug)
  DwellDuration = DefaultDwellDuration
  return LastMessage, ExecutionDuration, RequestedSpeed, DwellDuration
#--------------------

#--------------------
# Initialize the entire operational environment for the application & attached hardware.
def InitializeEnvironment(DefaultSpeed, DefaultExecutionDuration, DefaultDwellDuration, DefaultSensitivity, Debug):
  BreakLoop = False
  LastMessage, MessageText, LoopCounter, LoopTracker = InitializeSoftwareEnvironment(Debug)
  LastMessage, ExecutionDuration, RequestedSpeed, DwellDuration = InitializeHardwareEnvironment(LastMessage, DefaultSpeed, DefaultExecutionDuration, DefaultDwellDuration, DefaultSensitivity, Debug)
  return LastMessage, MessageText, LoopCounter, LoopTracker, ExecutionDuration, RequestedSpeed, DwellDuration, BreakLoop
#--------------------

#--------------------
# Command motor channel one to stop.
def MotorOneStop():
  GPIO.output(26, GPIO.LOW)
  GPIO.output(19, GPIO.LOW)
#--------------------

#--------------------
# Command motor channel two to stop.
def MotorTwoStop():
  GPIO.output(20, GPIO.LOW)
  GPIO.output(21, GPIO.LOW)
#--------------------

#--------------------
# Command all motor channels to stop.
def StopAllMotors():
  MotorOneStop()
  MotorTwoStop()
#--------------------

#--------------------
# Command motor channel one to rotate forward.
def MotorOneForward():
  GPIO.output(26, GPIO.HIGH)
#--------------------

#--------------------
# Command motor channel two to rotate forward.
def MotorTwoForward():
  GPIO.output(20, GPIO.HIGH)
#--------------------

#--------------------
# Command motor channel one to rotate backward.
def MotorOneReverse():
  GPIO.output(19, GPIO.HIGH)
#--------------------

#--------------------
# Command motor channel two to rotate backward.
def MotorTwoReverse():
  GPIO.output(21, GPIO.HIGH)
#--------------------

#--------------------
# Command all motor channels to rotate forward.
def ForwardAllMotors():
  MotorOneForward()
  MotorTwoForward()
#--------------------

#--------------------
# Command all motor channels to rotate backward.
def BackwardAllMotors():
  MotorOneReverse()
  MotorTwoReverse()
#--------------------

#--------------------
# Detect when a speed update is required.
def DetectSpeedChange(LastMessage, ExecDuration, DwellDuration, DefaultSensitivity, Debug):
  if KB.is_pressed('1'):
    ExecDuration, RequestedSpeed = UpdateSpeed(1, ExecDuration, DwellDuration, DefaultSensitivity, Debug)
  if KB.is_pressed('2'):
    ExecDuration, RequestedSpeed = UpdateSpeed(2, ExecDuration, DwellDuration, DefaultSensitivity, Debug)
  if KB.is_pressed('3'):
    ExecDuration, RequestedSpeed = UpdateSpeed(3, ExecDuration, DwellDuration, DefaultSensitivity, Debug)
  if KB.is_pressed('4'):
    ExecDuration, RequestedSpeed = UpdateSpeed(4, ExecDuration, DwellDuration, DefaultSensitivity, Debug)
  if KB.is_pressed('5'):
    ExecDuration, RequestedSpeed = UpdateSpeed(5, ExecDuration, DwellDuration, DefaultSensitivity, Debug)
  if KB.is_pressed('6'):
    ExecDuration, RequestedSpeed = UpdateSpeed(6, ExecDuration, DwellDuration, DefaultSensitivity, Debug)
  if KB.is_pressed('7'):
    ExecDuration, RequestedSpeed = UpdateSpeed(7, ExecDuration, DwellDuration, DefaultSensitivity, Debug)
  if KB.is_pressed('8'):
    ExecDuration, RequestedSpeed = UpdateSpeed(8, ExecDuration, DwellDuration, DefaultSensitivity, Debug)
  if KB.is_pressed('9'):
    ExecDuration, RequestedSpeed = UpdateSpeed(9, ExecDuration, DwellDuration, DefaultSensitivity, Debug)
  if KB.is_pressed('0'):
    ExecDuration, RequestedSpeed = UpdateSpeed(0, ExecDuration, DwellDuration, DefaultSensitivity, Debug)
  if Debug == True:
    LastMessage = PrintMessage(LastMessage, 
      'Command Detected. Updating Speed to '+str(RequestedSpeed)
      +'.\nThe Ideal Execution Duration is '+str(ExecDuration)
      +'.\nThe Ideal Dwell Duration is '+str(DwellDuration)
      +'.\nThe Requested Speed is '+str(RequestedSpeed)+'.')
  return LastMessage, ExecDuration, RequestedSpeed
#--------------------

#--------------------
# Detect a request to stop all motors.
def DetectStopRequest(LastMessage, Debug):
  if not KB.is_pressed('w') and not KB.is_pressed('s') and not KB.is_pressed('a') and not KB.is_pressed('d'):
    if not KB.is_pressed('q') and not KB.is_pressed('z') and not KB.is_pressed('e') and not KB.is_pressed('c'):
      StopAllMotors()
      if Debug == True:
        LastMessage = PrintMessage(LastMessage, 'Command Detected. All Motors Stop Moving.')
  return LastMessage
#--------------------

#--------------------
# Detect a request to rotate all motors forward.
def DetectForwardRequest(LastMessage, Debug):
  Moving = False
  if KB.is_pressed('w'):
    if not KB.is_pressed('s') and not KB.is_pressed('d') and not KB.is_pressed('c'):
      MotorOneForward()
      Moving = True
    if not KB.is_pressed('s') and not KB.is_pressed('a') and not KB.is_pressed('z'):
      MotorTwoForward()
      Moving = True
    if Debug == True and Moving == True:
      LastMessage = PrintMessage(LastMessage, 'Command Detected. All Motors Moving Forward.')
    return LastMessage
#--------------------

#--------------------
# Detect a request to rotate all motors backward.
def DetectReverseRequest(LastMessage, Debug):
  Moving = False
  if KB.is_pressed('s'):
    if not KB.is_pressed('w') and not KB.is_pressed('a') and not KB.is_pressed('e'):
      MotorOneReverse()
      Moving = True
    if not KB.is_pressed('w') and not KB.is_pressed('d') and not KB.is_pressed('q'):
      MotorTwoReverse()
      Movine = True
    if Debug == True and Moving == True:
      LastMessage = PrintMessage(LastMessage, 'Command Detected. All Motors Moving Backward.')
    return LastMessage
#--------------------

#--------------------
# Detect a request to rotate all motors left.
def DetectLeftRequest(LastMessage, Debug):
  if KB.is_pressed('a'):
    if not KB.is_pressed('w') and not KB.is_pressed('s') and not KB.is_pressed('d') and not KB.is_pressed('c') and not KB.is_pressed('q'):
      if Debug == True: 
        LastMessage = PrintMessage(LastMessage, 'Command Detected. All Motors Moving Left.')
      MotorOneForward()
      MotorTwoReverse()
  return LastMessage
#--------------------

#--------------------
# Detect a request to rotate all motors right.
def DetectRightRequest(LastMessage, Debug):
  if KB.is_pressed('d'):
    if not KB.is_pressed('w') and not KB.is_pressed('s') and not KB.is_pressed('a') and not KB.is_pressed('z') and not KB.is_pressed('e'):
      MotorTwoForward()
      MotorOneReverse()
      if Debug == True:
        LastMessage = PrintMessage(LastMessage, 'Command Detected. All Motors Moving Right.')
  return LastMessage
#--------------------

#--------------------
# Detect a request to rotate left motors right.
def DetectLeftLimpRightRequest(LastMessage, Debug):
  if KB.is_pressed('q'):
    if not KB.is_pressed('s') and not KB.is_pressed('a') and not KB.is_pressed('z') and not KB.is_pressed('c'):
      MotorTwoForward()
      if Debug == True:
        LastMessage = PrintMessage(LastMessage, 'Command Detected. Left Motors Moving Right.')
  return LastMessage
#--------------------

#--------------------
# Detect a request to rotate left motors left.
def DetectLeftLimpLeftRequest(LastMessage, Debug):
  if KB.is_pressed('z'):
    if not KB.is_pressed('w') and not KB.is_pressed('d') and not KB.is_pressed('q'):
      MotorTwoReverse()
      if Debug == True:
        LastMessage = PrintMessage(LastMessage, 'Command Detected. Left Motors Moving Left.')
  return LastMessage
#--------------------

#--------------------
# Detect a request to rotate right motors left.
def DetectRightLimpLeftRequest(LastMessage, Debug):
  if KB.is_pressed('e'):
    if not KB.is_pressed('s') and not KB.is_pressed('d') and not KB.is_pressed('c'):
      MotorOneForward()
      if Debug == True:
        LastMessage = PrintMessage(LastMessage, 'Command Detected. Right Motors Moving Left.')
  return LastMessage
#--------------------

#--------------------
# Detect a request to rotate right motors right.
def DetectRightLimpRightRequest(LastMessage, Debug):
  if KB.is_pressed('c'):
    if not KB.is_pressed('w') and not KB.is_pressed('a') and not KB.is_pressed('e'):
      MotorOneReverse()
      if Debug == True:
        LastMessage = PrintMessage(LastMessage, 'Command Detected. Right Motors Moving Right.')
  return LastMessage
#--------------------

#--------------------
# Detect which motion is being requested & activate the corresponding motor command.
def DetectMotion(LastMessage, Debug):
  LastMessage = DetectStopRequest(LastMessage, Debug)
  LastMessage = DetectForwardRequest(LastMessage, Debug)
  LastMessage = DetectReverseRequest(LastMessage, Debug)
  LastMessage = DetectRightRequest(LastMessage, Debug)
  LastMessage = DetectLeftLimpRightRequest(LastMessage, Debug)
  LastMessage = DetectLeftLimpLeftRequest(LastMessage, Debug)
  LastMessage = DetectRightLimpLeftRequest(LastMessage, Debug)
  LastMessage = DetectRightLimpRightRequest(LastMessage, Debug)
  if EnableSpeakerBeep == True:
    Beep()
  return LastMessage
#--------------------

#--------------------
# Listen for requests from the user & call the appropriate procedure to accomplish it.
def ListenForRequests(LastMessage, ExecutionDuration, DwellDuration, DefaultSensitivity, Debug):
  StartTime = Time.time()
  LastMessage, ExecutionDuration, RequestedSpeed = DetectSpeedChange(LastMessage, ExecutionDuration, DwellDuration, DefaultSensitivity, Debug)
  LastMessage = DetectMotion(LastMessage, Debug)
  FinishTime = Time.time()
  return LastMessage, StartTime, FinishTime, ExecutionDuration, RequestedSpeed
#--------------------

#--------------------
# Calculate the amount of sleep required to achieve the desired level of speed.
def PauseExecution(LoopCounter, LastMessage, StartTime, FinishTime, ExecutionDuration, DwellDuration, RequestedSpeed):
  LoopCounter = LoopCounter + 1
  ElapsedTime = StartTime - FinishTime
  if ElapsedTime <= ExecutionDuration:
    SleepDuration = ExecutionDuration - ElapsedTime
    Time.sleep(SleepDuration)
  else:
    SleepDuration = 0
  DwellDuration = DefaultDwellDuration - SleepDuration
  if ExecutionDuration >= DwellDuration:
    DwellDuration = 0
  if not RequestedSpeed == 0:
    StopAllMotors()
    Time.sleep(DwellDuration)
  return LoopCounter, LastMessage, DwellDuration
#--------------------

#--------------------
# The main logic of the program.

# Print the welcome text.
PrintWelcomeText(WelcomeText)

# Initialize the operating environment.
LastMessage, MessageText, LoopCounter, LoopTracker, ExecutionDuration, RequestedSpeed, DwellDuration, BreakLoop = InitializeEnvironment(DefaultSpeed, DefaultExecutionDuration, DefaultDwellDuration, DefaultSensitivity, Debug)

# Start listening for keyboard input.
while not KB.is_pressed('esc'):
  
  # Listen for & process requests from user input.
  LastMessage, StartTime, FinishTime, ExecutionDuration, RequestedSpeed = ListenForRequests(LastMessage, ExecutionDuration, DwellDuration, DefaultSensitivity, Debug)

  # Throttle the application according to configuration settings & compute performance.
  LoopCounter, LastMessage, DwellDuration = PauseExecution(LastMessage, StartTime, FinishTime, ExecutionDuration, DefaultDwellDuration, RequestedSpeed)

  # Track & control application execution for debugging purposes. 
  LastMessage, LoopCounter, LoopTracker, BreakLoop = TrackLoops(LastMessage, LoopCounter, LoopTracker, LoopAnnouncementInterval, Debug)
  
  # Break the loop if the max loop counter has been reached.
  if BreakLoop == True:
    break

# Print the goodbye text.
PrintGoodbyeText(GoodbyeText)
#--------------------