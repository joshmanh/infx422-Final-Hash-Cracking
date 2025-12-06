# INFX 422 Final Project

## **Note**: documentation is available by going to ./docs/build/html/index.html

### Author:

Joshua Huber

### Project Description
This project involves a python script that allows the user to input a hashed password file. Using a dictionary file, the program is able to detect which
hashing algorithm was used to hash the passwords. The program compares the hashed passwords of the input file with the hashed passwords of the output file.
If it finds a match, the program records the match, saving the time, the number of attempts, and the plaintext password.
After it has finished comparing all available passwords, the program outputs the results in the terminal.

### How to Run:

This project uses **python 3.11** with a virtual environment. It was created on a Linux machine, therefore the filepath syntax will match that of Linux. Attempting to run this on Windows will not work properly. It also utilizes **Git LFS** to handle the large
dictionary files. To run this project, please do the following:

- ensure you have python 3.11 installed
- ensure you have git lfs installed
- clone the repository using `git lfs clone https://github.com/joshmanh/infx422-Final-Hash-Cracking.git`
- navigate to the project directory
- setup a project virtual environment using `python3.11 -m venv venv`
- activate the virtual environment using `source venv/bin/activate`
- install the requirements using `pip install -r requirements.txt`
- run the program from within the project using `python3.11 main.py`

### Notes:

- first test: use txt with txt
- second test: use csv with csv
- third test: use json with csv