# PythonTest
Simple GUI app for [libplctag](https://github.com/libplctag/libplctag) python wrapper. 

Intended to be used solely as a testing tool (not fit for any production environment).

Make sure to check the pictures in the "screenshots" folder on how to setup the folder structure (the required and the optional expanded for Android).

Get libplctag libraries here:

- libplctag [releases](https://github.com/libplctag/libplctag/releases), v2.2.0 recommended

# Functionality
- Only a single value will be displayed per tag entered, either of string/char/integer/float...etc.
- The default values can be changed for the app's startup.
- The app provides automated READ and doesn't include WRITE functionality.
- The "Get Tags" button will fetch ControlLogix tags and double-clicking any of the fetched tags will copy it to the clipboard.
- The IP Address, Path and Tag text boxes offer right-click "Paste" functionality
- The Custom String Length has to be specified when the "custom string" data type is selected.
- Modbus functionality of the libplctag library is not included in this app.

There might be bugs in the app. Not everything could be tested by me, since I don't have access to all the different PLCs supported by the libplctag library.
See the libplctag website for all PLCs supported by the library.

# Usage

All it takes is to:

- Install python on your device (this was tested with v3.9 but might work with older versions).
- Create the required folder structure inside a folder of your choice, download plctag_gui.py file and add it to that folder.
- One way to run it would be from the command prompt in Windows, by navigating to your folder and running the file with "python plctag_gui.py"

# Licensing
This is MIT licensed.

# Trademarks
Any and all trademarks, either directly on indirectly mentioned here, belong to their respective owners.

# Useful Resources
Other open source projects with similar app:
- The [pylogix](https://github.com/dmroeder/pylogix) repository.
- The [pycomm3](https://github.com/ottowayi/pycomm3) repository.
