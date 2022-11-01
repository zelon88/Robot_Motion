# APPLICATION NAME
#   Robot_Motion.py

# APPLICATION INFORMATION
#   Written by Daniel Grimes & Justin Grimes.
#   https://github.com/zelon88/Robot_Motion
#   Version v4.4, October 31st, 2022
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
#   Move Left (Left Channel Only):          Q
#   Move Right (Left Channel Only):         Z
#   Move Left (Right Channel Only):         E
#   Move Right (Right Channel Only):        C
#   Increase Sensitivity:                   ]
#   Decrease Sensitivity:                   [
#   Increase Speed by 1:                    =
#   Decrease Speed by 1:                    -
#   Set Speed To Minimum:                   0
#   Set Speed To Level 1:                   1
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
#--------------------

#--------------------
# Application Name.
# Set a string containing the name of this application to display to the user.
ApplicationName = str('Robot Motion')
#--------------------

#--------------------
# Version Information.
# Set a string containing the version of this application to display to the user.
VersionInfo = str('Version v4.4, October 31st, 2022')
#--------------------

#--------------------
# Start Text.
# Set the start text that is displayed when the application starts.
StartText = str('Starting '+ApplicationName+' '+VersionInfo+'.')
#--------------------

#--------------------
# Set a string containing a brief description of this application to display to the user.
ApplicationDescription = 'An application to control Raspberry Pi Robots!'
#--------------------

#--------------------
# Application Authors.
# Set a string containing the authors who wrote this application.
AuthorText = str('Written by Daniel Grimes & Justin Grimes.')
#--------------------

#--------------------
# Application Authors.
# Set a string containing the license information of this application to display to the user.
LicenseText = str('Licensed Under GNU GPLv3.')
#--------------------

#--------------------
# Command Prompt Text.
# Set a string containing the prompt for user input to display to the user.
PromptText = str('Enter a command...')
#--------------------

#--------------------
# Welcome Text.
# Set the welcome text that is displayed to the user when the application is ready to accept user input.
WelcomeText = str('Welcome to '+ApplicationName+'!\n'+ApplicationDescription+'\n'+AuthorText+'\n'+LicenseText+'\n'+PromptText)
#--------------------

#--------------------
# Goodbye Text.
# Set the goodbye text that is displayed to the user when the application closes.
GoodbyeText = str('Thanks for playing, Have a nice day!')
#--------------------

#--------------------
# Enable Debug Mode.
# Set the Debug flag to True to enable additional output.
# Set the Debug flag to False for optimal performance.
# This configuration entry has a significant impact on performance.
# Once you have your robot fully configured set this to False.
# Default is True.
Debug = bool(True)
#--------------------

#--------------------
# Enable Debug Stops Mode.
# Set the DebugStops flag to True to enable output on stop requests when Debug is also enabled.
# Set the DebugStops flag to False to disable output on stop requests in all cases.
# This configuration entry has a significant impact on performance.
# Once you have your robot fully configured set this to False.
#Default is False.
DebugStops = False
#--------------------

#--------------------
# Enable Speaker Beep.
# Set whether or not to output an indicator beep to a simple speaker.
# This configuration entry has a significant impact on performance.
# Default is True.
EnableSpeakerBeep = bool(True)
#--------------------

#--------------------
# Speaker Beep Duration.
# How long should indicator beeps last, in seconds.
# This configuration entry has a significant impact on performance.
# Default is 1 / 100.
BeepDuration = float(1 / 100)
#--------------------

#--------------------
# Number Of Speaker Buzzes.
# Set the number of buzzes that occur during BeepDuration.
# The frequency to buzz the speaker, relative to the frequency established by DefaultDwellDuration.
# Default is 10.
NumberOfBuzzes = float(3)
#--------------------

#--------------------
# Enable Loop Tracking.
# Set whether or not to track loops.
# Set to True to enable LoopAnnouncementInterval & MaxLoopCount.
# Set to False to disable LoopAnnouncementInterval & MaxLoopCount.
# This configuration entry has a minor impact on performance.
# Once you have your robot fully configured set this to False.
# Default is True.
EnableLoopTracking = bool(True)
#--------------------

