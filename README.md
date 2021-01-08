# Fraction Collector - Collection Module
This repository holds python code for and anything related to the fraction collector program 
that is part of a larger program that controls the microfluidic nanoparticle production system. 
The paper describing the system can be found here:
Loy, D.M.; Krzysztoń, R.; Lächelt, U.; Rädler, J.O.; Wagner, E. 
Controlling Nanoparticle Formulation: A Low-Budget Prototype for the Automation of a Microfluidic Platform. Processes 2021, 9, 129. 
https://doi.org/10.3390/pr9010129

## Getting Started
1. Download all python files and save them to one dedicated folder on your raspberry pi.
2. Run main.py with a python interpreter (python version 3.x, tested on v. 3.7).
3. Follow the instructions printed by the console.

### Prerequisites
All modules used in this program are installed by default in Raspbian. 
To make sure that the RPi.GPIO module is at the latest version check out this Wiki entry on the homepage of the project:
https://sourceforge.net/p/raspberry-gpio-python/wiki/install/


### Installing

1. Start the raspberry pi, connect to it via ssh or use it in desktop mode. 
2. Use the command line to navigate to the desired folder the program should be written to.
3. Use ‘git’ to copy the syringe pump repository from GitHub to the Raspberry pi.
    ```
    git clone https://github.com/Dominikmloy/fraction-collector-program.git
    ```
    If the folder already exists, you will get an error.
    --> Either remove the folder (CAVE: It deletes all your logs!) and execute git clone again.
    ```
    rm -r fraction-collector-program
    git clone https://github.com/Dominikmloy/fraction-collector-program.git
    ```
    -->	Or update your repository:
    ```
    cd fraction-collector-program
    git pull origin master
     ```
4. open the repository and start the example program "main.py" to see how the fraction collector works
    ```
    sudo python3 main.py
    ```
    A video of the execution of this example program is published here as well: 
    ```
    FractionCollector_DominikLoy.mp4
    ```    


## Built With
* PyCharm 2019.1.3

## Versioning
* Version 1.0

## Authors

* **Dominik Loy** 

## License
CC BY 4.0
https://creativecommons.org/licenses/by/4.0/
## Acknowledgments

* **Adrian Loy** - proof reading, answering millions of questions, python wizard - 
* **Thomas Unterlinner** - setting up and building the fraction collector - 

