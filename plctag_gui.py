'''
Create a simple Tkinter window to display discovered devices,
tags and a single variable.
Tkinter doesn't come preinstalled on all
Linux distributions, so you may need to install it.
For Ubuntu: sudo apt-get install python-tk

Tkinter vs tkinter - Reference: https://stackoverflow.com/questions/17843596/difference-between-tkinter-and-tkinter
'''
import threading
import platform
import time
import math
import array

from libplctag import *

try:
    from Tkinter import *
except ImportError:
    from tkinter import *

pythonVersion = platform.python_version()

currentPLC = 'controllogix'
ipAddress = '192.168.1.20'
path = '1,3'
myTag = 'CT_STRINGArray[0]{5}'
timeout = 10000

ab_plc_type = ['controllogix', 'micrologix', 'logixpccc', 'micro800', 'slc500', 'plc5', 'njnx']
ab_data_type = ['int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64', 'float32', 'float64', 'bool', 'bool array', 'string', 'custom string', 'timer', 'counter', 'control']
ab_mlgx_data_type = ['int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64', 'float32', 'float64', 'string', 'timer', 'counter', 'control', 'pid']
ab_slcplc5_data_type = ['int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64','float32', 'float64', 'string', 'timer', 'counter', 'control']
pid_bits_words = ['None', 'TM', 'AM', 'CM', 'OL', 'RG', 'SC', 'TF', 'DA', 'DB', 'UL', 'LL', 'SP', 'PV', 'DN', 'EN', 'SPS', 'KC', 'Ti', 'TD', 'MAXS', 'MINS', 'ZCD', 'CVH', 'CVL', 'LUT', 'SPV', 'CVP']
bits_8bit = ['None', '0', '1', '2', '3', '4', '5', '6', '7']
bits_16bit = ['None', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
bits_32bit = ['None', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
bits_64bit = ['None', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63']
string_length = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50']
bool_display = ['T : F', '1 : 0', 'On : Off']

class connection_thread(threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      comm_check()

class get_tags_thread(threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      getTags()

class update_thread(threading.Thread):
   def __init__(self):
      threading.Thread.__init__(self)
   def run(self):
      start_update_value()

plctagVersion = ''

def main():
    '''
    Create our window and comm driver
    '''
    global root
    global tagID
    global currentTag
    global stringTag
    global tagValue
    global selectedPath
    global selectedIPAddress
    global selectedPLC
    global selectedDataType
    global selectedPID
    global selectedBit
    global selectedStringLength
    global selectedTag
    global selectedBoolDisplay
    global selectedProgramName
    global updateRunning
    global connectionInProgress
    global connected
    global bitIndex
    global pidElement
    global plctagVersion
    global offset
    global lblTagStatus
    global btnStart
    global btnStop
    global btnGetTags
    global lbPLC
    global lbDataType
    global lbPID
    global lbBit
    global lbStringLength
    global lbBoolDisplay
    global lbTags
    global tbPLC
    global tbDataType
    global tbPID
    global tbBit
    global tbStringLength
    global tbIPAddress
    global tbPath
    global tbTag
    global tbProgramName
    global popup_menu_tbIPAddress
    global popup_menu_tbPath
    global popup_menu_tbTag
    global popup_menu_tbProgramName

    root = Tk()
    root.config(background='#837DFF')
    root.title('Plctag GUI Test')
    root.geometry('800x600')

    connected, connectionInProgress, updateRunning = False, False, True
    currentTag, pidElement, plctagVersion = myTag, 'None', ''
    bitIndex, tagID = -1, -1

    frame1 = Frame(root, background='#837DFF')
    frame1.pack(fill=X)

    # add listboxes for PLCs, DataTypes, PID, Bits, Custom String Length, Bool Display and Tags
    lbPLC = Listbox(frame1, height=11, width=12, bg='lightgreen', justify=CENTER)
    lbDataType = Listbox(frame1, height=11, width=13, bg='lightblue', justify=CENTER)
    lbPID = Listbox(frame1, height=11, width=6, bg='lightgreen', justify=CENTER)
    lbBit = Listbox(frame1, height=11, width=6, bg='lightblue', justify=CENTER)
    lbStringLength = Listbox(frame1, height=11, width=5, bg='lightgreen', justify=CENTER)
    lbBoolDisplay = Listbox(frame1, height=11, width=9, bg='lightblue', justify=CENTER)
    lbTags = Listbox(frame1, height=11, width=50, bg='lightgreen')

    lbPLC.insert(1, '~ PLC')

    i = 2
    for plc in ab_plc_type:
        lbPLC.insert(i, plc)
        i = i + 1

    lbPLC.pack(anchor=N, side=LEFT, padx=2, pady=3)

    # select PLC on the mouse double-click
    lbPLC.bind('<Double-Button-1>', lambda event: plc_select())

    lbDataType.insert(1, '~ Data Type')

    i = 2
    for dataType in ab_data_type:
        lbDataType.insert(i, dataType)
        i = i + 1

    lbDataType.pack(anchor=N, side=LEFT, padx=2, pady=3)

    # select Data Type on the mouse double-click
    lbDataType.bind('<Double-Button-1>', lambda event: data_type_select())

    # add scrollbar for the DataTypes list box
    scrollbarDataTypes = Scrollbar(frame1, orient='vertical', width=12, command=lbDataType.yview)
    scrollbarDataTypes.pack(anchor=N, side=LEFT, pady=3, ipady=65)
    lbDataType.config(yscrollcommand = scrollbarDataTypes.set)

    if plc_tag_check_lib_version(2, 2, 0) != 0:
        lbPID.insert(1, '~ PID')

        i = 2
        for pid in pid_bits_words:
            lbPID.insert(i, pid)
            i = i + 1

        lbPID.pack(anchor=N, side=LEFT, padx=3, pady=3)
        lbPID['state'] = 'disabled'

        # select PID on the mouse double-click
        lbPID.bind('<Double-Button-1>', lambda event: pid_select())

        # add scrollbar for the PID list box
        scrollbarPID = Scrollbar(frame1, orient='vertical', width=12, command=lbPID.yview)
        scrollbarPID.pack(anchor=N, side=LEFT, pady=3, ipady=65)
        lbPID.config(yscrollcommand = scrollbarPID.set)

    lbBit.insert(1, '~ Bit')

    i = 2
    for bit in bits_8bit:
        lbBit.insert(i, bit)
        i = i + 1

    lbBit.pack(anchor=N, side=LEFT, padx=3, pady=3)

    # select Bit on the mouse double-click
    lbBit.bind('<Double-Button-1>', lambda event: bit_select())

    # add scrollbar for the Bit list box
    scrollbarBit = Scrollbar(frame1, orient='vertical', width=12, command=lbBit.yview)
    scrollbarBit.pack(anchor=N, side=LEFT, pady=3, ipady=65)
    lbBit.config(yscrollcommand = scrollbarBit.set)

    lbStringLength.insert(1, '~ Str')

    i = 2
    for strLength in string_length:
        lbStringLength.insert(i, strLength)
        i = i + 1

    lbStringLength.pack(anchor=N, side=LEFT, padx=3, pady=3)
    lbStringLength['state'] = 'disabled'

    # select string length on the mouse double-click
    lbStringLength.bind('<Double-Button-1>', lambda event: string_length_select())

    # add scrollbar for the string length listbox
    scrollbarStringLength = Scrollbar(frame1, orient='vertical', width=12, command=lbStringLength.yview)
    scrollbarStringLength.pack(anchor=N, side=LEFT, pady=3, ipady=65)
    lbStringLength.config(yscrollcommand = scrollbarStringLength.set)

    lbBoolDisplay.insert(1, '~ Bool')

    i = 2
    for boolDisplay in bool_display:
        lbBoolDisplay.insert(i, boolDisplay)
        i = i + 1

    lbBoolDisplay.pack(anchor=N, side=LEFT, padx=3, pady=3)

    # select boolean display format on the mouse double-click
    lbBoolDisplay.bind('<Double-Button-1>', lambda event: bool_display_select())

    # add scrollbar for the Tags list box
    scrollbarTags = Scrollbar(frame1, orient='vertical', width=12, command=lbTags.yview)
    scrollbarTags.pack(anchor=N, side=RIGHT, padx=3, pady=3, ipady=65)
    lbTags.config(yscrollcommand = scrollbarTags.set)

    # copy selected tag to the clipboard on the mouse double-click
    lbTags.bind('<Double-Button-1>', lambda event: tag_copy())

    lbTags.pack(anchor=N, side=RIGHT, pady=3)

    frame2 = Frame(root, background='#837DFF')
    frame2.pack(fill=X)

    # add text boxes to serve as labels showing currently selected PLC, DataType, PID, Bit, StringLength and BoolDisplay
    selectedPLC = StringVar()
    tbPLC = Entry(frame2, justify=CENTER, textvariable=selectedPLC, width=12, fg='blue', state='readonly')
    selectedPLC.set(currentPLC)
    tbPLC.pack(side=LEFT, padx=2, pady=1)
    selectedDataType = StringVar()
    tbDataType = Entry(frame2, justify=CENTER, textvariable=selectedDataType, width=13, fg='blue', state='readonly')
    selectedDataType.set('string')
    tbDataType.pack(side=LEFT, padx=2, pady=1)
    offsetBitBox = 9
    offsetStringLengthBox = -7
    offsetBoolBox = 6
    if plc_tag_check_lib_version(2, 2, 0) != 0:
        selectedPID = StringVar()
        tbPID = Entry(frame2, justify=CENTER, textvariable=selectedPID, width=6, fg='blue', state='readonly')
        selectedPID.set('None')
        tbPID.pack(side=LEFT, padx=14, pady=1)
        offsetBitBox = 0
        offsetStringLengthBox = 0
        offsetBoolBox = 0
    selectedBit = StringVar()
    tbBit = Entry(frame2, justify=CENTER, textvariable=selectedBit, width=6, fg='blue', state='readonly')
    selectedBit.set('None')
    tbBit.pack(side=LEFT, padx=5 + offsetBitBox, pady=1)
    selectedStringLength = StringVar()
    tbStringLength = Entry(frame2, justify=CENTER, textvariable=selectedStringLength, width=5, fg='blue', state='readonly')
    selectedStringLength.set('1')
    tbStringLength.pack(side=LEFT, padx=12 + offsetStringLengthBox, pady=1)
    selectedBoolDisplay = StringVar()
    tbBoolDisplay = Entry(frame2, justify=CENTER, textvariable=selectedBoolDisplay, width=9, fg='blue', state='readonly')
    selectedBoolDisplay.set('T : F')
    tbBoolDisplay.pack(side=LEFT, padx=6 + offsetBoolBox, pady=1)

    # add Get Tags button
    btnGetTags = Button(frame2, text = 'Get Tags', fg ='brown', height=1, width=8, relief=RAISED, command=start_get_tags)
    btnGetTags.pack(side=RIGHT, padx=3, pady=1)

    # add an entry box for the Program Name
    selectedProgramName = StringVar()
    tbProgramName = Entry(frame2, justify=CENTER, textvariable=selectedProgramName, font='Helvetica 9', relief=RAISED)
    selectedProgramName.set('MainProgram')

    # add the 'Paste' menu on the mouse right-click
    popup_menu_tbProgramName = Menu(tbProgramName, tearoff=0)
    popup_menu_tbProgramName.add_command(label='Paste', command=program_name_paste)
    tbProgramName.bind('<Button-3>', lambda event: program_name_menu(event, tbProgramName))

    tbProgramName.pack(side=RIGHT, padx=20, pady=1)

    frame3 = Frame(root, background='#837DFF')
    frame3.pack(fill=X)

    # create a label and a text box for the Tag entry
    lblTag = Label(frame3, text='Tag to Read', fg='black', bg='#837DFF', font='Helvetica 8 italic')
    lblTag.pack(anchor=CENTER, side=TOP, pady=5)
    selectedTag = StringVar()
    tbTag = Entry(frame3, justify=CENTER, textvariable=selectedTag, font='Helvetica 11', width=80, relief=RAISED)
    selectedTag.set(myTag)

    # add the 'Paste' menu on the mouse right-click
    popup_menu_tbTag = Menu(tbTag, tearoff=0)
    popup_menu_tbTag.add_command(label='Paste', command=tag_paste)
    tbTag.bind('<Button-3>', lambda event: tag_menu(event, tbTag))

    tbTag.pack(anchor=CENTER, side=TOP)

    # create a label to display the received tag value
    tagValue = Label(frame3, text='~', fg='yellow', bg='navy', font='Helvetica 18', width=52, relief=SUNKEN)
    tagValue.pack(anchor=CENTER, side=TOP, pady=4)

    frame4 = Frame(root, height=30, background='#837DFF')
    frame4.pack(fill=X)

    # add a button to start updating tag value
    btnStart = Button(frame4, text = 'Start Update', state='disabled', fg ='blue', height=1, width=10, relief=RAISED, command=start_update)
    btnStart.place(anchor=CENTER, relx=0.37, rely=0.55)

    # add a button to stop updating tag value
    btnStop = Button(frame4, text = 'Stop Update', state='disabled', fg ='blue', height=1, width=10, relief=RAISED, command=stop_update_value)
    btnStop.place(anchor=CENTER, relx=0.63, rely=0.55)

    frame5 = Frame(root, background='#837DFF')
    frame5.pack(side=BOTTOM, fill=X)

    frame6 = Frame(root, background='#837DFF')
    frame6.pack(side=BOTTOM, fill=X)

    # create a label and an entry box for the IPAddress
    lblIPAddress = Label(frame6, text='IP Address', fg='black', bg='#837DFF', font='Helvetica 9')
    lblIPAddress.pack(side=LEFT, padx=45)
    selectedIPAddress = StringVar()
    tbIPAddress = Entry(frame5, justify=CENTER, textvariable=selectedIPAddress, font='Helvetica 9', relief=RAISED)
    selectedIPAddress.set(ipAddress)

    # add the 'Paste' menu on the mouse right-click
    popup_menu_tbIPAddress = Menu(tbIPAddress, tearoff=0)
    popup_menu_tbIPAddress.add_command(label='Paste', command=ip_paste)
    tbIPAddress.bind('<Button-3>', lambda event: ip_menu(event, tbIPAddress))

    tbIPAddress.pack(side=LEFT, padx=3, pady=3)

    # create a label for tag status
    lblTagStatus = Label(frame5, text=' tag status ', fg='black', bg='red', font='Helvetica 9')
    lblTagStatus.pack(side=LEFT, padx=5)

    # create a label and an entry box for the Path
    lblPath = Label(frame6, text='Path', fg='black', bg='#837DFF', font='Helvetica 9')
    lblPath.pack(side=RIGHT, padx=60)
    selectedPath = StringVar()
    tbPath = Entry(frame5, justify=CENTER, textvariable=selectedPath, font='Helvetica 9', relief=RAISED)
    selectedPath.set(path)

    # add the 'Paste' menu on the mouse right-click
    popup_menu_tbPath = Menu(tbPath, tearoff=0)
    popup_menu_tbPath.add_command(label='Paste', command=path_paste)
    tbPath.bind('<Button-3>', lambda event: path_menu(event, tbPath))

    tbPath.pack(side=RIGHT, padx=3, pady=3)

    if int(pythonVersion[0]) >= 3:
        plctagVersion = str(plc_tag_get_int_attribute(0, ('version_major').encode('utf-8'), 0)) + '.' + str(plc_tag_get_int_attribute(0, ('version_minor').encode('utf-8'), 0)) + '.' + str(plc_tag_get_int_attribute(0, ('version_patch').encode('utf-8'), 0))
    else:
        plctagVersion = str(plc_tag_get_int_attribute(0, 'version_major', 0)) + '.' + str(plc_tag_get_int_attribute(0, 'version_minor', 0)) + '.' + str(plc_tag_get_int_attribute(0, 'version_patch', 0))

    # create a label for the plctag library version
    lblLibraryVersion = Label(frame5, text=' libplctag ' + plctagVersion + ' ', fg='black', bg='#837DFF', font='Helvetica 9')
    lblLibraryVersion.pack(side=RIGHT, padx=5)

    # add Exit button
    btnExit = Button(root, text = 'E x i t', fg ='red', height=1, width=8, relief=RAISED, command=root.destroy)
    btnExit.place(anchor=CENTER, relx=0.5, rely=0.97)

    start_connection()

    root.mainloop()

    if not tagID is None:
        if tagID > 0:
            plc_tag_destroy(tagID)

def start_connection():
    try:
        thread1 = connection_thread()
        thread1.setDaemon(True)
        thread1.start()
    except Exception as e:
        print('unable to start thread1 - connection_thread, ' + str(e))

def start_get_tags():
    try:
        thread2 = get_tags_thread()
        thread2.setDaemon(True)
        thread2.start()
    except Exception as e:
        print('unable to start thread2 - get_tags_thread, ' + str(e))

def start_update():
    try:
        thread3 = update_thread()
        thread3.setDaemon(True)
        thread3.start()
    except Exception as e:
        print('unable to start thread3 - update_thread, ' + str(e))

def get_bit(int, n):
    return ((int >> n & 1) != 0)

def getTags():
    cpu = selectedPLC.get()
    pth = (selectedPath.get()).replace(' ', '')
    if cpu == 'controllogix':
        controllerTags = []
        j = 1

        lbTags.delete(0, 'end')

        stringTag = 'protocol=ab_eip&gateway=' + ipAddress + '&path=' + pth + '&cpu=' + cpu + '&name=@tags'

        if int(pythonVersion[0]) >= 3:
            tagID = plc_tag_create(stringTag.encode('utf-8'), timeout)
        else:
            tagID = plc_tag_create(stringTag, timeout)

        while plc_tag_status(tagID) == 1:
            time.sleep(0.01)

        if plc_tag_status(tagID) < 0:
            plc_tag_destroy(tagID)
            lbTags.insert(j, 'Failed to fetch Controller Tags')
            j += 1
        else:
            tagSize = plc_tag_get_size(tagID)
            offset = 0

            while offset < tagSize:
                # tagId, tagLength and IsStructure variables can be calculated if needed.
                # They can also be diplayed by following the comments further below.

                # tagId = plc_tag_get_uint32(tagID, offset)

                tagType = plc_tag_get_uint16(tagID, offset + 4)

                # tagLength = plc_tag_get_uint16(tagID, offset + 6)

                systemBit = get_bit(tagType, 12) # bit 12

                if systemBit is False:
                    # IsStructure = get_bit(tagType, 15) # bit 15

                    x = int(plc_tag_get_uint32(tagID, offset + 8))
                    y = int(plc_tag_get_uint32(tagID, offset + 12))
                    z = int(plc_tag_get_uint32(tagID, offset + 16))

                    dimensions = ''

                    if (x != 0 and y != 0 and z != 0):
                        dimensions = '[' + str(x) + ', ' + str(y) + ', ' + str(z) + ']'
                    elif (x != 0 and y != 0):
                        dimensions = '[' + str(x) + ', ' + str(y) + ']'
                    elif (x != 0):
                        if (tagType == 8403 or tagType == 211):
                            dimensions = '[' + str(x * 32) + ']'
                        else:
                            dimensions = '[' + str(x) + ']'

                    offset += 20

                    tagNameLength = plc_tag_get_uint16(tagID, offset)
                    tagNameBytes = bytearray(tagNameLength)

                    offset += 2

                    i = 0
                    while i < tagNameLength:
                        tagNameBytes[i] = plc_tag_get_uint8(tagID, offset + i)
                        i += 1

                    tagName = tagNameBytes.decode('utf-8')

                    # skip all module tags by checking for ':'
                    if ':' not in tagName:
                        # display tag name and its dimensions only
                        controllerTags.append(tagName + dimensions)


                        # display tag name, dimensions, tagType, IsStructure, tagLength and tagId (comment and uncomment appropriate lines above and below)
                        # controllerTags.append(tagName + dimensions + '; Type=' + str(tagType) + '; IsStructure=' + IsStructure + '; Length=' + str(tagLength) + 'bytes; Id=' + str(tagId))

                    offset += tagNameLength
                else:
                    offset += 20
                    tagNameLength = plc_tag_get_uint16(tagID, offset)
                    offset += (2 + tagNameLength)

            for t in controllerTags:
                lbTags.insert(j, t)
                j += 1

            plc_tag_destroy(tagID)

        programName = selectedProgramName.get()

        programTags = []

        if programName != '':
            stringTag = 'protocol=ab_eip&gateway=' + ipAddress + '&path=' + path + '&cpu=' + cpu + '&name=Program:' + programName + '.@tags'

            if int(pythonVersion[0]) >= 3:
                tagID = plc_tag_create(stringTag.encode('utf-8'), timeout)
            else:
                tagID = plc_tag_create(stringTag, timeout)

            while plc_tag_status(tagID) == 1:
                time.sleep(0.01)

            if plc_tag_status(tagID) < 0:
                plc_tag_destroy(tagID)
                lbTags.insert(j, 'Failed to fetch ' + programName + ' Tags')
            else:
                tagSize = plc_tag_get_size(tagID)
                offset = 0

                while offset < tagSize:
                    # tagId, tagLength and IsStructure variables can be calculated if needed.
                    # They can also be diplayed by following the comments further below.

                    # tagId = plc_tag_get_uint32(tagID, offset)

                    tagType = plc_tag_get_uint16(tagID, offset + 4)

                    # tagLength = plc_tag_get_uint16(tagID, offset + 6)

                    systemBit = get_bit(tagType, 12) # bit 12

                    if systemBit is False:
                        # IsStructure = get_bit(tagType, 15) # bit 15

                        x = int(plc_tag_get_uint32(tagID, offset + 8))
                        y = int(plc_tag_get_uint32(tagID, offset + 12))
                        z = int(plc_tag_get_uint32(tagID, offset + 16))

                        dimensions = ''

                        if (x != 0 and y != 0 and z != 0):
                            dimensions = '[' + str(x) + ', ' + str(y) + ', ' + str(z) + ']'
                        elif (x != 0 and y != 0):
                            dimensions = '[' + str(x) + ', ' + str(y) + ']'
                        elif (x != 0):
                            if (tagType == 8403):
                                dimensions = '[' + str(x * 32) + ']'
                            else:
                                dimensions = '[' + str(x) + ']'

                        offset += 20

                        tagNameLength = plc_tag_get_uint16(tagID, offset)
                        tagNameBytes = bytearray(tagNameLength)

                        offset += 2

                        i = 0
                        while i < tagNameLength:
                            tagNameBytes[i] = plc_tag_get_uint8(tagID, offset + i)
                            i += 1

                        tagName = tagNameBytes.decode('utf-8')

                        # display tag name and its dimensions only
                        programTags.append('Program:' + programName + '.' + tagName + dimensions)

                        # display tag name, dimensions, tagType, IsStructure, tagLength and tagId (comment and uncomment appropriate lines above and below)
                        # programTags.append('Program:' + programName + '.' + tagName + dimensions + '; Type=' + str(tagType) + '; IsStructure=' + IsStructure + '; Length=' + str(tagLength) + 'bytes; Id=' + str(tagId))

                        offset += tagNameLength
                    else:
                        offset += 20
                        tagNameLength = plc_tag_get_uint16(tagID, offset)
                        offset += (2 + tagNameLength)

                for t in programTags:
                    lbTags.insert(j, t)
                    j += 1

                plc_tag_destroy(tagID)
        else:
            lbTags.insert(j, 'No Program Tags Retrieved (missing program name)')
    else:
        lbTags.insert(1, 'No Tags Retrieved (incorrect PLC type selected)')

def comm_check():
    global currentPLC
    global path
    global ipAddress
    global lblTagStatus
    global currentTag
    global myTag
    global tagID
    global elem_size
    global elem_count
    global bitIndex
    global pidElement
    global connectionInProgress
    global connected

    cpu = selectedPLC.get()
    ip = selectedIPAddress.get()
    pth = selectedPath.get()
    tag = selectedTag.get()
    bitIndex = -1
    pidElement = 'None'
    connectionInProgress = True

    if tag != '':
        if (not connected or tagID < 0 or currentPLC != cpu or ipAddress != ip or path != pth or myTag != tag):
            lblTagStatus['bg'] = 'red'
            btnStart['state'] = 'disabled'

            currentPLC = cpu
            ipAddress = ip
            path = pth.replace(' ', '')
            myTag = tag
            currentTag = myTag
            elem_count = 1
            elem_size = 1

            if not tagID is None:
                if tagID > 0:
                    plc_tag_destroy(tagID)

            if ('{' in myTag) and ('}' in myTag):
                if myTag.index('}') > myTag.index('{') + 1:
                    try:
                        elem_count = int(myTag[myTag.index('{') + 1:myTag.index('}')])
                        myTag = myTag[:myTag.index('{')]
                    except Exception as e:
                        print(e)

            if '/' in myTag:
                try:
                    bitIndex = int(myTag[myTag.index('/') + 1:])
                    myTag = myTag[:myTag.index('/')]
                except Exception as e:
                    print(e)

            dt = selectedDataType.get()

            if dt == 'bool':
                elem_size = 1
            elif dt == 'int8' or dt == 'uint8':
                elem_size = 1
            elif dt == 'int16' or dt == 'uint16':
                elem_size = 2
            elif dt == 'int32' or dt == 'uint32' or dt == 'float32':
                elem_size = 4
            elif dt == 'bool array':
                elem_size = 4

                if (('[' in myTag) and not (',' in myTag) and (']' in myTag)):
                    bitIndex = int(myTag[(myTag.index('[') + 1):(myTag.index(']'))])
                    if bitIndex > 0:
                        elem_count = math.ceil(bitIndex / (elem_size * 8))
                    myTag = myTag[:myTag.index('[')] + '[0]' # Workaround
            elif dt == 'int64' or dt == 'uint64' or dt == 'float64':
                elem_size = 8
            elif dt == 'custom string':
                elem_size = int(math.ceil(int(selectedStringLength.get()) / 8)) * 8
            elif dt == 'string':
                if cpu == 'micro800':
                    elem_size = 256
                elif cpu == 'controllogix':
                    elem_size = 88
                else:
                    elem_size = 84
            elif dt == 'timer' or dt == 'counter' or dt == 'control':
                if cpu == 'controllogix' or cpu == 'micro800':
                    if myTag.endsWith('.PRE') or myTag.endsWith('.ACC') or myTag.endsWith('.LEN') or myTag.endsWith('.POS'):
                        elem_size = 4
                    elif myTag.endsWith('.EN') or myTag.endsWith('.TT') or myTag.endsWith('.DN') or myTag.endsWith('.CU') or myTag.endsWith('.CD') or myTag.endsWith('.OV') or myTag.endsWith('.UN') or myTag.endsWith('.UA') or myTag.endsWith('.EU') or myTag.endsWith('.EM') or myTag.endsWith('.ER') or myTag.endsWith('.UL') or myTag.endsWith('.IN') or myTag.endsWith('.FD'):
                        elem_size = 1
                    else:
                        elem_size = 12
                else:
                    if myTag.endsWith('.PRE') or myTag.endsWith('.ACC') or myTag.endsWith('.LEN') or myTag.endsWith('.POS'):
                        elem_size = 2
                    else:
                        elem_size = 6
            else: # pid
                elem_size = 46

                if '.' in myTag:
                    pidElement = myTag[myTag.index('.') + 1:]
                    myTag = myTag[:myTag.index('.')]

            # example addressing:
            # 'protocol=ab_eip&gateway=192.168.1.10&cpu=mlgx&elem_size=4&elem_count=1&name=F8:0&debug=1'
            # 'protocol=ab-eip&gateway=192.168.1.24&path=1,3&cpu=lgx&name=@tags'
            # 'protocol=ab-eip&gateway=192.168.0.100&path=1,3&cpu=lgx&name=Program:MainProgram.@tags'

            stringTag = 'protocol=ab_eip&gateway=' + ipAddress + '&path=' + path + '&cpu=' + currentPLC + '&elem_size=' + str(elem_size) + '&elem_count=' + str(elem_count) + '&name=' + myTag

            if int(pythonVersion[0]) >= 3:
                tagID = plc_tag_create(stringTag.encode('utf-8'), timeout)
            else:
                tagID = plc_tag_create(stringTag, timeout)

            while plc_tag_status(tagID) == 1:
                time.sleep(0.01)

            if plc_tag_status(tagID) < 0:
                plc_tag_destroy(tagID)
                connected = False
                if btnStop['state'] == 'disabled':
                    btnStart['state'] = 'disabled'

                root.after(5000, start_connection)
            else:
                connected = True
                connectionInProgress = False
                lblTagStatus['bg'] = 'lightgreen'
                if btnStop['state'] == 'disabled':
                    btnStart['state'] = 'normal'
                    updateRunning = True
                else:
                    start_update()
    else:
        tagValue['text'] = '~'
        root.after(5000, start_connection)

def start_update_value():
    global currentPLC
    global path
    global ipAddress
    global myTag
    global tagID
    global currentTag
    global connected
    global updateRunning

    '''
    Call ourself to update the screen
    '''

    cpu = selectedPLC.get()
    ip = selectedIPAddress.get()
    pth = selectedPath.get()
    tag = selectedTag.get()

    if tag != '':
        if not connected or currentTag != tag or currentPLC != cpu or ipAddress != ip or path != pth:
            currentTag = tag
            currentPLC = cpu
            ipAddress = ip
            path = pth

            if not connectionInProgress:
                if btnStart['state'] != 'disabled':
                    btnStart['state'] = 'disabled'
                    btnStop['state'] = 'normal'
                    btnGetTags['state'] = 'disabled'
                    lbPLC['state'] = 'disabled'
                    lbDataType['state'] = 'disabled'
                    lbPID['state'] = 'disabled'
                    lbBit['state'] = 'disabled'
                    tbIPAddress['state'] = 'disabled'
                    tbPath['state'] = 'disabled'
                    tbTag['state'] = 'disabled'

                connected = False
                start_connection()
        else:
            if not updateRunning:
                updateRunning = True
            else:
                if btnStart['state'] != 'disabled':
                    btnStart['state'] = 'disabled'
                    btnStop['state'] = 'normal'
                    btnGetTags['state'] = 'disabled'
                    lbPLC['state'] = 'disabled'
                    lbDataType['state'] = 'disabled'
                    lbPID['state'] = 'disabled'
                    lbBit['state'] = 'disabled'
                    tbIPAddress['state'] = 'disabled'
                    tbPath['state'] = 'disabled'
                    tbTag['state'] = 'disabled'

                if tagID > 0:
                    try:
                        plc_tag_read(tagID, timeout)

                        if plc_tag_status(tagID) == 1 or plc_tag_status(tagID) < 0:
                            plc_tag_destroy(tagID)
                            connected = False
                            tagValue['text'] = 'not connected'
                            start_connection()
                        else:
                            dt = selectedDataType.get()

                            z = 0
                            strValues = ''

                            if dt == 'bool':
                                tagValue['text'] = set_bool_display(plc_tag_get_bit(tagID, 0))
                            elif (dt == 'bool array') or (bitIndex > -1):
                                while z < elem_count:
                                    strValues += set_bool_display(plc_tag_get_bit(tagID, bitIndex + z)) + ', '
                                    z += 1

                                tagValue['text'] = strValues[:-2]
                            elif dt == 'int8':
                                while z < elem_count:
                                    strValues += str(plc_tag_get_int8(tagID, z * elem_size)) + ', '
                                    z += 1

                                tagValue['text'] = strValues[:-2]
                            elif dt == 'uint8':
                                while z < elem_count:
                                    strValues += str(plc_tag_get_uint8(tagID, z * elem_size)) + ', '
                                    z += 1

                                tagValue['text'] = strValues[:-2]
                            elif dt == 'int16':
                                while z < elem_count:
                                    strValues += str(plc_tag_get_int16(tagID, z * elem_size)) + ', '
                                    z += 1

                                tagValue['text'] = strValues[:-2]
                            elif dt == 'uint16':
                                while z < elem_count:
                                    strValues += str(plc_tag_get_uint16(tagID, z * elem_size)) + ', '
                                    z += 1

                                tagValue['text'] = strValues[:-2]
                            elif dt == 'int32':
                                while z < elem_count:
                                    strValues += str(plc_tag_get_int32(tagID, z * elem_size)) + ', '
                                    z += 1

                                tagValue['text'] = strValues[:-2]
                            elif dt == 'uint32':
                                while z < elem_count:
                                    strValues += str(plc_tag_get_uint32(tagID, z * elem_size)) + ', '
                                    z += 1

                                tagValue['text'] = strValues[:-2]
                            elif dt == 'int64':
                                while z < elem_count:
                                    strValues += str(plc_tag_get_int64(tagID, z * elem_size)) + ', '
                                    z += 1

                                tagValue['text'] = strValues[:-2]
                            elif dt == 'uint64':
                                while z < elem_count:
                                    strValues += str(plc_tag_get_uint64(tagID, z * elem_size)) + ', '
                                    z += 1

                                tagValue['text'] = strValues[:-2]
                            elif dt == 'float32':
                                while z < elem_count:
                                    strValues += str(plc_tag_get_float32(tagID, z * elem_size)) + ', '
                                    z += 1

                                tagValue['text'] = strValues[:-2]
                            elif dt == 'float64':
                                while z < elem_count:
                                    strValues += str(plc_tag_get_float64(tagID, z * elem_size)) + ', '
                                    z += 1

                                tagValue['text'] = strValues[:-2]
                            elif dt == 'custom string':
                                actualStringLength = plc_tag_get_int32(tagID, 0)
                                strValBytes = []

                                i = 0
                                while i < actualStringLength:
                                    strValBytes.append(plc_tag_get_uint8(tagID, i + 4))
                                    i += 1

                                tagValue['text'] = ''.join(map(chr, strValBytes))
                            elif dt == 'string':
                                while z < elem_count:
                                    strValBytes = []
                                    i = 0

                                    if cpu == 'micro800':
                                        strLength = plc_tag_get_uint8(tagID, z * elem_size)

                                        while i < strLength:
                                            strValBytes.append(plc_tag_get_uint8(tagID, i + 1 + z * elem_size))
                                            i += 1
                                    elif cpu == 'controllogix':
                                        strLength = plc_tag_get_int32(tagID, z * elem_size)

                                        while i < strLength:
                                            strValBytes.append(plc_tag_get_uint8(tagID, i + 4 + z * elem_size))
                                            i += 1
                                    else:
                                        strLength = plc_tag_get_uint16(tagID, z * elem_size)

                                        result = strLength % 2

                                        if result == 0:
                                            strValBytes = ['\0'] * strLength
                                        else:
                                            strValBytes = ['\0'] * (strLength + 1)

                                        k = 0
                                        while k < len(strValBytes): # Reverse bytes
                                            strValBytes[k + 1] = plc_tag_get_uint8(tagID, k + 2 + z * elem_size)
                                            strValBytes[k] = plc_tag_get_uint8(tagID, k + 3 + z * elem_size)
                                            k += 2

                                    if len(strValBytes) == 0:
                                        strValues += '{}' + ', '
                                    else:
                                        strValues += (''.join(map(chr, strValBytes))) + ', '
                                    z += 1

                                tagValue['text'] = strValues[:-2]
                            elif dt == 'timer' or dt == 'counter' or dt == 'control':
                                pass
                            else: # pid
                                if pidElement != 'None':
                                    if pidElement == 'TM':
                                        tagValue['text'] = set_bool_display(plc_tag_get_bit(tagID, 0))
                                    elif pidElement == 'AM':
                                        tagValue['text'] = set_bool_display(plc_tag_get_bit(tagID, 1))
                                    elif pidElement == 'CM':
                                        tagValue['text'] = set_bool_display(plc_tag_get_bit(tagID, 2))
                                    elif pidElement == 'OL':
                                        tagValue['text'] = set_bool_display(plc_tag_get_bit(tagID, 3))
                                    elif pidElement == 'RG':
                                        tagValue['text'] = set_bool_display(plc_tag_get_bit(tagID, 4))
                                    elif pidElement == 'SC':
                                        tagValue['text'] = set_bool_display(plc_tag_get_bit(tagID, 5))
                                    elif pidElement == 'TF':
                                        tagValue['text'] = set_bool_display(plc_tag_get_bit(tagID, 6))
                                    elif pidElement == 'DA':
                                        tagValue['text'] = set_bool_display(plc_tag_get_bit(tagID, 7))
                                    elif pidElement == 'DB':
                                        tagValue['text'] = set_bool_display(plc_tag_get_bit(tagID, 8))
                                    elif pidElement == 'UL':
                                        tagValue['text'] = set_bool_display(plc_tag_get_bit(tagID, 9))
                                    elif pidElement == 'LL':
                                        tagValue['text'] = set_bool_display(plc_tag_get_bit(tagID, 10))
                                    elif pidElement == 'SP':
                                        tagValue['text'] = set_bool_display(plc_tag_get_bit(tagID, 11))
                                    elif pidElement == 'PV':
                                        tagValue['text'] = set_bool_display(plc_tag_get_bit(tagID, 12))
                                    elif pidElement == 'DN':
                                        tagValue['text'] = set_bool_display(plc_tag_get_bit(tagID, 13))
                                    elif pidElement == 'EN':
                                        tagValue['text'] = set_bool_display(plc_tag_get_bit(tagID, 15))
                                    elif pidElement == 'SPS':
                                        tagValue['text'] = plc_tag_get_int16(tagID, 4)
                                    elif pidElement == 'KC':
                                        tagValue['text'] = plc_tag_get_int16(tagID, 6)
                                    elif pidElement == 'Ti':
                                        tagValue['text'] = plc_tag_get_int16(tagID, 8)
                                    elif pidElement == 'TD':
                                        tagValue['text'] = plc_tag_get_int16(tagID, 10)
                                    elif pidElement == 'MAXS':
                                        tagValue['text'] = plc_tag_get_int16(tagID, 14)
                                    elif pidElement == 'MINS':
                                        tagValue['text'] = plc_tag_get_int16(tagID, 16)
                                    elif pidElement == 'ZCD':
                                        tagValue['text'] = plc_tag_get_int16(tagID, 18)
                                    elif pidElement == 'CVH':
                                        tagValue['text'] = plc_tag_get_int16(tagID, 22)
                                    elif pidElement == 'CVL':
                                        tagValue['text'] = plc_tag_get_int16(tagID, 24)
                                    elif pidElement == 'LUT':
                                        tagValue['text'] = plc_tag_get_int16(tagID, 26)
                                    elif pidElement == 'SPV':
                                        tagValue['text'] = plc_tag_get_int16(tagID, 28)
                                    elif pidElement == 'CVP':
                                        tagValue['text'] = plc_tag_get_int16(tagID, 32)
                                else:
                                    strValues = ''
                                    k = 0
                                    while k < 23:
                                        strValues += str(plc_tag_get_int16(tagID, k * 2)) + ', '
                                        k += 1

                                    if strValues != '':
                                        tagValue['text'] = strValues[:-2]
                    except Exception as e:
                        tagValue['text'] = str(e)
                        connected = False

                    root.after(500, start_update_value)
                else:
                    tagValue['text'] = 'not connected'
                    connected = False
                    start_connection()
    else:
        tagValue['text'] = 'no tag specified'

def stop_update_value():
    global updateRunning

    if updateRunning:
        tagValue['text'] = '~'
        btnStart['state'] = 'normal'
        btnStop['state'] = 'disabled'
        btnGetTags['state'] = 'normal'
        lbPLC['state'] = 'normal'
        lbDataType['state'] = 'normal'
        tbIPAddress['state'] = 'normal'
        tbPath['state'] = 'normal'
        tbTag['state'] = 'normal'

        dt = selectedDataType.get()

        if dt == 'pid':
            lbPID['state'] = 'normal'
        elif dt != 'custom string' and dt != 'string' and dt != 'bool' and dt != 'bool array' and dt != 'timer' and dt != 'counter' and dt != 'control':
            lbBit['state'] = 'normal'

        if not connectionInProgress:
            updateRunning = False

def set_bool_display(boolValue):
    boolFormat = selectedBoolDisplay.get()

    if boolValue == 1:
        if boolFormat == 'T : F':
            return 'True'
        elif boolFormat == '1 : 0':
            return '1'
        else:
            return 'On'
    elif boolValue == 0:
        if boolFormat == 'T : F':
            return 'False'
        elif boolFormat == '1 : 0':
            return '0'
        else:
            return 'Off'
    else:
        return 'Invalid Value'

def tag_copy():
    root.clipboard_clear()
    listboxSelectedTag = (lbTags.get(ANCHOR))
    root.clipboard_append(listboxSelectedTag)

def tag_menu(event, tbTag):
    try:
        old_clip = root.clipboard_get()
    except:
        old_clip = None

    if (not old_clip is None) and (type(old_clip) is str) and tbTag['state'] == 'normal':
        tbTag.select_range(0, 'end')
        popup_menu_tbTag.post(event.x_root, event.y_root)

def tag_paste():
    # user clicked the 'Paste' option so paste the tag from the clipboard
    selectedTag.set(root.clipboard_get())
    tbTag.select_range(0, 'end')
    tbTag.icursor('end')

def plc_select():
    if lbPLC.get(ANCHOR)[0] != '~':
        plc = lbPLC.get(ANCHOR)

        selectedPLC.set(plc)

        lbDataType.delete(1, 'end')

        if plc == 'controllogix' or plc == 'logixpccc' or plc == 'njnx':
            selectedIPAddress.set('192.168.1.20')
            selectedPath.set('1,3')
            tbPath['state'] = 'normal'

            if plc == 'controllogix':
                btnGetTags['state'] = 'normal'
            else:
                btnGetTags['state'] = 'disabled'

            i = 2
            for dataType in ab_data_type:
                lbDataType.insert(i, dataType)
                i = i + 1
        elif plc == 'micrologix':
            selectedIPAddress.set('192.168.1.10')
            selectedPath.set('')
            tbPath['state'] = 'disabled'
            btnGetTags['state'] = 'disabled'

            i = 2
            if plc_tag_check_lib_version(2, 2, 0) != 0:
                for dataType in ab_mlgx_data_type:
                    lbDataType.insert(i, dataType)
                    i = i + 1
            else:
                for dataType in ab_slcplc5_data_type:
                    lbDataType.insert(i, dataType)
                    i = i + 1
        else:
            selectedIPAddress.set('192.168.1.10')
            selectedPath.set('')
            tbPath['state'] = 'disabled'
            btnGetTags['state'] = 'disabled'

            i = 2
            for dataType in ab_slcplc5_data_type:
                lbDataType.insert(i, dataType)
                i = i + 1

        selectedDataType.set('int8')

        lbBit.delete(1, 'end')

        i = 2
        for bit in bits_8bit:
            lbBit.insert(i, bit)
            i = i + 1

def data_type_select():
    if lbDataType.get(ANCHOR)[0] != '~':
        selectedDataType.set(lbDataType.get(ANCHOR))

        dt = selectedDataType.get()

        if dt == 'pid':
            lbPID['state'] = 'normal'
            lbBit['state'] = 'disabled'
            lbStringLength['state'] = 'disabled'
        elif dt == 'string' or dt == 'bool' or dt == 'bool array' or dt == 'timer' or dt == 'counter' or dt == 'control':
            lbPID['state'] = 'disabled'
            lbBit['state'] = 'disabled'
            lbStringLength['state'] = 'disabled'
        elif dt == 'custom string':
            lbPID['state'] = 'disabled'
            lbBit['state'] = 'disabled'
            lbStringLength['state'] = 'normal'
        else:
            lbPID['state'] = 'disabled'
            lbBit['state'] = 'normal'
            lbStringLength['state'] = 'disabled'

        if lbBit['state'] == 'normal':
            lbBit.delete(1, 'end')

            if dt == 'int8' or dt == 'uint8':
                i = 2
                for bit in bits_8bit:
                    lbBit.insert(i, bit)
                    i = i + 1
            elif dt == 'int16' or dt == 'uint16':
                i = 2
                for bit in bits_16bit:
                    lbBit.insert(i, bit)
                    i = i + 1
            elif dt == 'int32' or dt == 'uint32' or dt == 'float32':
                i = 2
                for bit in bits_32bit:
                    lbBit.insert(i, bit)
                    i = i + 1
            elif dt == 'int64' or dt == 'uint64' or dt == 'float64':
                i = 2
                for bit in bits_64bit:
                    lbBit.insert(i, bit)
                    i = i + 1

def pid_select():
    if lbPID.get(ANCHOR)[0] != '~':
        selectedPID.set(lbPID.get(ANCHOR))

        if selectedPID.get() == 'None':
            selectedTag.set((selectedTag.get())[:(selectedTag.get()).find('.')])
        else:
            if not ('.' in selectedTag.get()):
                selectedTag.set(selectedTag.get() + '.' + selectedPID.get())
            else:
                selectedTag.set((selectedTag.get())[:(selectedTag.get()).find('.')] + '.' + selectedPID.get())


def bit_select():
    if lbBit.get(ANCHOR)[0] != '~':
        selectedBit.set(lbBit.get(ANCHOR))

        if selectedBit.get() == 'None':
            selectedTag.set((selectedTag.get())[:(selectedTag.get()).find('/')])
        else:
            if not ('/' in selectedTag.get()):
                selectedTag.set(selectedTag.get() + '/' + selectedBit.get())
            else:
                selectedTag.set((selectedTag.get())[:(selectedTag.get()).find('/')] + '/' + selectedBit.get())

def string_length_select():
    if lbStringLength.get(ANCHOR)[0] != '~':
        selectedStringLength.set(lbStringLength.get(ANCHOR))

def bool_display_select():
    if lbBoolDisplay.get(ANCHOR)[0] != '~':
        selectedBoolDisplay.set(lbBoolDisplay.get(ANCHOR))

def ip_menu(event, tbIPAddress):
    try:
        old_clip = root.clipboard_get()
    except:
        old_clip = None

    if (not old_clip is None) and (type(old_clip) is str) and tbIPAddress['state'] == 'normal':
        tbIPAddress.select_range(0, 'end')
        popup_menu_tbIPAddress.post(event.x_root, event.y_root)

def ip_paste():
    # user clicked the 'Paste' option so paste the IP Address from the clipboard
    selectedIPAddress.set(root.clipboard_get())
    tbIPAddress.select_range(0, 'end')
    tbIPAddress.icursor('end')

def path_menu(event, tbPath):
    try:
        old_clip = root.clipboard_get()
    except:
        old_clip = None

    if (not old_clip is None) and (type(old_clip) is str) and tbPath['state'] == 'normal':
        tbPath.select_range(0, 'end')
        popup_menu_tbPath.post(event.x_root, event.y_root)

def path_paste():
    # user clicked the 'Paste' option so paste the path from the clipboard
    selectedPath.set(root.clipboard_get())
    tbPath.select_range(0, 'end')
    tbPath.icursor('end')

def program_name_menu(event, tbProgramName):
    try:
        old_clip = root.clipboard_get()
    except:
        old_clip = None

    if (not old_clip is None) and (type(old_clip) is str) and tbTag['state'] == 'normal':
        tbProgramName.select_range(0, 'end')
        popup_menu_tbProgramName.post(event.x_root, event.y_root)

def program_name_paste():
    # user clicked the 'Paste' option so paste the name from the clipboard
    selectedProgramName.set(root.clipboard_get())
    tbProgramName.select_range(0, 'end')
    tbProgramName.icursor('end')

if __name__=='__main__':
    main()
