# PythonTest
Simple GUI app for [libplctag](https://github.com/libplctag/libplctag) python wrapper. 

Still work in progress but currently functional for reading atomic types and their arrays, bits, strings as well as getting tags from ControlLogix PLCs.

Intended to be used solely as a testing tool (not fit for any production environment).

Make sure to check the pictures in the "screenshots" folder on how to setup the folder structure, each folder with its own library file inside:
  - the required for Multi OS
  - the optional expanded to include Android as well
  - or just create a folder for the Operating System you will be using (Single OS)

Get the libplctag libraries and python wrapper files here:

- libplctag library [releases](https://github.com/libplctag/libplctag/releases), recommended v2.1.22 to be able to use MicroLogix PID, otherwise use the latest 
- libplctag's python wrapper [py](https://github.com/libplctag/libplctag/tree/release/src/wrappers/python/plctag) files
- modified [libplctag.py](https://github.com/libplctag/libplctag/issues/228) file

Android libraries, if you might need them, you can get from my [PhoneTest](https://github.com/GitHubDragonFly/PhoneTest) project or build them yourself by cloning the [libplctag4android](https://github.com/libplctag/libplctag4android) project.

# Functionality
- Only a single value will be displayed per tag entered, either of string/char/integer/float...etc.
- The default values can be changed for the app's startup.
- The app provides automated READ and doesn't include WRITE functionality.
- The "Get Tags" button will fetch ControlLogix tags and double-clicking any of the fetched tags will copy it to the clipboard.
- The IP Address, Path and Tag text boxes offer right-click "Paste" functionality.
- The Custom String Length has to be specified when the "custom string" data type is selected.
- Modbus functionality of the libplctag library is not included in this app.

There might be bugs in the app. Not everything could be tested by me, since I don't have access to all the different PLCs supported by the libplctag library.
See the libplctag website for all PLCs supported by the library.

# Usage

All it takes is to:

- Install python on your device (this was tested with v3.9 but might work just fine with older versions).
- Create the required folder structure inside a folder of your choice, copy the corresponding libplctag libraries to their folders, get wrapper files, download plctag_gui.py file and add it to your folder.
- One way to run it would be from the command prompt in Windows, by navigating to your folder and running the file with "python plctag_gui.py" command.

# Licensing
This is MIT licensed.

# Trademarks
Any and all trademarks, either directly on indirectly mentioned here, belong to their respective owners.

# Useful Resources
Other open source projects with similar app:
- The [pylogix](https://github.com/dmroeder/pylogix) repository.
- The [pycomm3](https://github.com/ottowayi/pycomm3) repository.