#--------------------
# Loop Announcement Interval.
# Set the number of iterations of the main loop to announce.
# Only takes effect if EnableLoopTracking is set to True. 
# Default is 100000. 
LoopAnnouncementInterval = int(100000)
#--------------------

#--------------------
# Maximum Loop Count.
# Set the maximum number of loops before the application terminates.
# Only takes effect if EnableLoopTracking is set to True.
# Set to 0 to run an unlimited number of iterations until the Escape key is pressed.
# Default is 0.
MaxLoopCount = int(0)
#--------------------

#--------------------
# Default Dwell Duration.
# Set the amount of time for each loop to last.
# This controls how long each motor is unpowered during a move command.
# This controls the overall frequency of the speed control.
# This is basically controlling the MOSFET frequency in a traditional ESC.
# Must be longer than the Execution Duration.
# Default is 1 / 30.
# Multiples of the default work well.
DefaultDwellDuration = float(1 / 30)
#--------------------

#--------------------
# Default Execution Duration.
# Set the amount of time for each command to last, in seconds.
# This controls how long each motor is powered during a move command by default.
# This value is variable. The default value is only used during initialization.
# Must be shorter than the Dwell Duration.
# Default is DefaultDwellDuration / 10.
DefaultExecutionDuration = float(DefaultDwellDuration / 10)
#--------------------

#--------------------
# Default Speed Level
# Set the default speed to use before a speed has been specified.
# Default is 0.
DefaultSpeed = int(0)
#--------------------

#--------------------
# Default Sensitivity Level.
# Set the default sensitivity for the speed controller.
# Faster relays means you can increase this number.
# Default is 2500.
# Multiples of the default work well.
DefaultSensitivity = int(2500)
#--------------------

#--------------------
# The minimum sensitivity that is allowed to be set using the increase & decrease inputs.
# Default is 500
MinimumSensitivity = int(500)
#--------------------

#--------------------
# The minimum sensitivity that is allowed to be set using the increase & decrease inputs.
# Default is 10000
MaximumSensitivity = int(10000)
#--------------------

#--------------------
# Sensitivity Change Amount.
# The amount to adjust the sensitivity value of the ESC when the sensitivity change keys are pressed.
# Default is 50.
SensitivityChangeAmount = int(50)
#--------------------

#--------------------
# Right Turn Boost Amount.
# The number of steps to boost speed during right turns where both motors are used.
# Can help when motors are struggling during turns, making turns too sluggish.
# Set to 0 to not apply any speed level boost during right turns.
# Do not set lower than RightReductionAmount.
# Default is 2.
RightBoostAmount = int(2)
#--------------------

#--------------------
# Left Turn Boost Amount.
# The number of steps to boost speed during left turns where both motors are used.
# Can help when motors are struggling during turns, making turns too sluggish.
# Set to 0 to not apply any speed level boost during left turns.
# Do not set lower than LeftReductionAmount.
# Default is 2.
LeftBoostAmount = int(2)
#--------------------

#--------------------
# Right Turn Reduction Amount.
# The number of steps to reduce speed during right turns where both motors are used.
# Can help when motors are too powerful during turns, making turns too rapid.
# Set to 0 to not apply any speed level reduction during right turns.
# Do not set higher than RightBoostAmount.
# Default is 0.
RightReductionAmount = int(0)
#--------------------

#--------------------
# Right Turn Reduction Amount.
# The number of steps to reduce speed during left turns where both motors are used.
# Can help when motors are too powerful during turns, making turns too rapid.
# Set to 0 to not apply any speed level reduction during left turns.
# Do not set higher than LeftBoostAmount.
# Default is 0.
LeftReductionAmount = int(0)
#--------------------

#--------------------
# Right Limp Boost Amount.
# The number of steps to boost speed during right turns where only one motor is used.
# Can help when motors are struggling during turns, making turns too sluggish.
# Set to 0 to not apply any speed level boost during right turns.
# Do not set lower than RightReductionAmount.
# Default is 2.
RightLimpBoostAmount = int(2)
#--------------------

