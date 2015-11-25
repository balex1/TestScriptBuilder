This repository is currently under active development.

This is designed to be a system which allows for long-term tracking of test scripts for large-scale software systems.

This is written in Python, leveraging the Kivy and SQLAlchemy libraries.

More information to come.

#Dependency Installs:

##Windows Install

###Install Kivy
1.	Install the Kivy Portable Package for Python 2.7, following the [install instructions](http://kivy.org/docs/installation/installation-windows.html)

###Install SQLAlchemy

1.	Find the Python Distribution shipped with your Kivy package (it’s located inside the Kivy folder, wherever you unzipped it to).  Copy the path to the python executable.

2.	Open the command prompt & run the following command:

```
""Path_to_Python_Executable"\python.exe -m pip install sqlalchemy
```

a.	For instance, my system compiled successfully with:

```
C:\Users\ABarry.US\Documents\Development\Python\Kivy-1.9.0-py2.7-win32-x86\python27\python.exe -m pip install sqlalchemy
```

###Install OpenPyXL

4.	Get the Python Distribution shipped with your Kivy package again and copy the path to the python executable

5.	Run the following command:

```
""Path_to_Python_Executable"\python.exe -m pip install openpyxl
```

###Start the Application

6.	Follow [the instructions](http://kivy.org/docs/installation/installation-windows.html#start-a-kivy-application) to start the application


##Linux Install

###Install Python

1.	Install Python (may not be necessary depending on distribution & version.  For instance, Python is included with Ubuntu 14.04 and later)

###Install Kivy

2.	Install Kivy using your package manager per the instructions here: http://kivy.org/docs/installation/installation-linux.html

###Install SQLAlchemy

3.	Install SQLAlchemy using PIP: sudo pip install sqlalchemy

###Install OpenPyXL

4.	Install OpenPyXL using PIP: sudo pip install openpyxl

###Start the Application

4.	Start the application using: sudo python TestScriptBuilder


Alex
