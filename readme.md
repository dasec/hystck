# What is hystck
Hystck is a tool that aims towards the automatic generation of traffic through multiple applications.
It was first developed in 2013 and is continuing to evolve and expand. Supported applications
include Firefox, Thunderbird, Pidgin and a variety of botnet attacks. There are further applications
hystck can emulate user input for, but they are of little interest for the generation of network traffic.

## What do different console outputs mean

There are different categories of outputs:
1) notset
1) debug
1) info
1) warning
1) error
1) critical

For info there are different starting symbols describing different actions:
- \[i] means: Information; May mean, that a function is not fully implemented yet.
- \[~] means: Task started and in progress.
- \[+] means: Task successfully ended.
- \[X] means: There have been errors and the program has been terminated.

## Where do I find the documentation?
Ready compiled html version of the documentation can be found in ```docs/build```.


The documentation can be found in ```docs/src/```. As the folder name suggests this only contains the source 
files of the documentation. In order to get it in readable format you need to install sphinx and inside the folder
run the command ```make html```. After this you will find the newest documentation in HTML format in the subfolder
```_build/html```. Just open the index.html with the browser of your choosing.

## Installation Host

## Installation Guest



