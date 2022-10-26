## Robot_Motion_Listener_3.py

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
By the time we forked into this iteration of the script we were using a new robot chassis.
This one had a metal frame and tracks instead of wheels. The frame was large enough to
allow us to mount the AGM batteries underneath the frame and the electronics neatly on top.
The motors were also larger and more powerful which allowed the robot to better cope with the
weight of all the batteries.

The goal of this iteration was to create some kind of variable speed control mechanism.
We accomplished this by creating a way to regulate the clock of the main loop.

### Process
This script was mostly about creating a reliable process to simulate the function of an ESC
using code. Efficiency and fine tuning would come later. Around this time we decided to put
considerably more effort into the project, thus this documentation was created and old versions
were archived.

### Technical Information
A typical brushed DC Electronic Speed Control (ESC) controls speed by setting a clock and
then powering an electric motor for a certain portion of that clock. To increase the speed
the ESC powers the motor for a longer duration during each clock cycle. The duration of time
that the motor is powered by the ESC is called the "pulse width" because if you look at the
signal on an oscilloscope you will notice that modulating the duration (width) of the signal
yields higher motor speed and power output.

To achieve this functionality using code instead of component hardware, we must first set a
clock frequency inside of our program, and then power the motor for a metered proportion of
each clock cycle. We already had the loop from the last iteration of our program, we just
needed a way to meter it to a stable frequency. To do this, we define a "Dwell Time" which
is basically just a period of time for the CPU to rest and do nothing. The dwell time has to
be just long enough for our CPU to be able to execute all code within the loop during one
cycle, and short enough to provide good throttle response at the motors.

But there is an point of diminishing returns to everything. If the base clock is too short
our relays might not be able to establish a stable connection before they are commanded to
switch off again. It is quickly becoming appearant that every piece of this puzzle will need
to be "right sized" for the model of Raspberry Pi, motors, batteries, and relays being used.
There are a lot of hardware variables to consider.

We also had to take into consideration the switching frequency of the RPI GPIO pins. Even if
our dwell time is 1/100th of 1 second (0.1khz) at low motor RPM we are actually toggling the
pins on and off in just 1/10th of each cycle. So even though our base clock is .1khz the GPIO
pins must be able to achieve speeds of up to 1khz in order to modulate reliably. In most cases
these numbers are probably dreadfully high, but they make the math easier for demonstration.

### Result
This iteration was such a success that version archives and documentation was created to
memorialize the process and inject some much needed dilligence into a very seat-of-the-pants
style project so far.

### Original File Header
> \# Robot_Motion_Listener_3.py

> \# A program to control Raspberry Pi Robots! 
> \# Written by Daniel Grimes & Justin Grimes.
> \# Licensed Under GNU GPLv3
> \# October 22nd, 2022
> \# Version v1.0

> \# This version of the program listens for keyboard inputs
> \# with standard Python modules.

> \# Designed with an RPi 4 Model B 