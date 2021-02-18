# PythonTest
Simple GUI app for [libplctag](https://github.com/libplctag/libplctag) python wrapper. 

Currently functional for getting tags from ControlLogix PLC, reading atomic types and their arrays, bits, strings, timers, counters, controls.

Intended to be used solely as a testing tool (not fit for any production environment).

Make sure to check the pictures in the "screenshots" folder on how to setup the folder structure, each folder with its own library file inside:
- the required folder structure for Multi OS
- the optional expanded folder structure to include Android as well
- or just create a single folder for the Operating System you will be using (Single OS)

Get the libplctag libraries and python wrapper files here:

- libplctag library [releases](https://github.com/libplctag/libplctag/releases)
  - use v2.1.22 to be able to use MicroLogix PID
  - otherwise use the latest, which is v2.3.2+
- libplctag's python wrapper [py](https://github.com/libplctag/libplctag/tree/release/src/wrappers/python/plctag) files
  - modified [libplctag.py](https://github.com/libplctag/libplctag/issues/228) file in case the above is not updated

Android libraries, if you might need them, you can get from my [PhoneTest](https://github.com/GitHubDragonFly/PhoneTest) project or build them yourself by cloning the [libplctag4android](https://github.com/libplctag/libplctag4android) project.

# Functionality
- Generally designed to display a single value per tag entered, either of string/integer/float...etc.
- Bit is requested by using "/" at the end of the tag + bit number.
- Multiple consecutive elements/bits can be displayed for certain data types by adding "{x}" at the end of the tag, where "x" is the number of elements/bits (ex. CT_STRINGArray[0]{5} or CT_DINT/2{15} or N7:0{3}).
- Displaying bit(s) - enter your tag, try selecting the starting bit from the "~ Bit" box (instead of entering it yourself) and optionally add "{x}" at the end.
- For timers, counters and controls there is no list box with subelements, so you will need to type one in, like T4:0.ACC or Timer_1.TT or Counter_1.CD.
- Tag status label turns red/green to indicate failure/success. 
- The default values can be changed for the app's startup, check declarations in the top section of the file.
- The app provides automated READ and doesn't include WRITE functionality.
- The "Get Tags" button will fetch ControlLogix tags and double-clicking any of the fetched tags will copy it to the clipboard.
- The IP Address, Path and Tag text boxes offer right-click "Paste" functionality.
- The Custom String Length has to be specified when the "custom string" data type is selected.
- Modbus functionality of the libplctag library is not included in this app.

There might be bugs in the app. Not everything could be tested by me, since I don't have access to all the different PLCs supported by the libplctag library.
See the libplctag website for all PLCs supported by the library.

# Usage

All it takes is to:

- Install python on your device (this was tested with v3.9 and v3.6.8 but might work just fine with older versions).
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
