#--------------------
# APPLICATION NAME
#   Robot_Motion.py

# APPLICATION INFORMATION
#   Written by Daniel Grimes & Justin Grimes.
#   https://github.com/zelon88/Robot_Motion
#   Version v4.5, November 1st, 2022
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

# DEFAULT KEYBOARD CONFIGURATION
#   Move Forward:                           W
#   Move Backward:                          S
#   Move Left:                              A
#   Move Right:                             D
#   Move Left (Left Channel Only):          Z
#   Move Right (Left Channel Only):         Q
#   Move Left (Right Channel Only):         E
#   Move Right (Right Channel Only):        C
#   Increase Sensitivity:                   ]
#   Decrease Sensitivity:                   [
#   Increase Speed by 1:                    =
#   Decrease Speed by 1:                    -
#   Set Speed To Minimum:                   1
#   Set Speed To Level 2:                   2
#   Set Speed To Level 3:                   3
#   Set Speed To Level 4:                   4
#   Set Speed To Level 5:                   5
#   Set Speed To Level 6:                   6
#   Set Speed To Level 7:                   7
#   Set Speed To Level 8:                   8
#   Set Speed To Level 9:                   9
#   Set Speed To Level 10:                  0
#   Close Application:                      Esc

# <3 Open-Source
#--------------------

#--------------------
# Print a static message to the console.
# Set Text to a string of text to print to the console.
def PrintText(Text):
  # An 80 character divider to make reading console output easier.
  Divider = '\n--------------------------------------------------------------------------------'
  # Format the message text as a string variable & print it to the console with a newline at the beginning.
  print(str(Text+Divider))
#--------------------

#--------------------
# Print a message to the console without duplicating the last message.
# Set LastMessage to LastMessage. Always.
# Set MessageText to a string of text to print to the console.
def PrintMessage(LastMessage, MessageText):
  # Compare the two messages to each other & only continue if they are not identical.
  if not str(LastMessage) == str(MessageText):
    # Print the current message to the console.
    PrintText(MessageText)
    # Set the last message variable to the message that was just displayed.
    LastMessage = MessageText
  return LastMessage
#--------------------

#--------------------
# Print an error message to the console.
# Set ErrorNumber to a unique number for the error being displayed.
# Set ErrorMessage to a string of text to print to the console.
# Set Fatal to True to kill the script after displaying the error.
# Set Fatal to False to allow execution to continue after displaying the error.
# Do not use fatal errors inside the loop.
# If you terminate the application while GPIO pins are activated they will remain active until manually deactivated.
def PrintError(ErrorNumber, ErrorMessage, Fatal):
  # Format the error message text as a string variable & print it to the console with a newline at the beginning & error number.
  PrintText('Error '+str(ErrorNumber)+': '+(ErrorMessage))
  # Determine if this error message is fatal.
  if Fatal == True:
    # If this error message is fatal inform the user that the script is about to close.
    PrintText('This application will now terminate.')
    # Stop executing code.
    exit(':(\n')
  return ErrorMessage
#--------------------

#--------------------
# Specify all the libraries to be loaded & the handles to use them.
def ImportLibraries(LastMessage):
  # Set some error flags to default values.
  LibErrorA, LibErrorB, MissingLibs = '', False, ''
  # Announce the start of the operation if Debug is enabled by configuration.
  if Debug == True:
    LastMessage = PrintMessage(LastMessage, 'Importing Required Libraries...')
  try:
    import RPi.GPIO as GPIO
  # Handle the exception that is raised if the RPi library is missing.
  except ModuleNotFoundError as LibErrorA:
    LibErrorB, MissingLibs = True, ' RPi'
    PrintError(1, 'Captured Exception, '+str(LibErrorA)+'.', False)
  # Attempt to import the Time Library.
  try:
    import time as Time
  # Handle the exception that is raised if the time library is missing.
  except ModuleNotFoundError as LibErrorA:
    LibErrorB, MissingLibs = True, MissingLibs+' time'
    PrintError(2, 'Captured Exception, '+str(LibErrorA)+'.', False)
  # Attempt to import the Keyboard Library.
  try:
    import keyboard as KB
  # Handle the exception that is raised if the keyboard library is missing.
  except ModuleNotFoundError as LibErrorA:
    LibErrorB, MissingLibs = True, MissingLibs+' keyboard'
    PrintError(3, 'Captured Exception, '+str(LibErrorA)+'.', False)
  # Consolidate error flags to determine if any errors happened.
  if LibErrorB == False:
    # Announce the end of the operation only if Debug is enabled by configuration.
    if Debug == True:
      LastMessage = PrintMessage(LastMessage, 'Libraries Imported Successfully.')
  else:
    # Announce a fatal error if the required libraries are not installed.
    LastMessage = PrintError(4, 'Could not Import Required Libraries. \nPlease install the following libraries: '+MissingLibs+'.', True)
  return LastMessage, GPIO, Time, KB
#--------------------

#--------------------
# Initialize the software operating environment.
def InitializeSoftwareEnvironment(LastMessage, Debug):
  # Initialize the message cache and loop tracking variables to default values.
  LoopCounter, LoopTracker = 0, 0
  # Announce the start of the operation if Debug is enabled by configuration.
  if Debug == True:
    LastMessage = PrintMessage(LastMessage, 'Initializing Software Operating Environment...')
  # Import required libraries.
  LastMessage, GPIO, Time, KB = ImportLibraries(LastMessage)
  # Announce the end of the operation if Debug is enabled by configuration.
  if Debug == True:
    LastMessage = PrintMessage(LastMessage, 'Software Operating Environment Initialized Successfully.')
  return LastMessage, LoopCounter, LoopTracker, GPIO, Time, KB
#--------------------

#--------------------
# Initialize the GPIO environment for a 40 pin Raspberry Pi.
def InitializeGPIO(LastMessage, GPIO, GPIOMode, GPIOWarnings, SpeakerGPIO, MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO, MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO):
  # Announce the start of the operation if Debug is enabled by configuration.
  if Debug == True:
    LastMessage = PrintMessage(LastMessage, 'Initializing GPIO Environment...')
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
  # Announce the end of the operation if Debug is enabled by configuration.
  if Debug == True:
    LastMessage = PrintMessage(LastMessage, 'GPIO Environment Initialized Successfully.')
  # Return the flag to the calling code as a sanity check in addition to the required variables from the RPi library.
  return GPIO
#--------------------

#--------------------
# Command the speaker to beep.
def Beep(SpeakerGPIO, BeepDuration, NumberOfBuzzes, Time):
  # Initialize duration & counter variables.
  Break, BeDuration, BuzzCount = False, (BeepDuration / NumberOfBuzzes) / 2, 0
  # Initialize a loop that sets up a frequency for the buzz.
  while Break == False:
    # Count this iteration of the loop.
    BuzzCount = BuzzCount + 1
    # Set the speaker GPIO pin to high.
    GPIO.output(SpeakerGPIO, GPIO.HIGH)
    # Pause for a moment.
    Time.sleep(BeDuration)
    # Set the speaker GPIO pin to low.
    GPIO.output(SpeakerGPIO, GPIO.LOW)
    # Determine if the maximum number of buzzes has been met.
    if BuzzCount < NumberOfBuzzes:
      # If there is another iteration coming then pause for a moment.
      Time.sleep(BeDuration)
    else:
      # Set a flag to break out of the loop.
      Break = True
#--------------------

#--------------------
# Calculate what the execution duration should be for a given throttle input.
def CalculateExecutionDuration(RequestedSpeed, DefaultSensitivity):
  # Calculate the square root of the throttle input.
  ExecutionDuration = RequestedSpeed * RequestedSpeed
  # Divide the square root of throttle input by the sensitivity value set by configuration.
  ExecutionDuration = ExecutionDuration / DefaultSensitivity
  return ExecutionDuration
#--------------------

#--------------------
# Update the speed setting for the motors.
def UpdateSpeed(RequestedSpeed, ExecutionDuration, DefaultDwellDuration, DefaultSensitivity):
  # Set the upper boundary for the RequestedSpeed variable to 9.
  # Anything higher than 9 will be considered a request for full throttle.
  if RequestedSpeed > 9:
    RequestedSpeed = 0
  # If full throttle has been requested the ExecutionDuration will consume the entire clock cycle.
  if RequestedSpeed == 0:
    ExecutionDuration = DefaultDwellDuration
  # Calculate what the execution time should be when partial throttle is requested.
  if RequestedSpeed > 0 and RequestedSpeed <= 9:
    ExecutionDuration = CalculateExecutionDuration(RequestedSpeed, DefaultSensitivity)
  return ExecutionDuration, RequestedSpeed
#--------------------

