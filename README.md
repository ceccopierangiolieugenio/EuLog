# EuLog
Logfile Viewer in PyQt5

This is a tiny Python Qt5 experiment.
The main purpose is to practice with these technologies and realize a generic Log Viewer able to parse and display LogFiles of any size.

## Install
#### Win 7 - Win 10
(This procedure is based on Python 2.7)
* Install [Python 2.7](https://www.python.org/)
* From the cmd prompt, type:

        c:\Python27\python.exe -m pip install python-qt5

#### Linux
* Install [Python 2.7](https://www.python.org/)
* From the shell, type:

        pip install python-qt5

## Run
#### Win 7 - Win 10
* From the cmd prompt, type (inside the project folder):

        c:\Python27\python.exe EuLog.py

#### Linux
* From the shell, type (inside the project folder):

        python2 EuLog.py

## Testing Logfile
Inside the testing folder the '''create_log.py''' script can be used to generate a random Logfile that can be imported using the default setup.

##### Usage
        create_log.py <FILENAME> <LINES>

## Build Windows standalone executable

#### Environment
(This procedure is based on Python 2.7, py2exe[0.6.9])
* Install [Python 2.7](https://www.python.org/)
* Install [py2exe](https://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/)
* From the cmd prompt, type:

        c:\Python27\python.exe -m pip install python-qt5
* Run **build.win.bat**

The **dist** folder will contain the executable and all the required files
        
