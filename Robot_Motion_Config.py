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
# Set a string containing the name of this application to display to the user.
ApplicationName = str('Robot Motion')
#--------------------

#--------------------
# Set a string containing the version of this application to display to the user.
VersionInfo = str('Version v4.3, October 27th, 2022')
#--------------------

#--------------------
# Set the start text that is displayed when the application starts.
StartText = str(ApplicationName+'\n'+VersionInfo)
#--------------------

#--------------------
# Set the welcome text that is displayed to the user when the application is ready to accept user input.
WelcomeText = str('An application to control Raspberry Pi Robots! \nWritten by Daniel Grimes & Justin Grimes.\nLicensed Under GNU GPLv3. \nEnter a command...')
#--------------------

#--------------------
# Set the goodbye text that is displayed to the user when the application closes.
GoodbyeText = str('Thanks for playing, Have a nice day! :)')
#--------------------

#--------------------
# Set the Debug flag to True to enable additional output.
# Set the Debug flag to False for optimal performance.
# This configuration entry has a significant impact on performance.
# Once you have your robot fully configured set this to False.
# Default is True.
Debug = bool(True)
#--------------------

#--------------------
# Set whether or not to output an indicator beep to a simple speaker.
# Enabling speaker beep will reduce potential max frequency by BeepDuration.
# Default is True.
EnableSpeakerBeep = bool(True)
#--------------------

#--------------------
# How long should indicator beeps last, in seconds.
# Default is 1 / 10000.
BeepDuration = float(1 / 10000)
#--------------------

#--------------------
# The duration of the 'Bee' in the indicator beep, in seconds.
# Default is BeepDuration / 3.
BeDuration = float(BeepDuration / 3)
#--------------------

#--------------------
# The duration of the 'Eep' in the indicator beep, in seconds.
# Default is BeepDuration / 3.
EpDuration = float(BeepDuration / 3)
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
# Must be longer than the Execution Duration.
# Default is 1 / 30.
# Multiples of the default work well.
DefaultDwellDuration = float(1 / 30)
#--------------------

#--------------------
# Set the amount of time for each command to last, in seconds.
# This controls how long each motor is powered during a move command by default.
# This value is variable. The default value is only used during initialization.
# Must be shorter than the Dwell Duration.
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
# Default is 2500.
# Multiples of the default work well.
DefaultSensitivity = int(2500)
#--------------------

#--------------------
# Set the GPIO pin numbering mode.
# Supports BCM and BOARD numbering styles.
# Default is BCM.
GPIOMode = str('BCM')
#--------------------

#--------------------
# Set whether or not to display GPIO related warnings in the console.
# Default is False.
GPIOWarnings = bool(False)

#--------------------
# Set the GPIO pin to use for controlling the speaker.
# Default is 16.
SpeakerGPIO = int(16)
#--------------------

#--------------------
# Set the GPIO pins to use for controlling the positive output to Motor Relay 1.
# Default is 26.
MotorRelayOnePositiveGPIO = int(26)
#--------------------

#--------------------
# Set the GPIO pins to use for controlling the negative output to Motor Relay 1.
# Default is 19.
MotorRelayOneNegativeGPIO = int(19)
#--------------------

#--------------------
# Set the GPIO pins to use for controlling the positive output to Motor Relay 2.
# Default is 20.
MotorRelayTwoPositiveGPIO = int(20)
#--------------------

#--------------------
# Set the GPIO pins to use for controlling the negative output to Motor Relay 2.
# Default is 21.
MotorRelayTwoNegativeGPIO = int(21)
#--------------------