#--------------------
# Initialize the hardware operating environment.
def InitializeHardwareEnvironment(LastMessage, GPIO, GPIOWarnings, SpeakerGPIO, MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO, MotorRelayTwoPositiveGPIO, \
  MotorRelayTwoNegativeGPIO, DefaultSpeed, DefaultExecutionDuration, DefaultDwellDuration, DefaultSensitivity, Debug):
  # Initialize the current sensitivity to the default sensitivity set by configuration.
  CurrentSensitivity = DefaultSensitivity
  # Announce the start of the operation if Debug is enabled by configuration.
  if Debug == True:
    LastMessage = PrintMessage(LastMessage, 'Initializing Hardware  Operating Environment...')
  # Initialize the GPIO environment.
  GPIO = InitializeGPIO(LastMessage, GPIO, GPIOMode, GPIOWarnings, SpeakerGPIO, MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO, MotorRelayTwoPositiveGPIO, \
    MotorRelayTwoNegativeGPIO)
  # Calculate the default speed before a specific speed has been requested by the user. 
  ExecutionDuration, CurrentSpeed = UpdateSpeed(DefaultSpeed, DefaultExecutionDuration, DefaultDwellDuration, DefaultSensitivity)
  OriginalSpeed = CurrentSpeed
  # Set the clock speed for the session based on configuration.
  DwellDuration = DefaultDwellDuration
  # Announce the end of the operation if Debug is enabled by configuration.
  if Debug == True:
    LastMessage = PrintMessage(LastMessage, 'Hardware Operating Environment Initialized Successfully.')
  return LastMessage, ExecutionDuration, CurrentSpeed, OriginalSpeed, DwellDuration, CurrentSensitivity
#--------------------

#--------------------
# Initialize the entire operational environment for the application & attached hardware.
def InitializeEnvironment(SpeakerGPIO, MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO, MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO, DefaultSpeed, \
  DefaultExecutionDuration, DefaultDwellDuration, DefaultSensitivity, Debug):
  LastMessage, SensitivityCounter, SpeedCounter, Boosted = 'Init', 0, 0, False
  # Announce the start of the operation if Debug is enabled by configuration.
  if Debug == True:
    LastMessage = PrintMessage(LastMessage, 'Initializing Operating Environment...')  
  # Initialize the BreakLoop variable to False. This will allow the main loop to start which controls timing of the ESC.
  BreakLoop = False
  # Initialize the software environment.
  LastMessage, LoopCounter, LoopTracker, GPIO, Time, KB = InitializeSoftwareEnvironment(LastMessage, Debug)
  # Initialize the hardware environment.
  LastMessage, ExecutionDuration, CurrentSpeed, OriginalSpeed, DwellDuration, CurrentSensitivity = InitializeHardwareEnvironment(LastMessage, GPIO, GPIOWarnings, SpeakerGPIO, MotorRelayOnePositiveGPIO, \
    MotorRelayOneNegativeGPIO, MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO, DefaultSpeed, DefaultExecutionDuration, DefaultDwellDuration, DefaultSensitivity, Debug)
  # Announce the end of the operation if Debug is enabled by configuration.
  if Debug == True:
    LastMessage = PrintMessage(LastMessage, 'Operating Environment Initialized Successfully.')
  return LastMessage, SensitivityCounter, SpeedCounter, LoopCounter, LoopTracker, ExecutionDuration, CurrentSpeed, OriginalSpeed, CurrentSensitivity, DwellDuration, BreakLoop, Boosted, GPIO, Time, KB
#--------------------

#--------------------
# Remove boost from completed turn operations.
def RemoveBoost(Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed, DefaultDwellDuration, DefaultSensitivity):
  # Detect leftover boost or reduction from completed turn commands.
  if Boosted == True:
    # Set the speed back to the original speed.
    ExecutionDuration, CurrentSpeed = UpdateSpeed(OriginalSpeed, ExecutionDuration, DefaultDwellDuration, DefaultSensitivity)
    # Reset speed related variables.
    Boosted, OriginalSpeed = False, CurrentSpeed;
  return Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed
#--------------------

#--------------------
# Calculate the final speed should be with all boost & reduction applied.
def CalculateBoost(Boosted, CurrentSpeed, RightTotalBoost, LeftTotalBoost):
  # Detect if boost is already applied & do not apply boost more than once.
  if Boosted == False:
    # Set the upper limit for boost to 0.
    if CurrentSpeed == 0:
      RightBoosted, LeftBoosted = 10, 10
    else:
      RightBoosted, LeftBoosted = CurrentSpeed, CurrentSpeed
    # Set variables bounc by initial upper limit.
    RightMoving, LeftMoving = RightBoosted + RightTotalBoost, LeftBoosted + LeftTotalBoost
    # Set the lower limit for reduction.
    if CurrentSpeed != 0 and RightMoving <= 0:
      RightMoving = 1
    if CurrentSpeed != 0 and LeftMoving <= 0:
      LeftMoving = 1
    # Reset the upperr limit for boost.
    if RightMoving >= 10:
      RightMoving = 0
    if LeftMoving >= 10:
      LeftMoving = 0
  # If boost is already applied set the speed level for each channel to the currrent speed.
  else:
    RightMoving, LeftMoving = CurrentSpeed, CurrentSpeed
  return RightMoving, LeftMoving
#--------------------

#--------------------
# Apply any needed boost or reduction to a requested turn operation.
def AddBoost(Moving, Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed, DefaultDwellDuration, DefaultSensitivity):
  # Detect if boost is currently applied.
  if Moving != CurrentSpeed and Boosted == False:
    # Set variables to boosted values.
    Boosted, OriginalSpeed = True, CurrentSpeed
    # Update speed related variables to the new boosted values.
    ExecutionDuration, CurrentSpeed = UpdateSpeed(Moving, ExecutionDuration, DefaultDwellDuration, DefaultSensitivity)
  return Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed
#--------------------

#--------------------
# Motor One Stop Command.
# Command motor channel one to stop.
def MotorOneStop(MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO):
  # Deactivate the motor one positive GPIO pin.
  GPIO.output(MotorRelayOnePositiveGPIO, GPIO.LOW)
  # Deactivate the motor one negative GPIO pin.
  GPIO.output(MotorRelayOneNegativeGPIO, GPIO.LOW)
#--------------------

#--------------------
# Motor Two Stop Command.
# Command motor channel two to stop.
def MotorTwoStop(MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO):
  # Deactivate the motor two positive GPIO pin.
  GPIO.output(MotorRelayTwoPositiveGPIO, GPIO.LOW)
  # Deactivate the motor two negative GPIO pin.
  GPIO.output(MotorRelayTwoNegativeGPIO, GPIO.LOW)
#--------------------

#--------------------
# Motor One Forward Command.
# Command motor channel one to rotate forward.
def MotorOneForward(MotorRelayOnePositiveGPIO):
  # Activate motor one positive GPIO pin.
  GPIO.output(MotorRelayOnePositiveGPIO, GPIO.HIGH)
#--------------------

#--------------------
# Motor Two Forward Command.
# Command motor channel two to rotate forward.
def MotorTwoForward(MotorRelayTwoPositiveGPIO):
  # Activate motor two positive GPIO pin.
  GPIO.output(MotorRelayTwoPositiveGPIO, GPIO.HIGH)
#--------------------

#--------------------
# Motor One Reverse Command.
# Command motor channel one to rotate backward.
def MotorOneReverse(MotorRelayOneNegativeGPIO):
  # Activate motor one negative GPIO pin.
  GPIO.output(MotorRelayOneNegativeGPIO, GPIO.HIGH)
#--------------------

#--------------------
# Motor Two Reverse Command.
# Command motor channel two to rotate backward.
def MotorTwoReverse(MotorRelayTwoNegativeGPIO):
  # Activate motor two negative GPIO pin.
  GPIO.output(MotorRelayTwoNegativeGPIO, GPIO.HIGH)
#--------------------

#--------------------
# All Motors Stop Command.
# Command all motor channels to stop.
def AllMotorsStop(MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO, MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO):
  # Deactivate motor.
  MotorOneStop(MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO)
  # Deactivate motor.
  MotorTwoStop(MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO)
#--------------------

#--------------------
# All Motors Forward Command.
# Command all motor channels to rotate forward.
def AllMotorsForward(MotorRelayOnePositiveGPIO, MotorRelayTwoPositiveGPIO):
  # Activate Motor.
  MotorOneForward(MotorRelayOnePositiveGPIO)
  # Activate Motor.
  MotorTwoForward(MotorRelayTwoPositiveGPIO)
#--------------------

#--------------------
# All Motors Reverse Command.
# Command all motor channels to rotate backward.
def AllMotorsReverse(MotorRelayOneNegativeGPIO, MotorRelayTwoNegativeGPIO):
  # Activate Motor.
  MotorOneReverse(MotorRelayOneNegativeGPIO)
  # Activate Motor.
  MotorTwoReverse(MotorRelayTwoNegativeGPIO)
#--------------------

