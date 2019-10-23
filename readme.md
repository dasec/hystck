# What is hystck
Hystck is a tool that aims towards the automatic generation of traffic through multiple applications.
It was first developed in 2013 and is continuing to evolve and expand. Supported applications
include Firefox, Thunderbird, Pidgin and a variety of botnet attacks. There are further applications
hystck can emulate user input for, but they are of little interest for the generation of network traffic.

## Where do I find the documentation?
The documentation can be found in ```docs/src/```. As the folder name suggests this only contains the source 
files of the documentation. In order to get it in readable format you need to install sphinx and inside the folder
run the command ```make html```. After this you will find the newest documentation in HTML format in the subfolder
```_build/html```. Just open the index.html with the browser of your choosing.

## General Information describing hystck
* Client-Server architecture.
* Python 2.7 Codebase