#--------------------
# Left Limp Boost Amount.
# The number of steps to boost speed during left turns where only one motor is used.
# Can help when motors are struggling during turns, making turns too sluggish.
# Set to 0 to not apply any speed level boost during left turns.
# Do not set lower than LeftReductionAmount.
# Default is 2.
LeftLimpBoostAmount = int(2)
#--------------------

#--------------------
# Right Limp Reduction Amount.
# The number of steps to reduce speed during right turns where only one motor is used.
# Can help when motors are too powerful during turns, making turns too rapid.
# Set to 0 to not apply any speed level reduction during right turns.
# Do not set higher than RightBoostAmount.
# Default is 0.
RightLimpReductionAmount = int(0)
#--------------------

#--------------------
# Right Limp Reduction Amount.
# The number of steps to reduce speed during left turns where only one motor is used.
# Can help when motors are too powerful during turns, making turns too rapid.
# Set to 0 to not apply any speed level reduction during left turns.
# Do not set higher than LeftBoostAmount.
# Default is 0.
LeftLimpReductionAmount = int(0)
#--------------------

#--------------------
# Detect Sensitivity Interval
# Set the cycle interval for performing sensitivity update detection.
# Default is 3.
DetectSensitivityInterval = int(3)
#--------------------

#--------------------
# Detect Sensitivity Skip Interval
# Set the number of cycles to skip sensitivity update detection after a sensitivity change is performed.
# Default is 8.
DetectSensitivitySkipInterval = int(8)
#--------------------

#--------------------
# Detect Speed Interval
# Set the cycle interval for performing speed update detection.
# Default is 3.
DetectSpeedInterval = int(3)
#--------------------

#--------------------
# Detect Speed Skip Interval
# Set the number of cycles to skip speed update detection after a speed change is performed.
# Default is 8.
DetectSpeedSkipInterval = int(8)
#--------------------

#--------------------
# GPIO Pin Numbering Mode.
# Set the GPIO pin numbering mode.
# Supports BCM and BOARD numbering styles.
# Default is BCM.
GPIOMode = str('BCM')
#--------------------

#--------------------
# Enable GPIO Warnings.
# Set whether or not to display GPIO related warnings in the console.
# Default is False.
GPIOWarnings = bool(False)

#--------------------
# GPIO Pin Configuration - Speaker.
# Set the GPIO pin to use for controlling the speaker.
# Default is 16.
SpeakerGPIO = int(16)
#--------------------

#--------------------
# GPIO Pin Configuration - Motor 1, Positive.
# Set the GPIO pins to use for controlling the positive output to Motor Relay 1.
# Default is 26.
MotorRelayOnePositiveGPIO = int(26)
#--------------------

#--------------------
# GPIO Pin Configuration - Motor 1, Negative.
# Set the GPIO pins to use for controlling the negative output to Motor Relay 1.
# Default is 19.
MotorRelayOneNegativeGPIO = int(19)
#--------------------

#--------------------
# GPIO Pin Configuration - Motor 2, Positive.
# Set the GPIO pins to use for controlling the positive output to Motor Relay 2.
# Default is 20.
MotorRelayTwoPositiveGPIO = int(20)
#--------------------

#--------------------
# GPIO Pin Configuration - Motor 2, Negative.
# Set the GPIO pins to use for controlling the negative output to Motor Relay 2.
# Default is 21.
MotorRelayTwoNegativeGPIO = int(21)
#--------------------

#--------------------
# Keyboard Input Configuration - Enable Keyboard Input.
# Enable listening for requests from the keyboard.
# Does not change the function of the CloseKey.
# Default is True.
EnableKeyboardInput = bool(True)
#--------------------

#--------------------
# Keyboard Input Configuration - All Motors Forward.
# The key on the keyboard to command the robot forward.
# Default is w.
ForwardKey = str('w')
#--------------------

#--------------------
# Keyboard Input Configuration - All Motors Backward.
# The key on the keyboard to command the robot backward.
# Default is s.
BackwardKey = str('s')
#--------------------

#--------------------
# Keyboard Input Configuration - All Motors Turn Right.
# The key on the keyboard to command the robot to turn right.
# Default is a.
TurnRightKey = str('d')
#--------------------