#--------------------
# Sensitivity Change Request.
# Detect when a sensitivity update is required.
def DetectKeyboardSensitivityChange(LastMessage, MinimumSensitivity, MaximumSensitivity, SensitivityCounter, DetectSensitivityInterval, DetectSensitivitySkipInterval, CurrentSensitivity, DefaultSensitivity, \
  SensitivityChangeAmount, KB, IncreaseSensitivityKey, DecreaseSensitivityKey, ExecutionDuration, DwellDuration, BeepDuration, NumberOfBuzzes, EnableSpeakerBeep, SpeakerGPIO, Debug):
  # Initialize variables for sanity checks, request flags, & movement flags.
  Pressed, RequestReceived, CommandSent, CommandsIssued, OpText = False, False, False, 0, False
  # Detect if a sensitivity check shoult be performed during the current cycle.
  if SensitivityCounter == 0:
    SensitivityCounter = DetectSensitivityInterval
    # Detect when the increase sensitivity key is pressed.
    if KB.is_pressed(IncreaseSensitivityKey):
      # Reinitialize variables for request & movement flags if a request is detected.
      # If the sensitivity counter is 0 then we reset it to the sensitivity interval set by configuration.
      SensitivityCounter, Pressed, RequestReceived, CommandSent, CommandsIssued, OpText = DetectSensitivitySkipInterval, False, 'Increase Sensitivity', 'Update Sensitivity', 0, 'Increase Sensitivity to Level '
      # Determine what the requested sensitivity is.
      RequestedSensitivity = CurrentSensitivity + SensitivityChangeAmount
      # Do not increase the sensitivity above the maximum set by configuration.
      if RequestedSensitivity <= MaximumSensitivity:
        # Increment the current sensitivity by the sensitivity change amount set by configuration.
        CurrentSensitivity = RequestedSensitivity
        # Increment the command counter & specify the request type.
        SensitivityCounter, Pressed, CommandsIssued, RequestReceived = DetectSensitivitySkipInterval, True, CommandsIssued + 1, OpText+str(CurrentSensitivity)
      else:
        SensitivityCounter, Pressed, RequestReceived, CommandSent, CommandsIssued, OpText = DetectSensitivitySkipInterval, False, 'Increase Sensitivity', 'Cannot Increase Sensitivity Any Higher', 0, 'Increase Sensitivity to Level '
    # Detect when the decrease sensitivity key is pressed.
    if KB.is_pressed(DecreaseSensitivityKey) and Pressed == False:
      # Reinitialize variables for request & movement flags if a request is detected.
      # If the sensitivity counter is 0 then we reset it to the sensitivity interval set by configuration.
      SensitivityCounter, Pressed, RequestReceived, CommandSent, CommandsIssued, OpText = DetectSensitivitySkipInterval, False, 'Decrease Sensitivity', 'Update Sensitivity', 0, 'Decrease Sensitivity to Level '
      # Determine what the requested sensitivity is.
      RequestedSensitivity = CurrentSensitivity - SensitivityChangeAmount
      # Do not decrease the sensitivity below zero or below the minimum set by configuration.
      if RequestedSensitivity > 0 and RequestedSensitivity >= MinimumSensitivity:
        # Decrement the current sensitivity by the sensitivity change amount set by configuration.
        CurrentSensitivity = RequestedSensitivity
        # Increment the command counter & specify the request type.
        SensitivityCounter, Pressed, CommandsIssued, RequestReceived = DetectSensitivitySkipInterval, True, CommandsIssued + 1, OpText+str(CurrentSensitivity)
      else:
        SensitivityCounter, Pressed, RequestReceived, CommandSent, CommandsIssued, OpText = DetectSensitivitySkipInterval, False, 'Increase Sensitivity', 'Cannot Decrease Sensitivity Any Lower', 0, 'Increase Sensitivity to Level '
    # Detect if a request was received.
    if Pressed == True:
      # Determine if the speaker is enabled by configuration.
      if EnableSpeakerBeep == True:
        # Output a beep from the speaker.
        Beep(SpeakerGPIO, BeepDuration, NumberOfBuzzes, Time)
      # Output when a speed change command is detected if Debug is set by configuration.
      if Debug == True:
        LastMessage = PrintMessage(LastMessage, 'Request Received: '+str(RequestReceived)+'. \nNumber Of Commands Issued: '+str(CommandsIssued)+\
          '. \nCommands Issued: '+str(CommandSent)+'. \nThe Execution Duration is '+str(ExecutionDuration)+\
          '. \nThe Dwell Duration is '+str(DwellDuration)+'.')
  # If no sensitivity check was performed, decrement the sensitivity counter by 1.
  else:
    SensitivityCounter = SensitivityCounter - 1
  return CurrentSensitivity, SensitivityCounter
#--------------------

#--------------------
# Speed Change Request.
# Detect when a speed update is required.
def DetectKeyboardSpeedChange(LastMessage, SpeedCounter, DetectSpeedInterval, DetectSpeedSkipInterval, ExecutionDuration, DwellDuration, Sensitivity, CurrentSpeed, KB, IncreaseSpeedKey, DecreaseSpeedKey, \
  SpeedOneKey, SpeedTwoKey, SpeedThreeKey, SpeedFourKey, SpeedFiveKey, SpeedSixKey, SpeedSevenKey, SpeedEightKey, SpeedNineKey, SpeedTenKey, BeepDuration, NumberOfBuzzes, EnableSpeakerBeep, SpeakerGPIO, Debug):
  # Initialize variables for sanity checks, request flags, & movement flags.
  Pressed, RequestReceived, CommandSent, CommandsIssued, OpText = False, False, False,  0, 'Update Speed to Level '
  # Detect if a speed check shoult be performed during the current cycle.
  if SpeedCounter == 0:
    SpeedCounter = DetectSpeedInterval
    # Detect when the increase speed key is pressed.
    if KB.is_pressed(IncreaseSpeedKey):
      # Reinitialize variables for request & movement flags if a request is detected.
      # If the speed counter is 0 then we reset it to the speed interval set by configuration.
      SpeedCounter, Pressed, RequestReceived, CommandSent, CommandsIssued, OpText = DetectSpeedSkipInterval, False, 'Increase Speed', 'Update Speed', 0, 'Increase Speed to Level '
      # Define the maximum speed that is possible.
      if CurrentSpeed == 0:
        Pressed, CommandSent, RequestReceived, RequestedSpeed, SpeedCounter = True, 'Cannot Increase Speed Any Higher', OpText+str(CurrentSpeed), CurrentSpeed, DetectSpeedSkipInterval
      if CurrentSpeed == 9:
        CurrentSpeed = 0
        Pressed, CommandsIssued, RequestReceived, RequestedSpeed, SpeedCounter = True, CommandsIssued + 1, OpText+str(CurrentSpeed), CurrentSpeed, DetectSpeedSkipInterval
      if CurrentSpeed != 0:
        # Increment the current speed by 1.
        CurrentSpeed = CurrentSpeed + 1
        # Increment the command counter & specify the request type.
        Pressed, CommandsIssued, RequestReceived, RequestedSpeed, SpeedCounter = True, CommandsIssued + 1, OpText+str(CurrentSpeed), CurrentSpeed, DetectSpeedSkipInterval
    # Detect when the decrease speed key is pressed.
    if KB.is_pressed(DecreaseSpeedKey):
      # Reinitialize variables for request & movement flags if a request is detected.
      # If the speed counter is 0 then we reset it to the speed interval set by configuration.
      SpeedCounter, Pressed, RequestReceived, CommandSent, CommandsIssued, OpText = DetectSpeedSkipInterval, False, 'Decrease Speed', 'Update Speed', 0, 'Decrease Speed to Level '
      # Do not decrement the speed value if it is already set to the lowest speed possible.
      if CurrentSpeed == 0:
        CurrentSpeed = 10
      if CurrentSpeed == 1:
        Pressed, CommandSent, RequestReceived, RequestedSpeed, SpeedCounter = True, 'Cannot Decrease Speed Any Lower', OpText+str(CurrentSpeed), CurrentSpeed, DetectSpeedSkipInterval
      else:
        # Decrement the current speed by 1.
        CurrentSpeed = CurrentSpeed - 1
        # Increment the command counter & specify the request type.
        Pressed, CommandsIssued, RequestReceived, RequestedSpeed, SpeedCounter = True, CommandsIssued + 1, OpText+str(CurrentSpeed), CurrentSpeed, DetectSpeedSkipInterval
    # Detect when a number key is pressed & set the speed level to that number.
    if KB.is_pressed(SpeedOneKey) and Pressed == False:
      # Increment the command counter & specify the request type.
      SpeedCounter, Pressed, CommandsIssued, RequestReceived, CommandSent, RequestedSpeed = DetectSpeedSkipInterval, True, CommandsIssued + 1, 'Update Speed', OpText+str(1), 1
    if KB.is_pressed(SpeedTwoKey) and Pressed == False:
      # Increment the command counter & specify the request type.
      SpeedCounter, Pressed, CommandsIssued, RequestReceived, CommandSent, RequestedSpeed = DetectSpeedSkipInterval, True, CommandsIssued + 1, 'Update Speed', OpText+str(2), 2
    if KB.is_pressed(SpeedThreeKey) and Pressed == False:
      # Increment the command counter & specify the request type.
      SpeedCounter, Pressed, CommandsIssued, RequestReceived, CommandSent, RequestedSpeed = DetectSpeedSkipInterval, True, CommandsIssued + 1, 'Update Speed', OpText+str(3), 3
    if KB.is_pressed(SpeedFourKey) and Pressed == False:
      # Increment the command counter & specify the request type.
      SpeedCounter, Pressed, CommandsIssued, RequestReceived, CommandSent, RequestedSpeed = DetectSpeedSkipInterval, True, CommandsIssued + 1, 'Update Speed', OpText+str(4), 4
    if KB.is_pressed(SpeedFiveKey) and Pressed == False:
      # Increment the command counter & specify the request type.
      SpeedCounter, Pressed, CommandsIssued, RequestReceived, CommandSent, RequestedSpeed = DetectSpeedSkipInterval, True, CommandsIssued + 1, 'Update Speed', OpText+str(5), 5
    if KB.is_pressed(SpeedSixKey) and Pressed == False:
      # Increment the command counter & specify the request type.
      SpeedCounter, Pressed, CommandsIssued, RequestReceived, CommandSent, RequestedSpeed = DetectSpeedSkipInterval, True, CommandsIssued + 1, 'Update Speed', OpText+str(6), 6
    if KB.is_pressed(SpeedSevenKey) and Pressed == False:
      # Increment the command counter & specify the request type.
      SpeedCounter, Pressed, CommandsIssued, RequestReceived, CommandSent, RequestedSpeed = DetectSpeedSkipInterval, True, CommandsIssued + 1, 'Update Speed', OpText+str(7), 7
    if KB.is_pressed(SpeedEightKey) and Pressed == False:
      # Increment the command counter & specify the request type.
      SpeedCounter, Pressed, CommandsIssued, RequestReceived, CommandSent, RequestedSpeed = DetectSpeedSkipInterval, True, CommandsIssued + 1, 'Update Speed', OpText+str(8), 8
    if KB.is_pressed(SpeedNineKey) and Pressed == False:
      # Increment the command counter & specify the request type.
      SpeedCounter, Pressed, CommandsIssued, RequestReceived, CommandSent, RequestedSpeed = DetectSpeedSkipInterval, True, CommandsIssued + 1, 'Update Speed', OpText+str(9), 9
    if KB.is_pressed(SpeedTenKey) and Pressed == False:
      # Increment the command counter & specify the request type.
      SpeedCounter, Pressed, CommandsIssued, RequestReceived, CommandSent, RequestedSpeed = DetectSpeedSkipInterval, True, CommandsIssued + 1, 'Update Speed', OpText+str(0), 0
    # Detect if a request was received.
    if Pressed == True:
      # Determine if the requested speed is within boundaries.
      if RequestedSpeed >= 0 and RequestedSpeed <= 9:
        # Update the speed & timing related variables to achieve the specified speed.
        ExecutionDuration, CurrentSpeed = UpdateSpeed(RequestedSpeed, ExecutionDuration, DefaultDwellDuration, Sensitivity)
        # Determine if the speaker is enabled by configuration.
        if EnableSpeakerBeep == True:
          # Output a beep from the speaker.
          Beep(SpeakerGPIO, BeepDuration, NumberOfBuzzes, Time)
        # Output when a speed change command is detected if Debug is set by configuration.
        if Debug == True:
          LastMessage = PrintMessage(LastMessage, 'Request Received: '+str(RequestReceived)+'. \nNumber Of Commands Issued: '+str(CommandsIssued)+\
            '. \nCommands Issued: '+str(CommandSent)+'. \nThe Execution Duration is '+str(ExecutionDuration)+\
            '. \nThe Dwell Duration is '+str(DwellDuration)+'.')
  # If no speed check was performed, decrement the speed counter by 1.
  else:
    SpeedCounter = SpeedCounter - 1
  return LastMessage, ExecutionDuration, CurrentSpeed, SpeedCounter
