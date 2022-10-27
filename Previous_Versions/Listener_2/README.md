## Robot_Motion_Listener_2.py

### Preface
This README.md file reads like a blog post and was created long after the code it is
meant to represent.

In this document I (zelon88) will share my experiences building a robot kit with my 
son. We built this kit as a learning experience so this section will contain plenty 
of errors, mistakes, and misunderstandings about a variety of topics. I will share 
our reasoning, intentions, & lessons learned along the way. Even if they are flawed.
Wherever possible, I will highlight these flaws and elaborate on them. This is part of 
my development process. If you're following along I'd like you to know that not every
script contained in this repository is "good." Some scripts contain errors or obvious
flaws. None of them are malicious, but that doesn't mean they are all inherintly safe.
When playing with RPI GPIO, large AGM batteries, and high current DC electronics there
exists a high probability that you will damage something. If you run these early scripts
you are following in the footsteps of people who are not experts in any field other than
taking initiative. Be warned that you may become frustrated at some of these things.
Especially if you are a professional robotics/electrical/computer engineer.

### Background
I had bought my son a new metal robot chassis kit for Christmas because the plastic one
had given us everything it had over the years. It was caked in hot glue and the motors
were mismatched in color due to having been replaced and a couple were partially melted.
It was a good robot, but it didn't owe us anything anymore. The chassis was always too 
small for the amount of batteries and electronics. The new chassis was about twice as big
and the motors were too. Plenty of space for batteries, electronics, and future expansion.
It would take my son a couple months to get around to building the kit, but once built
it didn't take long to get everything rewired. 

### Process
We cleaned this iteration up nice and focused on making it more application-like. 
We didn't really continue to develop this as a fork once we saw the bug it contained and
realized the potential that was on the table. We were not far off from having an ESC!
This iteration got forked into Robot_Motion_Listener_3.py which is where the bulk of 
research & development into making an ESC went. This iteration still contains the motor
switching bug, which was never patched. This bug has a serious impact on motor performance.

This script was an attempt to combine the benefits of the listener developed previously
with the programming flexibility we were enjoying with standard Python modules. We already
knew what the functionality we wanted looked like, we just needed to materialze that 
functionality in a style we could live & grow with. Also, our application was starting to
become more and more application-like with much of main loop starting to be set in stone.
While this was certainly shaping up to be the correct direction for the project, we 
inadvertantly stumbled into a bug that would lead to a massive discovery!

### Technical Information
This script was only 160 lines of code and corrected the syntax inconsistencies we didn't 
like about the previous iteration. We switched from using the pynput module to the keyboard
module for handling key presses. We incorporated this and much of the motor command logic 
into the loop itself. By doing this we realized we were switching our motors on and off at
the same rate as our loop. This greatly reduced the observed performance of the motors, but
gave us an interesting idea! What if we could harness this bug and use it to emulate the
functionality of a MOSFET style electronic speed control?

We were intrigued, but laser focused on driving the robot. So we finalized this version to
allow us to move our robot around and forked the project yet again so we could focus on 
researching if we had the capability to create an ESC. At this point there were more questions
than answers. We didn't know if our cheap relay board would survive or perform at high
frequency. We didn't know if the RPI could toggle GPIO fast enough to make a meaningful
frequency. We didn't know if the RPI had enough processing speed or low enough latency to run
all of this code in between cycles of this unknown frequency. 

### Result
This iteration contained a bug that led to the realization that we were not far off from
creating a MOSFET style electronic speed control (ESC) for brushed DC motors. We finalized
this version of the application, including the bug, which reduces motor performance considerably.
Regardless we put this code to good use in a new robot chassis.

### Original File Header
> \# Robot_Motion_Listener.py

> \# A program to control Raspberry Pi Robots! 
> \# Written by Daniel Grimes & Justin Grimes.
> \# Licensed Under GNU GPLv3
> \# November 9th, 2019
> \# Version v1.0

> \# This version of the program listens for keyboard inputs
> \# with standard Python modules.

> \# Designed with an RPi 2 Model B
