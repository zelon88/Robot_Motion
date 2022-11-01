## ROBOT MOTION

### APPLICATION INFORMATION ...

Copyright on 10/25/2022 by Justin Grimes, www.github.com/zelon88. This application is intended to turn any Raspberry Pi with a 40 pin GPIO header into a 2 channel Electronic Speed Control (ESC) for brushed DC motors arranged in a skid-steer configuration. Perfect for skid steer robots or other electric vehicles. When Robot_Motion.py is run in a terminal as root, this application will initialize the 40 pin GPIO header of the Raspberry Pi computer using the pin configuration specified in the configuration file Robot_Motion_Config.py and listen for keyboard input. When keyboard input is detected the GPIO pins specified will be toggled in such a way as to simulate the signal behavior of a dual motor, skid-steer, MOSFET-style ESC.

Currently only keyboard input is supported. Basic movement is controlled using the W, S, A, and D keys. Individual motor channels can be controlled using the Q, E, Z, and C keys. Speed can be adjusted in 10 discreet steps using the 1, 2, 3, 4, 5, 6, 7, 8, 9, and 0 keys with 1 being minimum speed and 0 being maximum speed. Speed adjustments are applied to both motor channels and cannot be controlled independant of one another. This application can be halted at any time by pressing the Esc key. Within the application logic valid keyboard inputs are known as requests, although there is no verification mechanism and all requests are implied to be approved. Currently requests are named as such merely to provide logical and syntactical separation between input and output operations. Requests are input operations which trigger corresponding output operations known internally as commands. Commands result in GPIO output intended to trigger an action by the attached hardware. If enabled by configuration and if supported by hardware this application supports beeping to an attached buzzer or speaker upon execution of a valid move command.

To achieve variable motor speed, this application initializes a loop which generates a steady clock at a frequency defined by the DefaultDwellDuration configuration variable. At the start of every clock cycle, keyboard input is detected and parsed through a filter to determine if any move commands are being requested. If a move command is requested this application will activate the configured GPIO pins for a portion of the current clock cycle. The portion of the clock cycle that the pin remains activated is known internally as the ExecutionDuration. The balance of the clock cycle is known internally as the DwellDuration. The DefaultDwellDuration specified in Robot_Motion_Config.py represents the entire clock cycle which equals the sum of ExecutionDuration plus DwellDuration. If we plot this GPIO activity on an oscilloscope we would see that the DefaultDwellDuration of this loop creates the frequency of the ESC and the ExecutionDuration sets the pulse width of the ESC's duty cycle and the DwellDuration sets the period of the ESC's duty cycle. The input keys from 1 through 0 can be considered as a proportion of available motor power, with the 1 key representing 10% power, the 5 key representing 50% power, and the 0 key representing 100% power.

After installation of this application the timing of DefaultDwellDuration must be adjusted to match the attached hardware. Running the relays too quickly will result in reduced relay performance and longevity. Running the relays too slowly will provide poor performance and throttle response. The GPIO of most Raspberry Pi computers can achieve higher frequencies than most relays, but every configuration is different. It is best to look up the datasheet for the relays being used and set the DefaultDwellDuration configuration variables to align with the capabilities of your relays.

-----------------------------------------------------------------------------------

### LICENSE INFORMATION ...

This project is protected by the GNU GPLv3 Open-Source license.

-----------------------------------------------------------------------------------

### DEPENDENCY REQUIREMENTS ... 

This application must be run as root on a Raspberry Pi 2 computer running any version of Raspberry Pi OS with a default installation of Python 3.6 or later with the RPi and keyboard libraries installed. 

Any size and number of motors is supported on each channel provided the relays being used are adequate for the load. This application only emulates the signal behaviour of an ESC, not the load rating. Do not exceed the maximum supported GPIO current rating for your specific model of Raspberri Pi computer. A Raspberry Pi computer cannot handle the current required to drive any DC electric motor and will be damaged if you attach a motor directly to the GPIO pins. This application assumes the user will attach the GPIO pins to external relays that are capable of handling the load requirements of the specific electric motors being used. This application will supply a signal to the relays via GPIO output that causes the relays to emulate the behavior of a MOSFET-style ESC.
  
-----------------------------------------------------------------------------------

### VALID SWITCHES / ARGUMENTS / USAGE ...

Quick Start Example:

     ~$ cd /home/pi/Robot_Motion
     /home/pi/Robot_Motion$ sudo python Robot_Motion.py

Step By Step Instructions:

1. Open a terminal.
2. Make sure all dependencies are installed. `pip install keyboard RPi`
3. Navigate to the directory where the Robot_Motion Application application is stored. `cd /path/to/Robot_Motion`
4. Use your favorite text editor to adjust the configuration file named `Robot_Motion_Config.py`.
5. Run this application as root with Python. `sudo python Robot_Motion.py`
  
Supported Keyboard Inputs Include:

     Move Forward:                           W
     Move Backward:                          S
     Move Left:                              A
     Move Right:                             D
     Move Left (Left Channel Only):          Q
     Move Right (Left Channel Only):         Z
     Move Left (Right Channel Only):         E
     Move Right (Right Channel Only):        C
     Increase Sensitivity:                   ]
     Decrease Sensitivity:                   [
     Increase Speed by 1:                    =
     Decrease Speed by 1:                    -
     Set Speed To Minimum:                   0
     Set Speed To Level 1:                   1
     Set Speed To Level 2:                   2
     Set Speed To Level 3:                   3
     Set Speed To Level 4:                   4
     Set Speed To Level 5:                   5
     Set Speed To Level 6:                   6
     Set Speed To Level 7:                   7
     Set Speed To Level 8:                   8
     Set Speed To Level 9:                   9
     Set Speed To Level 10:                  0
     Close Application:                      Esc

------------------------------------------------------------------------------------