#--------------------

#--------------------
# Stop Request.
# Detect a request to stop all motors.
def DetectStopRequest(LastMessage, DebugStops, CurrentSpeed, OriginalSpeed, KB, Boosted, ExecutionDuration, DefaultDwellDuration, DefaultSensitivity, MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO, \
  MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO, Debug):
  # Initialize variables for sanity checks, request flags, & movement flags.
  CheckOne, CheckTwo, RequestReceived, CommandSent, RightMoving, LeftMoving, CommandsIssued  = False, False, False, False, 0, 0, 0
  # Detect when a primary movement key is pressed.
  if not KB.is_pressed(ForwardKey) and not KB.is_pressed(BackwardKey) and not KB.is_pressed(TurnLeftKey) and not KB.is_pressed(TurnRightKey):
    CheckOne = True
  # Detect when a primary movement key is pressed.
  if not KB.is_pressed(LeftLimpRightKey) and not KB.is_pressed(LeftLimpLeftKey) and not KB.is_pressed(RightLimpLeftKey) and not KB.is_pressed(RightLimpRightKey):
    CheckTwo = True
  # Determine if either set of primary movement keys were detected.
  if CheckOne == True and CheckTwo == True:
    # Initialize variables for sanity checks, request flags, & movement flags.
    CheckOne, CheckTwo, RequestReceived, CommandSent = False, False, 'Stop', 'All Motors Stop'
    # Remove boost from completed turn operations.
    Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed = RemoveBoost(Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed, DefaultDwellDuration, DefaultSensitivity)
    # Deactivate all motors.
    AllMotorsStop(MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO, MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO)
    # Increment the command counter.
    CommandsIssued = CommandsIssued + 1
    # Set the movement flags to stopping.
    RightMoving, LeftMoving = 'Stopping', 'Stopping'
    # Output when a movement command is detected if Debug is set by configuration.
    if CommandsIssued > 0:
      if Debug == True:
        if DebugStops == True:
          LastMessage = PrintMessage(LastMessage, 'Request Received: '+str(RequestReceived)+'. \nNumber Of Commands Issued: '+str(CommandsIssued)+\
            '. \nCommands Issued: '+str(CommandSent)+'. \nEffective Boost: Right, None. Left, None. \nRight Channel Status: '+str(RightMoving)+'. \nLeft Channel Status: '+str(LeftMoving)+'.')
  return LastMessage, RequestReceived, RightMoving, LeftMoving, Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed
#--------------------

#--------------------
# Forward Request.
# Detect a request to rotate all motors forward.
def DetectForwardRequest(LastMessage, CurrentSpeed, OriginalSpeed, KB, Boosted, ExecutionDuration, DefaultDwellDuration, DefaultSensitivity, MotorRelayOnePositiveGPIO, MotorRelayTwoPositiveGPIO, ForwardKey, \
  BackwardKey, TurnRightKey, TurnLeftKey, RightLimpRighKey, RightLimpLeftKey, LeftLimpRightKey, LeftLimpLeftKey, Debug):
  # Initialize variables for sanity checks, request flags, & movement flags.
  RightMoving, LeftMoving, RequestReceived, CommandSent, RightTotalBoost, LeftTotalBoost, CommandsIssued = False, False, False, False, 0, 0, 0
  # Detect when a primary movement key is pressed.
  if KB.is_pressed(ForwardKey):
    # Detect when conflicting movement keys are pressed & ignore input for this channel.
    if not KB.is_pressed(BackwardKey) and not KB.is_pressed(TurnRightKey) and not KB.is_pressed(RightLimpRightKey):
      # Reinitialize variables for request & movement flags if a request is detected.
      RequestReceived, CommandSent, RightMoving, LeftMoving = 'Forward', 'Motor One Forward', CurrentSpeed, CurrentSpeed
      # Remove boost from completed turn operations.
      Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed = RemoveBoost(Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed, DefaultDwellDuration, DefaultSensitivity)
      # Activate motor.
      MotorOneForward(MotorRelayOnePositiveGPIO)
      # Increment the command counter.
      CommandsIssued = CommandsIssued + 1
    # Detect when conflicting movement keys are pressed & ignore input for this channel.
    if not KB.is_pressed(BackwardKey) and not KB.is_pressed(TurnLeftKey) and not KB.is_pressed(LeftLimpLeftKey):
      # Reinitialize variables for request & movement flags if a request is detected.
      RequestReceived, CommandSent, RightMoving, LeftMoving = 'Forward', str(CommandSent)+', Motor Two Forward', CurrentSpeed, CurrentSpeed
      # Remove boost from completed turn operations.
      Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed = RemoveBoost(Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed, DefaultDwellDuration, DefaultSensitivity)
      # Activate motor.
      MotorTwoForward(MotorRelayTwoPositiveGPIO)
      # Increment the command counter.
      CommandsIssued = CommandsIssued + 1
    # Output when a movement command is detected if Debug is set by configuration.
    if CommandsIssued > 0:
      if Debug == True:
        LastMessage = PrintMessage(LastMessage, 'Request Received: '+str(RequestReceived)+'. \nNumber Of Commands Issued: '+str(CommandsIssued)+\
          '. \nCommands Issued: '+str(CommandSent)+'. \nEffective Boost: Right, None. Left, None. \nRight Channel Status: '+str(RightMoving)+'. \nLeft Channel Status: '+str(LeftMoving)+'.')
  return LastMessage, RequestReceived, RightMoving, LeftMoving, Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed
#--------------------

