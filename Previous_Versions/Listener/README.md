## Robot_Motion_Listener.py

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
This script was created as an attempt to overcome the execution duration of the first
script limiting control granularity. We also wanted to try to accomplish the same result
using pynput keyboard listeners, which proved to be too much work & not clean enough.

### Process
We spent a little while refactoring about half the code for this iteration. We continued
operating the robot with this code for a while as we mulled over what we wanted the next 
fork to look like.

### Result
We iterated on this idea by switching to a different library that was more aligned
with our style. This iteration demonstrated just how flexible programming is. 
We spent time working on an idea that provided indirect value by narrowing down our direction. 
There is value in development, even if the thing you developed is immediately supersceded by 
something else. There's no need to fear, the undo button is here!

Part of the reason why I don't like mixing and matching a million Python modules is you 
then have to write janky code in a mish-mashed manajare of styles. You're almost forced to 
write code in the same style as the module author unless you want unreadable code. I 
especially find dot notation frustrating because it makes no sense linguistically. 
You can't show dot notation to a non-programmer and expect them to know what's going on.
Functional or procedural programming is much more approachable in this regard.
The human brain is not very object oriented. Humans think in word documents, not spreadsheets.
Humans are good at retaining patterns, procedures, techniques, and algorithms. 
Humans are not good at retaining data, data types, constraints, requirements, or attributes. 

### Original File Header
> \# Robot_Motion_Listener.py

> \# A program to control Raspberry Pi Robots! 
> \# Written by Daniel Grimes & Justin Grimes.
> \# Licensed Under GNU GPLv3
> \# November 9th, 2019
> \# Version v1.2

> \# This version of the program listens for keyboard inputs
> \# with pynput.

> \# Designed with an RPi 2 Model B
