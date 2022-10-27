## Robot_Motion.py

### Preface
In this section I (zelon88) will share my experiences building a robot kit with my 
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
This original script was created in just a few minutes as a proof-of-concept by 
myself (zelon88) and my son. We designed this script to control a 4 motor robot
my son got as a gift from Micro Center. We both have years of experience with hobby
grade R/C cars, but this robot kit would provide a great learning experience beyond
simply following colorful pictures printed in a user manual. We would both go on to 
learn a tremendous amount and have a lot of fun with this little plastic robot kit.

### Process
The robot kit has enough room for several batteries and an RPI. We attached an RPI2 
because I had one laying around. I gave my son a quick tutorial on Thonny and Python
and before long we were brainstorming psuedo code out loud in the living room. We 
hashed out a quick program with several constraints. 
The code had to be super minimalistic. No error handling, minimal branching.
The code had to use the most basic language features to be approachable & unintimidating.
The code had to be clean & follow best practices.
The code had to use standard Python libraries that were included with RPI OS.
The code had to control 4 motors in 2 pairs of 2.
The code had to provide the ability to turn the robot in a "skid-steer" configuration.
The code had to have 4 main features. Move forward, backward, left, & right.
The code would be a complete, cohesive application with a clear start, middle, & end.
No spaghetti because we're trying to teach a kid.
Minimal abbreviations so the code is fully human readable.
No cowboy stuff because we want to demonstrate going the extra mile is worthwhile.
No fancy modules because we want to learn how to cook for ourselves.

### Technical Information
This script was only 146 lines of code and did not offer very precise motor control.
This script used a command queue instead of a real-time-listener. Commands would
run for a predetermined amount of time in the order they were received. As a result
it was possible for the user to input commands faster than the robot could execute them.
There was also a notable lack of granularity to movement operations. Turning was especially
difficult to do with accuracy, as there was no mechanism to stop a command while it was 
being executed by the robot. So if the execution duration was set to 1 second, the robot
would execute every "turn left" command for 1 entire second. Turning just one or two degrees 
at a time is impossible.

### Result
We quickly burned out the gear motors, replaced them, and burned out the replacements.
We learned a lot including that the motors were simply too small for the weight
of the batteries. As a result, the current draw was putting us over the edge of what 
the electronics could supply. The voltage drop from the motors would kill the Raspberry
Pi causing it to reboot and kill the application. We tried adding massive capacitors but
these only helped until the batteries dropped to about 50-75% capacity. Ultimately our vision
for this robot had already outgrown the chassis and drivetrain we were working with.

### Original File Header
> \# Robot_Motion.py

> \# A program to control Raspberry Pi Robots! 
> \# Written by Daniel Grimes & Justin Grimes.
> \# Licensed Under GNU GPLv3
> \# November 9th, 2019
> \# Version v1.1