#--------------------
# Reverse Request.
# Detect a request to rotate all motors backward.
def DetectReverseRequest(LastMessage, CurrentSpeed, OriginalSpeed, KB, Boosted, ExecutionDuration, DefaultDwellDuration, DefaultSensitivity, MotorRelayOneNegativeGPIO, MotorRelayTwoNegativeGPIO, ForwardKey, \
  BackwardKey, TurnRightKey, TurnLeftKey, RightLimpRighKey, RightLimpLeftKey, LeftLimpRightKey, LeftLimpLeftKey, Debug):
  # Initialize variables for sanity checks, request flags, & movement flags.
  RightMoving, LeftMoving, RequestReceived, CommandSent, RightTotalBoost, LeftTotalBoost, CommandsIssued = False, False, False, False, 0, 0, 0
  # Detect when a primary movement key is pressed.
  if KB.is_pressed(BackwardKey):
    # Detect when conflicting movement keys are pressed & ignore input for this channel.
    if not KB.is_pressed(ForwardKey) and not KB.is_pressed(TurnLeftKey) and not KB.is_pressed(RightLimpLeftKey) and not KB.is_pressed(LeftLimpLeftKey):
      # Reinitialize variables for request & movement flags if a request is detected.
      RequestReceived, CommandSent, RightMoving, LeftMoving = 'Backward', 'Motor One Reverse', CurrentSpeed, CurrentSpeed
      # Remove boost from completed turn operations.
      Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed = RemoveBoost(Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed, DefaultDwellDuration, DefaultSensitivity)
      # Activate motor.
      MotorOneReverse(MotorRelayOneNegativeGPIO)
      # Increment the command counter.
      CommandsIssued = CommandsIssued + 1
    # Detect when conflicting movement keys are pressed & ignore input for this channel.
    if not KB.is_pressed(ForwardKey) and not KB.is_pressed(TurnRightKey) and not KB.is_pressed(RightLimpRightKey) and not KB.is_pressed(LeftLimpRightKey):
      # Reinitialize variables for request & movement flags if a request is detected.
      RequestReceived, CommandSent, RightMoving, LeftMoving = 'Backward', str(CommandSent)+', Motor Two Reverse', CurrentSpeed, CurrentSpeed
      # Remove boost from completed turn operations.
      Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed = RemoveBoost(Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed, DefaultDwellDuration, DefaultSensitivity)
      # Activate motor.
      MotorTwoReverse(MotorRelayTwoNegativeGPIO)
      # Increment the command counter.
      CommandsIssued = CommandsIssued + 1
    # Output when a movement command is detected if Debug is set by configuration.
    if CommandsIssued > 0:
      if Debug == True:
        LastMessage = PrintMessage(LastMessage, 'Request Received: '+str(RequestReceived)+'. \nNumber Of Commands Issued: '+str(CommandsIssued)+\
          '. \nCommands Issued: '+str(CommandSent)+'. \nEffective Boost: Right, None. Left, None. \nRight Channel Status: '+str(RightMoving)+'. \nLeft Channel Status: '+str(LeftMoving)+'.')
  return LastMessage, RequestReceived, RightMoving, LeftMoving, Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed
#--------------------

#--------------------
# Turn Right Request.
# Detect a request to rotate all motors right.
def DetectRightRequest(LastMessage, CurrentSpeed, OriginalSpeed, KB, ExecutionDuration, DefaultDwellDuration, DefaultSensitivity, Boosted, MotorRelayTwoPositiveGPIO, MotorRelayOneNegativeGPIO, \
  RightBoostAmount, RightReductionAmount, LeftBoostAmount, LeftReductionAmount, ForwardKey, BackwardKey, TurnRightKey, TurnLeftKey, RightLimpRighKey, RightLimpLeftKey, LeftLimpRightKey, \
  LeftLimpLeftKey, Debug):
  # Initialize variables for sanity checks, request flags, & movement flags.
  RightMoving, LeftMoving, RequestReceived, CommandSent, RightTotalBoost, LeftTotalBoost, CommandsIssued = False, False, False, False, 0, 0, 0
  # Detect when a primary movement key is pressed.
  if KB.is_pressed(TurnRightKey):
    # Detect when conflicting movement keys are pressed & ignore input for this channel.
    if not KB.is_pressed(ForwardKey) and not KB.is_pressed(BackwardKey) and not KB.is_pressed(TurnLeftKey) and not KB.is_pressed(LeftLimpLeftKey) and not KB.is_pressed(RightLimpLeftKey):
      # Reinitialize variables for request & movement flags if a request is detected.
      RequestReceived, CommandSent, RightTotalBoost, LeftTotalBoost = 'Turn Right', 'Motor One Reverse. Motor Two Forward', RightBoostAmount - RightReductionAmount, LeftBoostAmount - LeftReductionAmount
      # Set boosted speed values.
      RightMoving, LeftMoving = CalculateBoost(Boosted, CurrentSpeed, RightTotalBoost, LeftTotalBoost)
      # Apply boost & reduction.
      Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed = AddBoost(RightMoving, Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed, DefaultDwellDuration, DefaultSensitivity)
      # Activate motor.
      MotorOneReverse(MotorRelayOneNegativeGPIO)
      # Increment the command counter.
      CommandsIssued = CommandsIssued + 1
      # Activate motor.
      MotorTwoForward(MotorRelayTwoPositiveGPIO)
      # Increment the command counter.
      CommandsIssued = CommandsIssued + 1
      # Output when a movement command is detected if Debug is set by configuration.
      if CommandsIssued > 0:
        if Debug == True:
          LastMessage = PrintMessage(LastMessage, 'Request Received: '+str(RequestReceived)+'. \nNumber Of Commands Issued: '+str(CommandsIssued)+\
            '. \nCommands Issued: '+str(CommandSent)+'. \nEffective Boost: Right, '+str(RightTotalBoost)+'. Left, '+str(LeftTotalBoost)+'. \nRight Channel Status: '+str(RightMoving)+\
            '. \nLeft Channel Status: '+str(LeftMoving)+'.')
  return LastMessage, RequestReceived, RightMoving, LeftMoving, Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed
#--------------------

#--------------------
# Turn Left Request.
# Detect a request to rotate all motors left.
def DetectLeftRequest(LastMessage, CurrentSpeed, OriginalSpeed, KB, ExecutionDuration, DefaultDwellDuration, DefaultSensitivity, Boosted, MotorRelayOnePositiveGPIO, MotorRelayTwoNegativeGPIO, RightBoostAmount, \
  RightReductionAmount, LeftBoostAmount, LeftReductionAmount, ForwardKey, BackwardKey, TurnRightKey, TurnLeftKey, RightLimpRighKey, RightLimpLeftKey, LeftLimpRightKey, LeftLimpLeftKey,  Debug):
  # Initialize variables for sanity checks, request flags, & movement flags.
  RightMoving, LeftMoving, RequestReceived, CommandSent, RightTotalBoost, LeftTotalBoost, CommandsIssued = False, False, False, False, 0, 0, 0
  # Detect when a primary movement key is pressed.
  if KB.is_pressed(TurnLeftKey):
    # Detect when conflicting movement keys are pressed & ignore input for this channel.
    if not KB.is_pressed(ForwardKey) and not KB.is_pressed(BackwardKey) and not KB.is_pressed(TurnRightKey) and not KB.is_pressed(RightLimpRightKey) and not KB.is_pressed(LeftLimpRightKey):
      # Reinitialize variables for request & movement flags if a request is detected.
      RequestReceived, CommandSent, RightTotalBoost, LeftTotalBoost = 'Turn Left', 'Motor One Forward. Motor Two Reverse', RightBoostAmount - RightReductionAmount, LeftBoostAmount - LeftReductionAmount
      # Set boosted speed values.
      RightMoving, LeftMoving = CalculateBoost(Boosted, CurrentSpeed, RightTotalBoost, LeftTotalBoost)
      # Apply boost & reduction.
      Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed = AddBoost(LeftMoving, Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed, DefaultDwellDuration, DefaultSensitivity)
      # Activate motor.
      MotorOneForward(MotorRelayOnePositiveGPIO)
      # Increment the command counter.
      CommandsIssued = CommandsIssued + 1
      # Activate motor.
      MotorTwoReverse(MotorRelayTwoNegativeGPIO)
      # Increment the command counter.
      CommandsIssued = CommandsIssued + 1
      # Output when a movement command is detected if Debug is set by configuration.
      if CommandsIssued > 0:
        if Debug == True:
          LastMessage = PrintMessage(LastMessage, 'Request Received: '+str(RequestReceived)+'. \nNumber Of Commands Issued: '+str(CommandsIssued)+\
            '. \nCommands Issued: '+str(CommandSent)+'. \nEffective Boost: Right, '+str(RightTotalBoost)+'. Left, '+str(LeftTotalBoost)+'. \nRight Channel Status: '+str(RightMoving)+\
            '. \nLeft Channel Status: '+str(LeftMoving)+'.')
  return LastMessage, RequestReceived, RightMoving, LeftMoving, Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed
#--------------------