#--------------------
# Keyboard Input Configuration - All Motors Turn Left.
# The key on the keyboard to command the robot to turn right.
# Default is d.
TurnLeftKey = str('a')
#--------------------

#--------------------
# Keyboard Input Configuration - Right Motors Turn Right.
# The key on the keyboard to command the robot to turn right using only right motors.
# Default is w.
RightLimpRightKey = str('c')
#--------------------

#--------------------
# Keyboard Input Configuration - Right Motors Turn Left.
# The key on the keyboard to command the robot to turn left using only right motors.
# Default is 2.
RightLimpLeftKey = str('e')
#--------------------

#--------------------
# Keyboard Input Configuration - Left Motors Turn Right.
# The key on the keyboard to command the robot to turn right using only left motors.
# Default is z.
LeftLimpRightKey = str('q')
#--------------------

#--------------------
# Keyboard Input Configuration - Left Motors Turn Left.
# The key on the keyboard to command the robot to turn left using only left motors.
# Default is q.
LeftLimpLeftKey = str('z')
#--------------------

#--------------------
# Keyboard Input Configuration - Increase Sensitivity by the Sensitivity Change Amount.
# Default is ].
IncreaseSensitivityKey = str(']')
#--------------------

#--------------------
# Keyboard Input Configuration - Decrease Sensitivity by the Sensitivity Change Amount.
# Default is [.
DecreaseSensitivityKey = str('[')
#--------------------

#--------------------
# Keyboard Input Configuration - Increase Speed By 1.
# The key on the keyboard to increase the currently selected speed by 1.
# Default is =.
IncreaseSpeedKey = str('=')
#--------------------

#--------------------
# Keyboard Input Configuration - Decrease Speed By 1.
# The key on the keyboard to decrease the currently selected speed by 1.
# Default is -.
DecreaseSpeedKey = str('minus')
#--------------------

#--------------------
# Keyboard Input Configuration - Set Speed Level To 1.
# The key on the keyboard to set the speed to level one.
# Default is 1.
SpeedOneKey = str('1')
#--------------------

#--------------------
# Keyboard Input Configuration - Set Speed Level To 2.
# The key on the keyboard to set the speed to level two.
# Default is 1.
SpeedTwoKey = str('2')
#--------------------

#--------------------
# Keyboard Input Configuration - Set Speed Level To 3.
# The key on the keyboard to set the speed to level three.
# Default is 3.
SpeedThreeKey = str('3')
#--------------------

#--------------------
# Keyboard Input Configuration - Set Speed Level To 4.
# The key on the keyboard to set the speed to level four.
# Default is 4.
SpeedFourKey = str('4')
#--------------------

#--------------------
# Keyboard Input Configuration - Set Speed Level To 5.
# The key on the keyboard to set the speed to level five.
# Default is 5.
SpeedFiveKey = str('5')
#--------------------

#--------------------
# Keyboard Input Configuration - Set Speed Level To 6.
# The key on the keyboard to set the speed to level six.
# Default is 6.
SpeedSixKey = str('6')
#--------------------

#--------------------
# Keyboard Input Configuration - Set Speed Level To 7.
# The key on the keyboard to set the speed to level seven.
# Default is 7.
SpeedSevenKey = str('7')
#--------------------

#--------------------
# Keyboard Input Configuration - Set Speed Level To 8.
# The key on the keyboard to set the speed to level eight.
# Default is 8.
SpeedEightKey = str('8')
#--------------------

#--------------------
# Keyboard Input Configuration - Set Speed Level To 9.
# The key on the keyboard to set the speed to level nine.
# Default is 9.
SpeedNineKey = str('9')
#--------------------

#--------------------
# Keyboard Input Configuration - Set Speed Level To 10.
# The key on the keyboard to set the speed to level ten.
# Default is 0.
SpeedTenKey = str('0')
#--------------------

#--------------------
# Keyboard Input Configuration - Close Application.
# The key on the keyboard to close the application.
# This key is not affected by EnableKeyboardInput,
# Default is esc.
CloseKey = str('esc')
#--------------------