#--------------------
# Right Motors Limp Right Request.
# Detect a request to rotate right motors right.
def DetectRightLimpRightRequest(LastMessage, CurrentSpeed, OriginalSpeed, KB, ExecutionDuration, DefaultDwellDuration, DefaultSensitivity, Boosted, MotorRelayOneNegativeGPIO, RightLimpBoostAmount, \
  RightLimpReductionAmount, ForwardKey, BackwardKey, TurnRightKey, TurnLeftKey, RightLimpRighKey, RightLimpLeftKey, LeftLimpRightKey, LeftLimpLeftKey, Debug):
  # Initialize variables for sanity checks, request flags, & movement flags.
  RightMoving, LeftMoving, RequestReceived, CommandSent, RightTotalBoost, LeftTotalBoost, CommandsIssued = False, False, False, False, 0, 0, 0
  # Detect when a primary movement key is pressed.
  if KB.is_pressed(RightLimpRightKey):
    # Detect when conflicting movement keys are pressed & ignore input for this channel.
    if not KB.is_pressed(ForwardKey) and not KB.is_pressed(TurnLeftKey) and not KB.is_pressed(RightLimpLeftKey)  and not KB.is_pressed(LeftLimpLeftKey):
      # Reinitialize variables for request & movement flags if a request is detected.
      RequestReceived, CommandSent, RightTotalBoost, LeftTotalBoost = 'Turn Right With Right Motors', 'Motor One Reverse', RightLimpBoostAmount - RightLimpReductionAmount, LeftLimpBoostAmount - LeftLimpReductionAmount
      # Set boosted speed values.
      RightMoving, LeftMoving = CalculateBoost(Boosted, CurrentSpeed, RightTotalBoost, LeftTotalBoost)
      # Apply boost & reduction.
      Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed = AddBoost(RightMoving, Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed, DefaultDwellDuration, DefaultSensitivity)
      # Activate motor.
      MotorOneReverse(MotorRelayOneNegativeGPIO)
      # Increment the command counter.
      CommandsIssued = CommandsIssued + 1
      # Output when a movement command is detected if Debug is set by configuration.
      if CommandsIssued > 0:
        if Debug == True:
          LastMessage = PrintMessage(LastMessage, 'Request Received: '+str(RequestReceived)+'. \nNumber Of Commands Issued: '+str(CommandsIssued)+\
            '. \nCommands Issued: '+str(CommandSent)+'. \nEffective Boost: Right, '+str(RightTotalBoost)+'. Left, '+str(LeftTotalBoost)+'. \nRight Channel Status: '+str(RightMoving)+\
            '. \nLeft Channel Status: '+str(LeftMoving)+'.')
  return LastMessage, RequestReceived, RightMoving, LeftMoving, Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed
#--------------------

#--------------------
# Right Motors Limp Left Request.
# Detect a request to rotate right motors left.
def DetectRightLimpLeftRequest(LastMessage, CurrentSpeed, OriginalSpeed, KB, ExecutionDuration, DefaultDwellDuration, DefaultSensitivity, Boosted, MotorRelayOnePositiveGPIO, RightLimpBoostAmount, \
  RightLimpReductionAmount, ForwardKey, BackwardKey, TurnRightKey, TurnLeftKey, RightLimpRighKey, RightLimpLeftKey, LeftLimpRightKey, LeftLimpLeftKey, Debug):
  # Initialize variables for sanity checks, request flags, & movement flags.
  RightMoving, LeftMoving, RequestReceived, CommandSent, RightTotalBoost, LeftTotalBoost, CommandsIssued = False, False, False, False, 0, 0, 0
  # Detect when a primary movement key is pressed.
  if KB.is_pressed(RightLimpLeftKey):
    # Detect when conflicting movement keys are pressed & ignore input for this channel.
    if not KB.is_pressed(BackwardKey) and not KB.is_pressed(TurnRightKey) and not KB.is_pressed(RightLimpRightKey) and not KB.is_pressed(LeftLimpRightKey):
      # Reinitialize variables for request & movement flags if a request is detected.
      RequestReceived, CommandSent, RightTotalBoost, LeftTotalBoost = 'Turn Left With Right Motors', 'Motor One Forward', RightLimpBoostAmount - RightLimpReductionAmount, LeftLimpBoostAmount - LeftLimpReductionAmount
      # Set boosted speed values.
      RightMoving, LeftMoving = CalculateBoost(Boosted, CurrentSpeed, RightTotalBoost, LeftTotalBoost)
      # Apply boost & reduction.
      Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed = AddBoost(LeftMoving, Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed, DefaultDwellDuration, DefaultSensitivity)
      # Activate motor.
      MotorOneForward(MotorRelayOnePositiveGPIO)
      # Increment the command counter.
      CommandsIssued = CommandsIssued + 1
      # Output when a movement command is detected if Debug is set by configuration.
      if CommandsIssued > 0:
        if Debug == True:
          LastMessage = PrintMessage(LastMessage, 'Request Received: '+str(RequestReceived)+'. \nNumber Of Commands Issued: '+str(CommandsIssued)+\
            '. \nCommands Issued: '+str(CommandSent)+'. \nEffective Boost: Right, '+str(RightTotalBoost)+'. Left, '+str(LeftTotalBoost)+'. \nRight Channel Status: '+str(RightMoving)+\
            '. \nLeft Channel Status: '+str(LeftMoving)+'.')
  return LastMessage, RequestReceived, RightMoving, LeftMoving, Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed
#--------------------

#--------------------
# Left Motors Limp Right Request.
# Detect a request to rotate left motors right.
def DetectLeftLimpRightRequest(LastMessage, CurrentSpeed, OriginalSpeed, KB, ExecutionDuration, DefaultDwellDuration, DefaultSensitivity, Boosted, MotorRelayTwoPositiveGPIO, LeftLimpBoostAmount, \
  LeftLimpReductionAmount, ForwardKey, BackwardKey, TurnRightKey, TurnLeftKey, RightLimpRighKey, RightLimpLeftKey, LeftLimpRightKey, LeftLimpLeftKey, Debug):
  # Initialize variables for sanity checks, request flags, & movement flags.
  RightMoving, LeftMoving, RequestReceived, CommandSent, RightTotalBoost, LeftTotalBoost, CommandsIssued = False, False, False, False, 0, 0, 0
  # Detect when a primary movement key is pressed.
  if KB.is_pressed(LeftLimpRightKey):
    # Detect when conflicting movement keys are pressed & ignore input for this channel.
    if not KB.is_pressed(BackwardKey) and not KB.is_pressed(TurnLeftKey) and not KB.is_pressed(LeftLimpLeftKey) and not KB.is_pressed(RightLimpLeftKey):
      # Reinitialize variables for request & movement flags if a request is detected.
      RequestReceived, CommandSent, RightTotalBoost, LeftTotalBoost = 'Turn Right With Left Motors', 'Motor Two Forward', RightLimpBoostAmount - RightLimpReductionAmount, LeftLimpBoostAmount - LeftLimpReductionAmount
      # Set boosted speed values.
      RightMoving, LeftMoving = CalculateBoost(Boosted, CurrentSpeed, RightTotalBoost, LeftTotalBoost)
      # Apply boost & reduction.
      Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed = AddBoost(RightMoving, Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed, DefaultDwellDuration, DefaultSensitivity)
      # Activate motor.
      MotorTwoForward(MotorRelayTwoPositiveGPIO)
      # Increment the command counter.
      CommandsIssued = CommandsIssued + 1
      # Output when a movement command is detected if Debug is set by configuration.
      if CommandsIssued > 0:
        if Debug == True:
          LastMessage = PrintMessage(LastMessage, 'Request Received: '+str(RequestReceived)+'. \nNumber Of Commands Issued: '+str(CommandsIssued)+\
            '. \nCommands Issued: '+str(CommandSent)+'. \nEffective Boost: Right, '+str(RightTotalBoost)+'. Left, '+str(LeftTotalBoost)+'. \nRight Channel Status: '+str(RightMoving)+\
            '. \nLeft Channel Status: '+str(LeftMoving)+'.')
  return LastMessage, RequestReceived, RightMoving, LeftMoving, Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed
#--------------------

#--------------------
# Left Motors Limp Left Request.
# Detect a request to rotate left motors left.
def DetectLeftLimpLeftRequest(LastMessage, CurrentSpeed, OriginalSpeed, KB, ExecutionDuration, DefaultDwellDuration, DefaultSensitivity, Boosted, MotorRelayTwoNegativeGPIO, LeftBoostAmount, \
  LeftReductionAmount, ForwardKey, BackwardKey, TurnRightKey, TurnLeftKey, RightLimpRighKey, RightLimpLeftKey, LeftLimpRightKey, LeftLimpLeftKey, Debug):
  # Initialize variables for sanity checks, request flags, & movement flags.
  RightMoving, LeftMoving, RequestReceived, CommandSent, RightTotalBoost, LeftTotalBoost, CommandsIssued = False, False, False, False, 0, 0, 0
  # Detect when a primary movement key is pressed.
  if KB.is_pressed(LeftLimpLeftKey):
    # Detect when conflicting movement keys are pressed & ignore input for this channel.
    if not KB.is_pressed(ForwardKey) and not KB.is_pressed(TurnRightKey) and not KB.is_pressed(LeftLimpRightKey) and not KB.is_pressed(RightLimpRightKey):
      # Reinitialize variables for request & movement flags if a request is detected.
      RequestReceived, CommandSent, RightTotalBoost, LeftTotalBoost = 'Turn Left With Left Motors', 'Motor One Reverse', RightLimpBoostAmount - RightLimpReductionAmount, LeftLimpBoostAmount - LeftLimpReductionAmount
      # Set boosted speed values.
      RightMoving, LeftMoving = CalculateBoost(Boosted, CurrentSpeed, RightTotalBoost, LeftTotalBoost)
      # Apply boost & reduction.
      Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed = AddBoost(LeftMoving, Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed, DefaultDwellDuration, DefaultSensitivity)
      # Activate motor.
      MotorTwoReverse(MotorRelayTwoNegativeGPIO)
      # Increment the command counter.
      CommandsIssued = CommandsIssued + 1
      # Output when a movement command is detected if Debug is set by configuration.
      if CommandsIssued > 0:
        if Debug == True:
          LastMessage = PrintMessage(LastMessage, 'Request Received: '+str(RequestReceived)+'. \nNumber Of Commands Issued: '+str(CommandsIssued)+\
            '. \nCommands Issued: '+str(CommandSent)+'. \nEffective Boost: Right, '+str(RightTotalBoost)+'. Left, '+str(LeftTotalBoost)+'. \nRight Channel Status: '+str(RightMoving)+\
            '. \nLeft Channel Status: '+str(LeftMoving)+'.')
  return LastMessage, RequestReceived, RightMoving, LeftMoving, Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed
#--------------------

#--------------------
# Detect which motion is being requested & activate the corresponding motor command.
def DetectKeyboardMotion(LastMessage, DebugStops, CurrentSpeed, OriginalSpeed, BeepDuration, NumberOfBuzzes, EnableSpeakerBeep, SpeakerGPIO, MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO, \
  MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO, RightBoostAmount, RightReductionAmount, RightLimpBoostAmount, RightLimpReductionAmount, LeftBoostAmount, \
  LeftReductionAmount, LeftLimpBoostAmount, LeftLimpReductionAmount, ForwardKey, BackwardKey, TurnRightKey, TurnLeftKey, RightLimpRighKey, RightLimpLeftKey, \
  LeftLimpRightKey, LeftLimpLeftKey, Boosted, ExecutionDuration, Time, KB, Debug):
  # Initialize variables for request & movement flags.
  RequestReceived, RightMoving, LeftMoving, Pressed = False, False, False, False
  # Detect motion requests from supplied user input.
  # These functions trigger GPIO output activity.
  # Detect a Stop Request.
  LastMessage, RequestReceived, RightMoving, LeftMoving, Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed = DetectStopRequest(LastMessage, DebugStops, CurrentSpeed, OriginalSpeed, \
    KB, Boosted, ExecutionDuration, DefaultDwellDuration, DefaultSensitivity, MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO, MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO, Debug)
  if RequestReceived != False and DebugStops == True:
    Pressed = True
  # Detect a Forward Request.
  LastMessage, RequestReceived, RightMoving, LeftMoving, Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed = DetectForwardRequest(LastMessage, CurrentSpeed, OriginalSpeed, KB, Boosted, \
    ExecutionDuration, DefaultDwellDuration, DefaultSensitivity, MotorRelayOnePositiveGPIO, MotorRelayTwoPositiveGPIO, ForwardKey, BackwardKey, TurnRightKey, TurnLeftKey, RightLimpRighKey, \
    RightLimpLeftKey, LeftLimpRightKey, LeftLimpLeftKey, Debug)
  if RequestReceived != False:
    Pressed = True
  # Detect a Reverse Request.
  LastMessage, RequestReceived, RightMoving, LeftMoving, Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed = DetectReverseRequest(LastMessage, CurrentSpeed, OriginalSpeed, KB, Boosted, \
    ExecutionDuration, DefaultDwellDuration, DefaultSensitivity, MotorRelayOneNegativeGPIO, MotorRelayTwoNegativeGPIO, ForwardKey, BackwardKey, TurnRightKey, TurnLeftKey, RightLimpRighKey, \
    RightLimpLeftKey, LeftLimpRightKey, LeftLimpLeftKey, Debug)
  if RequestReceived != False:
    Pressed = True
  # Detect a Right Turn Request.
  LastMessage, RequestReceived, RightMoving, LeftMoving, Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed = DetectRightRequest(LastMessage, CurrentSpeed, OriginalSpeed, KB, ExecutionDuration, \
    DefaultDwellDuration, DefaultSensitivity, Boosted, MotorRelayTwoPositiveGPIO, MotorRelayOneNegativeGPIO, RightBoostAmount, RightReductionAmount, LeftBoostAmount, LeftReductionAmount, ForwardKey, \
    BackwardKey, TurnRightKey, TurnLeftKey, RightLimpRighKey, RightLimpLeftKey, LeftLimpRightKey, LeftLimpLeftKey, Debug)
  if RequestReceived != False:
    Pressed = True
  # Detect a Left Turn Request.
  LastMessage, RequestReceived, RightMoving, LeftMoving, Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed = DetectLeftRequest(LastMessage, CurrentSpeed, OriginalSpeed, KB, ExecutionDuration, \
    DefaultDwellDuration, DefaultSensitivity, Boosted, MotorRelayOnePositiveGPIO, MotorRelayTwoNegativeGPIO, RightBoostAmount, RightReductionAmount, LeftBoostAmount, LeftReductionAmount, ForwardKey, \
    BackwardKey, TurnRightKey, TurnLeftKey, RightLimpRighKey, RightLimpLeftKey, LeftLimpRightKey, LeftLimpLeftKey, Debug)
  if RequestReceived != False:
    Pressed = True
  # Detect a Right Motor Limp Right Request.
  LastMessage, RequestReceived, RightMoving, LeftMoving, Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed = DetectRightLimpRightRequest(LastMessage, CurrentSpeed, OriginalSpeed, KB, ExecutionDuration, \
    DefaultDwellDuration, DefaultSensitivity, Boosted, MotorRelayOneNegativeGPIO, RightLimpBoostAmount, RightLimpReductionAmount, ForwardKey, BackwardKey, TurnRightKey, TurnLeftKey, RightLimpRighKey, \
    RightLimpLeftKey, LeftLimpRightKey, LeftLimpLeftKey, Debug)
  if RequestReceived != False:
    Pressed = True
  # Detect a Right Motor Limp Left Request.
  LastMessage, RequestReceived, RightMoving, LeftMoving, Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed = DetectRightLimpLeftRequest(LastMessage, CurrentSpeed, OriginalSpeed, KB, ExecutionDuration, \
    DefaultDwellDuration, DefaultSensitivity, Boosted, MotorRelayOnePositiveGPIO, RightLimpBoostAmount, RightLimpReductionAmount, ForwardKey, BackwardKey, TurnRightKey, TurnLeftKey, RightLimpRighKey, \
    RightLimpLeftKey, LeftLimpRightKey, LeftLimpLeftKey, Debug)
  if RequestReceived != False:
    Pressed = True
  # Detect a Left Motor Limp Right Request.
  LastMessage, RequestReceived, RightMoving, LeftMoving, Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed = DetectLeftLimpRightRequest(LastMessage, CurrentSpeed, OriginalSpeed, KB, ExecutionDuration, \
    DefaultDwellDuration, DefaultSensitivity, Boosted, MotorRelayTwoNegativeGPIO, LeftLimpBoostAmount, LeftLimpReductionAmount, ForwardKey, BackwardKey, TurnRightKey, TurnLeftKey, RightLimpRighKey, \
    RightLimpLeftKey, LeftLimpRightKey, LeftLimpLeftKey, Debug)
  if RequestReceived != False:
    Pressed = True
  # Detect a Left Motor Limp Left Request.
  LastMessage, RequestReceived, RightMoving, LeftMoving, Boosted, ExecutionDuration, CurrentSpeed, OriginalSpeed = DetectLeftLimpLeftRequest(LastMessage, CurrentSpeed, OriginalSpeed, KB, ExecutionDuration, \
    DefaultDwellDuration, DefaultSensitivity, Boosted, MotorRelayTwoPositiveGPIO, LeftLimpBoostAmount, LeftLimpReductionAmount, ForwardKey, BackwardKey, TurnRightKey, TurnLeftKey, RightLimpRighKey, \
    RightLimpLeftKey, LeftLimpRightKey, LeftLimpLeftKey, Debug)
  if RequestReceived != False:
    Pressed = True
  # Determine if a request was received.
  if Pressed == True:
    # Determine if the speaker is enabled by configuration.
    if EnableSpeakerBeep == True:
      # Output a beep from the speaker.
      Beep(SpeakerGPIO, BeepDuration, NumberOfBuzzes, Time)
  return LastMessage, ExecutionDuration, CurrentSpeed, OriginalSpeed, Boosted
#--------------------

#--------------------
# Listen for requests from the user & call the appropriate procedure to accomplish it.
def ListenForKeyboardRequests(LastMessage, DebugStops, MinimumSensitivity, MaximumSensitivity, SensitivityCounter, SpeedCounter, ExecutionDuration, DwellDuration, DefaultSensitivity, CurrentSpeed, OriginalSpeed, BeepDuration, \
  NumberOfBuzzes, EnableSpeakerBeep, SpeakerGPIO, MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO, MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO, RightBoostAmount, RightReductionAmount, \
  RightLimpBoostAmount, RightLimpReductionAmount, LeftBoostAmount, LeftReductionAmount, LeftLimpBoostAmount, LeftLimpReductionAmount, ForwardKey, BackwardKey, \
  TurnRightKey, TurnLeftKey, RightLimpRighKey, RightLimpLeftKey, LeftLimpRightKey, LeftLimpLeftKey, IncreaseSpeedKey, DecreaseSpeedKey, SpeedOneKey, SpeedTwoKey, \
  SpeedThreeKey, SpeedFourKey, SpeedFiveKey, SpeedSixKey, SpeedSevenKey, SpeedEightKey, SpeedNineKey, SpeedTenKey, CurrentSensitivity, Boosted, Time, KB, Debug):
  # Start timing execution of the current loop now.
  StartTime = Time.time()
  # Detect any speed change requests.
  CurrentSensitivity, SensitivityCounter = DetectKeyboardSensitivityChange(LastMessage, MinimumSensitivity, MaximumSensitivity, SensitivityCounter, DetectSensitivityInterval, DetectSensitivitySkipInterval, \
    CurrentSensitivity, DefaultSensitivity, SensitivityChangeAmount, KB, IncreaseSensitivityKey, DecreaseSensitivityKey, ExecutionDuration, DwellDuration, BeepDuration, NumberOfBuzzes, EnableSpeakerBeep, SpeakerGPIO, Debug)
  LastMessage, ExecutionDuration, CurrentSpeed, SpeedCounter = DetectKeyboardSpeedChange(LastMessage, SpeedCounter, DetectSpeedInterval, DetectSpeedSkipInterval, ExecutionDuration, DwellDuration, CurrentSensitivity, CurrentSpeed, KB, \
    IncreaseSpeedKey, DecreaseSpeedKey, SpeedOneKey, SpeedTwoKey, SpeedThreeKey, SpeedFourKey, SpeedFiveKey, SpeedSixKey, SpeedSevenKey, SpeedEightKey, SpeedNineKey, \
    SpeedTenKey, BeepDuration, NumberOfBuzzes, EnableSpeakerBeep, SpeakerGPIO, Debug)
  # Detect any motion requests.
  LastMessage, ExecutionDuration, CurrentSpeed, OriginalSpeed, Boosted = DetectKeyboardMotion(LastMessage, DebugStops, CurrentSpeed, OriginalSpeed, BeepDuration, NumberOfBuzzes, EnableSpeakerBeep, SpeakerGPIO, MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO, \
    MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO, RightBoostAmount, RightReductionAmount, RightLimpBoostAmount, RightLimpReductionAmount, LeftBoostAmount, \
    LeftReductionAmount, LeftLimpBoostAmount, LeftLimpReductionAmount, ForwardKey, BackwardKey, TurnRightKey, TurnLeftKey, RightLimpRighKey, RightLimpLeftKey, \
    LeftLimpRightKey, LeftLimpLeftKey, Boosted, ExecutionDuration, Time, KB, Debug)
  return LastMessage, StartTime, ExecutionDuration, CurrentSpeed, OriginalSpeed, CurrentSensitivity, SensitivityCounter, SpeedCounter, Boosted
#--------------------

#--------------------
# Track the number of iterations of the main loop for debugging purposes.
def TrackLoops(LastMessage, EnableLoopTracking, LoopCounter, LoopTracker, LoopAnnouncementInterval, MaxLoopCount, Debug):
  # Run loop tracking code only if enabled by configuration.
  if EnableLoopTracking == True:
    BreakLoop, LoopCounter, CurrentLoop = False, LoopCounter + 1, LoopTracker + LoopCounter
    # Determine if the LoopAnnouncementInterval specified by configuration has been reached.
    if LoopCounter == LoopAnnouncementInterval:
      LoopTracker, LoopCounter = CurrentLoop, 0
      # Inform the user that the LoopAnnouncementInterval specified by configuration has been reached.
      if Debug == True:
        LastMessage = PrintMessage(LastMessage, 'Execution Has Reached '+str(LoopTracker)+' Cycles.')
    # Determine if a maximum loop count has been specified as MaxLoopCount by configuration.
    if MaxLoopCount != 0:
      # Determine if the maximum loop count specified by configuration has been met.
      if CurrentLoop >= MaxLoopCount:
        # Inform the user that the maximum loop count specieid by configuration has been met & that execuition will now terminate.
        if Debug == True:
          LastMessage = PrintText('Execution has reached '+str(CurrentLoop)+' cycles. The maximum number of cycles allowed by configuration is '+str(MaxLoopCount)+\
            ' cycles. The loop will now end.')
        # Set the BreakLoop variable to True to prevent the loop from performing another iteration.
        BreakLoop = True 
  return LastMessage, LoopCounter, LoopTracker, BreakLoop
#--------------------

#--------------------
# Calculate the amount of sleep required to achieve the desired level of speed.
def PauseExecution(LastMessage, StartTime, ExecutionDuration, DefaultDwellDuration, Time, CurrentSpeed):
  # Stop timing execution of the current loop now.
  FinishTime = Time.time()
  # Calculate the amount of time that the current iteration of the loop has been running for.
  ElapsedTime = StartTime - FinishTime
  # Determine if the execution duration has elapsed already.
  if ElapsedTime <= ExecutionDuration:
    # Set an amount of time to pause execution to achieve the execution duration.
    SleepDuration = ExecutionDuration - ElapsedTime
    # Pause execution to wait for the execution duration to elapse.
    Time.sleep(SleepDuration)
  # If the execution duration has already elapsed don't pause execution at all.
  else:
    SleepDuration = 0
  # Calculate current dwell duration based on how much of it the execution duration has already consumed.
  DwellDuration = DefaultDwellDuration - SleepDuration
  # Determine if full speed is specified.
  if CurrentSpeed != 0:
    # If partial speed is specified then the motors must be disabled for the dwell duration.
    AllMotorsStop(MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO, MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO)
  # Determine if the dwell duration is a positive number before we try to pause execution for that amount of time.
  if DwellDuration < 0:
    # Determine if partial speed is specified.
    if CurrentSpeed != 0:
      # Output an error when a lag in execution is detected only if Debug is set by configuration.
      if Debug == True:
        LastMessage = PrintError(5, 'Execution Falling Behind.', False)
  else:
    Time.sleep(DwellDuration)
  return LastMessage, DwellDuration
#--------------------

#--------------------
# The main logic of the application.

# Attempt to import the configuration variables located in Robot_Motion_Config.py. 
try:
  from Robot_Motion_Config import *
# Handle the exception that is raised if the configuration file is missing.
except ModuleNotFoundError as ConfigError:
  # Display the raw exception if Debug is enabled by configuration.
  LastMessage = PrintError(6, 'Captured Exception, '+str(ConfigError)+'.', False)
  # Announce a fatal error if the configuration file cannot be loaded.
  LastMessage = PrintError(7, 'Could not Import Configuration File.', True)

# Print the start text.
PrintText(StartText)

# Initialize the operating environment.
LastMessage, SensitivityCounter, SpeedCounter, LoopCounter, LoopTracker, ExecutionDuration, CurrentSpeed, OriginalSpeed, CurrentSensitivity, DwellDuration, BreakLoop, Boosted, GPIO, Time, KB = InitializeEnvironment(SpeakerGPIO, \
  MotorRelayOnePositiveGPIO, MotorRelayOneNegativeGPIO, MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO, DefaultSpeed, DefaultExecutionDuration, DefaultDwellDuration, \
  DefaultSensitivity, Debug)

# Print the welcome text.
PrintText(WelcomeText)

# Start the loop which defines the timings of the electronic speed control (ESC).
# Break out of this loop if the max loop counter has been reached or if the Esc key is pressed.
while BreakLoop == False and not KB.is_pressed(CloseKey):

  # Listen for keyboard input when enabled by configuration.
  if EnableKeyboardInput == True:
  
    # Listen for & process requests from user input.
    LastMessage, StartTime, ExecutionDuration, CurrentSpeed, OriginalSpeed, CurrentSensitivity, SensitivityCounter, SpeedCounter, Boosted = ListenForKeyboardRequests(LastMessage, DebugStops, MinimumSensitivity, MaximumSensitivity, \
      SensitivityCounter, SpeedCounter, ExecutionDuration, DwellDuration, DefaultSensitivity, CurrentSpeed, OriginalSpeed, BeepDuration, NumberOfBuzzes, EnableSpeakerBeep, SpeakerGPIO, MotorRelayOnePositiveGPIO, \
      MotorRelayOneNegativeGPIO, MotorRelayTwoPositiveGPIO, MotorRelayTwoNegativeGPIO, RightBoostAmount, RightReductionAmount, RightLimpBoostAmount, RightLimpReductionAmount, LeftBoostAmount, \
      LeftReductionAmount, LeftLimpBoostAmount, LeftLimpReductionAmount, ForwardKey, BackwardKey, TurnRightKey, TurnLeftKey, RightLimpRightKey, RightLimpLeftKey, LeftLimpRightKey, \
      LeftLimpLeftKey, IncreaseSpeedKey, DecreaseSpeedKey, SpeedOneKey, SpeedTwoKey, SpeedThreeKey, SpeedFourKey, SpeedFiveKey, SpeedSixKey, SpeedSevenKey, SpeedEightKey, \
      SpeedNineKey, SpeedTenKey, CurrentSensitivity, Boosted, Time, KB, Debug)

  # Track & control application execution for debugging purposes. 
  LastMessage, LoopCounter, LoopTracker, BreakLoop = TrackLoops(LastMessage, EnableLoopTracking, LoopCounter, LoopTracker, LoopAnnouncementInterval, MaxLoopCount, Debug)

  # Throttle the application according to configuration settings & compute performance.
  LastMessage, DwellDuration = PauseExecution(LastMessage, StartTime, ExecutionDuration, DefaultDwellDuration, Time, CurrentSpeed)

# Print the goodbye text.
PrintText(GoodbyeText)

# Close the application.
exit(':)\n')
#--------------------