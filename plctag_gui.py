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
plc = 'controllogix'
ipAddress = '192.168.1.24'
path = '1,3'
myTag = 'CT_DINT'
timeout = 10000
bitIndex = -1
tagID = -1

ab_plc_type = ['controllogix', 'logixpccc', 'micro800', 'micrologix', 'slc500', 'plc5', 'njnx']
ab_data_type = ['int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64', 'float32', 'float64', 'bool', 'bool array', 'string', 'custom string', 'timer', 'counter', 'control']
ab_mlgx_data_type = ['int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64', 'float32', 'float64', 'string', 'timer', 'counter', 'control', 'pid']
ab_slcplc5_data_type = ['int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64','float32', 'float64', 'string', 'timer', 'counter', 'control']
pid_bits_words = ['None', 'TM', 'AM', 'CM', 'OL', 'RG', 'SC', 'TF', 'DA', 'DB', 'UL', 'LL', 'SP', 'PV', 'DN', 'EN', 'SPS', 'KC', 'Ti', 'TD', 'MAXS', 'MINS', 'ZCD', 'CVH', 'CVL', 'LUT', 'SPV', 'CVP']
bits_8bit = ['None', '0', '1', '2', '3', '4', '5', '6', '7']
bits_16bit = ['None', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']
bits_32bit = ['None', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']
bits_64bit = ['None', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63']
string_length = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47', '48', '49', '50']
bool_display = ['True : False', 'One : Zero', 'On : Off']

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
      startUpdateValue()

def main():
    '''
    Create our window and comm driver
    '''
    global root
    global tagID
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
    global updateRunning
    global btnStart
    global btnStop
    global btnGetTags
    global lbPLC
    global lbDataType
    global lbPID
    global lbBit
    global lbStringLength
    global lbBoolDisplay
    global tbPLC
    global tbDataType
    global tbPID
    global tbBit
    global tbStringLength
    global lbTags
    global tbIPAddress
    global tbPath
    global tbTag
    global popup_menu_tbIPAddress
    global popup_menu_tbPath
    global popup_menu_tbTag

    root = Tk()
    root.config(background='#837DFF')
    root.title('Plctag GUI Test')
    root.geometry('800x600')

    updateRunning = True

    frame1 = Frame(root, background='#837DFF')
    frame1.pack(fill=X)

    # add listboxes for PLCs, DataTypes, PID, Bits, Custom String Length, Bool Display and Tags
    lbPLC = Listbox(frame1, height=11, width=11, bg='lightgreen')
    lbDataType = Listbox(frame1, height=11, width=13, bg='lightblue')
    lbPID = Listbox(frame1, height=11, width=6, bg='lightgreen')
    lbBit = Listbox(frame1, height=11, width=6, bg='lightblue')
    lbStringLength = Listbox(frame1, height=11, width=8, bg='lightgreen')
    lbBoolDisplay = Listbox(frame1, height=11, width=10, bg='lightblue')
    lbTags = Listbox(frame1, height=11, width=40, bg='lightgreen')

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
    scrollbarDataTypes = Scrollbar(frame1, orient='vertical', width=3, command=lbDataType.yview)
    scrollbarDataTypes.pack(anchor=N, side=LEFT, pady=3, ipady=65)
    lbDataType.config(yscrollcommand = scrollbarDataTypes.set)

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
    scrollbarPID = Scrollbar(frame1, orient='vertical', width=3, command=lbPID.yview)
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
    scrollbarBit = Scrollbar(frame1, orient='vertical', width=3, command=lbBit.yview)
    scrollbarBit.pack(anchor=N, side=LEFT, pady=3, ipady=65)
    lbBit.config(yscrollcommand = scrollbarBit.set)

    lbStringLength.insert(1, '~ StrLen')

    i = 2
    for strLength in string_length:
        lbStringLength.insert(i, strLength)
        i = i + 1

    lbStringLength.pack(anchor=N, side=LEFT, padx=3, pady=3)
    lbStringLength['state'] = 'disabled'

    # select string length on the mouse double-click
    lbStringLength.bind('<Double-Button-1>', lambda event: string_length_select())

    # add scrollbar for the string length listbox
    scrollbarStringLength = Scrollbar(frame1, orient='vertical', width=3, command=lbStringLength.yview)
    scrollbarStringLength.pack(anchor=N, side=LEFT, pady=3, ipady=65)
    lbStringLength.config(yscrollcommand = scrollbarStringLength.set)

    lbBoolDisplay.insert(1, '~ Boolean')

    i = 2
    for boolDisplay in bool_display:
        lbBoolDisplay.insert(i, boolDisplay)
        i = i + 1

    lbBoolDisplay.pack(anchor=N, side=LEFT, padx=3, pady=3)

    # select boolean display format on the mouse double-click
    lbBoolDisplay.bind('<Double-Button-1>', lambda event: bool_display_select())

    # add scrollbar for the Tags list box
    scrollbarTags = Scrollbar(frame1, orient='vertical', width=3, command=lbTags.yview)
    scrollbarTags.pack(anchor=N, side=RIGHT, padx=3, pady=3, ipady=65)
    lbTags.config(yscrollcommand = scrollbarTags.set)

    # copy selected tag to the clipboard on the mouse double-click
    lbTags.bind('<Double-Button-1>', lambda event: tag_copy())

    lbTags.pack(anchor=N, side=RIGHT, pady=3)

    frame2 = Frame(root, background='#837DFF')
    frame2.pack(fill=X)

    # add text boxes to serve as labels showing currently selected PLC, DataType, PID, Bit, StringLength and BoolDisplay
    selectedPLC = StringVar()
    tbPLC = Entry(frame2, justify=CENTER, textvariable=selectedPLC, width=11, fg='blue', state='readonly')
    selectedPLC.set('controllogix')
    tbPLC.pack(side=LEFT, padx=2, pady=1)
    selectedDataType = StringVar()
    tbDataType = Entry(frame2, justify=CENTER, textvariable=selectedDataType, width=13, fg='blue', state='readonly')
    selectedDataType.set('int8')
    tbDataType.pack(side=LEFT, padx=2, pady=1)
    selectedPID = StringVar()
    tbPID = Entry(frame2, justify=CENTER, textvariable=selectedPID, width=6, fg='blue', state='readonly')
    selectedPID.set('None')
    tbPID.pack(side=LEFT, padx=5, pady=1)
    selectedBit = StringVar()
    tbBit = Entry(frame2, justify=CENTER, textvariable=selectedBit, width=6, fg='blue', state='readonly')
    selectedBit.set('None')
    tbBit.pack(side=LEFT, padx=4, pady=1)
    selectedStringLength = StringVar()
    tbStringLength = Entry(frame2, justify=CENTER, textvariable=selectedStringLength, width=8, fg='blue', state='readonly')
    selectedStringLength.set('1')
    tbStringLength.pack(side=LEFT, padx=5, pady=1)
    selectedBoolDisplay = StringVar()
    tbBoolDisplay = Entry(frame2, justify=CENTER, textvariable=selectedBoolDisplay, width=10, fg='blue', state='readonly')
    selectedBoolDisplay.set('True : False')
    tbBoolDisplay.pack(side=LEFT, padx=5, pady=1)

    # add Get Tags button
    btnGetTags = Button(frame2, text = 'Get Tags', fg ='brown', height=1, width=7, relief=RAISED, command=start_get_tags)
    btnGetTags.pack(side=RIGHT, padx=3, pady=1)

    frame3 = Frame(root, background='#837DFF')
    frame3.pack(fill=X)

    # create a label and a text box for the Tag entry
    lblTag = Label(frame3, text='Tag to Read', fg='black', bg='#837DFF', font='Helvetica 8 italic')
    lblTag.pack(anchor=CENTER, side=TOP, pady=5)
    selectedTag = StringVar()
    tbTag = Entry(frame3, justify=CENTER, textvariable=selectedTag, font='Helvetica 10 bold', width=90, relief=RAISED)
    selectedTag.set(myTag)

    # add the 'Paste' menu on the mouse right-click
    popup_menu_tbTag = Menu(tbTag, tearoff=0)
    popup_menu_tbTag.add_command(label='Paste', command=tag_paste)
    tbTag.bind('<Button-3>', lambda event: tag_menu(event, tbTag))

    tbTag.pack(anchor=CENTER, side=TOP)

    # create a label to display the received tag value
    tagValue = Label(frame3, text='~', fg='yellow', bg='navy', font='Helvetica 24', width=33, relief=SUNKEN)
    tagValue.pack(anchor=CENTER, side=TOP, pady=4)

    frame4 = Frame(root, height=30, background='#837DFF')
    frame4.pack(fill=X)

    # add a button to start updating tag value
    btnStart = Button(frame4, text = 'Start Update', state='normal', fg ='blue', height=1, width=9, relief=RAISED, command=start_update)
    btnStart.place(anchor=CENTER, relx=0.37, rely=0.55)

    # add a button to stop updating tag value
    btnStop = Button(frame4, text = 'Stop Update', state='disabled', fg ='blue', height=1, width=9, relief=RAISED, command=stopUpdateValue)
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

    # add Exit button
    btnExit = Button(root, text = 'E x i t', fg ='red', height=1, width=7, relief=RAISED, command=root.destroy)
    btnExit.place(anchor=CENTER, relx=0.5, rely=0.97)

    start_connection()

    root.mainloop()

    if not tagID is None:
        if tagID > 0:
            plcTagDestroy(tagID)

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
    plc = selectedPLC.get()
    pth = (selectedPath.get()).replace(' ', '')
    if plc == 'controllogix':
        controllerTags = []
        j = 1

        lbTags.delete(0, 'end')

        stringTag = 'protocol=ab_eip&gateway=' + ipAddress + '&path=' + pth + '&cpu=' + plc + '&name=@tags'

        if int(pythonVersion[0]) >= 3:
            tagID = plcTagCreate(stringTag.encode('utf-8'), timeout)
        else:
            tagID = plcTagCreate(stringTag, timeout)

        while plcTagStatus(tagID) == 1:
            time.sleep(0.01)

        if plcTagStatus(tagID) < 0:
            plcTagDestroy(tagID)
            lbTags.insert(1, 'Failed to fetch Controller Tags')
        else:
            tagSize = plcTagGetSize(tagID)
            offset = 0

            while offset < tagSize:
                # tagId, tagLength and IsStructure variables can be calculated if needed.
                # They can also be diplayed by following the comments further below.

                # tagId = plcTagGetUInt32(tagID, offset)

                tagType = plcTagGetUInt16(tagID, offset + 4)

                # tagLength = plcTagGetUInt16(tagID, offset + 6);

                systemBit = get_bit(tagType, 12) # bit 12

                if systemBit is False:
                    # IsStructure = get_bit(tagType, 15) # bit 15

                    x = int(plcTagGetUInt32(tagID, offset + 8))
                    y = int(plcTagGetUInt32(tagID, offset + 12))
                    z = int(plcTagGetUInt32(tagID, offset + 16))

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

                    tagNameLength = plcTagGetUInt16(tagID, offset)
                    tagNameBytes = bytearray(tagNameLength)

                    offset += 2

                    i = 0
                    while i < tagNameLength:
                        tagNameBytes[i] = plcTagGetUInt8(tagID, offset + i);
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
                    offset += 20;
                    tagNameLength = plcTagGetUInt16(tagID, offset);
                    offset += (2 + tagNameLength)

            for t in controllerTags:
                lbTags.insert(j, t)
                j += 1

            plcTagDestroy(tagID)

        programTags = []

        stringTag = 'protocol=ab_eip&gateway=' + ipAddress + '&path=' + path + '&cpu=' + plc + '&name=Program:MainProgram.@tags'

        if int(pythonVersion[0]) >= 3:
            tagID = plcTagCreate(stringTag.encode('utf-8'), timeout)
        else:
            tagID = plcTagCreate(stringTag, timeout)

        while plcTagStatus(tagID) == 1:
            time.sleep(0.01)

        if plcTagStatus(tagID) < 0:
            plcTagDestroy(tagID)
            lbTags.insert(2, 'Failed to fetch MainProgram Tags')
        else:
            tagSize = plcTagGetSize(tagID)
            offset = 0

            while offset < tagSize:
                # tagId, tagLength and IsStructure variables can be calculated if needed.
                # They can also be diplayed by following the comments further below.

                # tagId = plcTagGetUInt32(tagID, offset)

                tagType = plcTagGetUInt16(tagID, offset + 4)

                # tagLength = plcTagGetUInt16(tagID, offset + 6);

                systemBit = get_bit(tagType, 12) # bit 12

                if systemBit is False:
                    # IsStructure = get_bit(tagType, 15) # bit 15

                    x = int(plcTagGetUInt32(tagID, offset + 8))
                    y = int(plcTagGetUInt32(tagID, offset + 12))
                    z = int(plcTagGetUInt32(tagID, offset + 16))

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

                    tagNameLength = plcTagGetUInt16(tagID, offset)
                    tagNameBytes = bytearray(tagNameLength)

                    offset += 2

                    i = 0
                    while i < tagNameLength:
                        tagNameBytes[i] = plcTagGetUInt8(tagID, offset + i);
                        i += 1

                    tagName = tagNameBytes.decode('utf-8')

                    # display tag name and its dimensions only
                    programTags.append('Program:MainProgram.' + tagName + dimensions)

                    # display tag name, dimensions, tagType, IsStructure, tagLength and tagId (comment and uncomment appropriate lines above and below)
                    # programTags.append('Program:MainProgram.' + tagName + dimensions + '; Type=' + str(tagType) + '; IsStructure=' + IsStructure + '; Length=' + str(tagLength) + 'bytes; Id=' + str(tagId))

                    offset += tagNameLength
                else:
                    offset += 20;
                    tagNameLength = plcTagGetUInt16(tagID, offset);
                    offset += (2 + tagNameLength)

            for t in programTags:
                lbTags.insert(j, t)
                j += 1

            plcTagDestroy(tagID)
    else:
        lbTags.insert(1, 'No Tags Retrieved (incorrect PLC type selected)')

def comm_check():
    global plc
    global path
    global ipAddress
    global myTag
    global tagID
    global bitIndex

    cpu = selectedPLC.get()
    ip = selectedIPAddress.get()
    pth = selectedPath.get()
    tag = selectedTag.get()

    if tag != '':
        if (tagID < 0 or plc != cpu or ipAddress != ip or path != pth or myTag != tag):
            plc = cpu
            ipAddress = ip
            path = pth.replace(' ', '')
            myTag = tag

            if not tagID is None:
                if tagID > 0:
                    plcTagDestroy(tagID)

            dt = selectedDataType.get()
            elem_count = 1

            if dt == 'bool':
                elem_size = 1
            elif dt == 'int8' or dt == 'uint8':
                elem_size = 1
            elif dt == 'int16' or dt == 'uint16':
                elem_size = 2
            elif dt == 'int32' or dt == 'uint32' or dt == 'float32' or dt == 'bool array':
                elem_size = 4

                if dt == 'bool array':
                    if (('[' in myTag) and (not ',' in myTag) and (']' in myTag)):
                        bitIndex = int(myTag[(myTag.index('[') + 1):(myTag.index(']'))])
                        elem_count = math.ceil(bitIndex / (elem_size * 8))
                        myTag = myTag[0:(myTag.index('[') + 1)] + '0' + ']' # Workaround
            elif dt == 'int64' or dt == 'uint64' or dt == 'float64':
                elem_size = 8
            elif dt == 'custom string':
                elem_size = int(math.ceil(int(selectedStringLength.get()) / 8)) * 8
            elif dt == 'string':
                if plc == 'micro800':
                    elem_size = 256
                elif plc == 'controllogix':
                    elem_size = 88
                else:
                    elem_size = 84
            else:
                    elem_size = 1

            # example addressing:
            # 'protocol=ab_eip&gateway=192.168.1.10&cpu=mlgx&elem_size=4&elem_count=1&name=F8:0&debug=1'
            # 'protocol=ab-eip&gateway=192.168.1.24&path=1,3&cpu=lgx&name=@tags'
            # 'protocol=ab-eip&gateway=192.168.0.100&path=1,3&cpu=lgx&name=Program:MainProgram.@tags'

            stringTag = 'protocol=ab_eip&gateway=' + ipAddress + '&path=' + path + '&cpu=' + plc + '&elem_size=' + str(elem_size) + '&elem_count=' + str(elem_count) + '&name=' + myTag

            if int(pythonVersion[0]) >= 3:
                tagID = plcTagCreate(stringTag.encode('utf-8'), timeout)
            else:
                tagID = plcTagCreate(stringTag, timeout)
    else:
        tagValue['text'] = '~'

def startUpdateValue():
    global tagID
    global updateRunning

    '''
    Call ourself to update the screen
    '''

    comm_check()

    if not updateRunning:
        updateRunning = True
    else:
        if tagID > 0:
            if btnStart['state'] != 'disabled':
                btnStart['state'] = 'disabled'
                btnStop['state'] = 'normal'
                btnGetTags['state'] = 'disabled'
                lbPLC['state'] = 'disabled'
                lbDataType['state'] = 'disabled'
                tbIPAddress['state'] = 'disabled'
                tbPath['state'] = 'disabled'
                tbTag['state'] = 'disabled'

            try:
                plcTagRead(tagID, timeout)
                
                dt = selectedDataType.get()

                if dt == 'bool':
                    tagValue['text'] = set_bool_display(plcTagGetBit(tagID, 0))
                elif dt == 'bool array':
                    tagValue['text'] = set_bool_display(plcTagGetBit(tagID, bitIndex))
                elif dt == 'int8':
                    tagValue['text'] = plcTagGetInt8(tagID, 0)
                elif dt == 'uint8':
                    tagValue['text'] = plcTagGetUInt8(tagID, 0)
                elif dt == 'int16':
                    tagValue['text'] = plcTagGetInt16(tagID, 0)
                elif dt == 'uint16':
                    tagValue['text'] = plcTagGetUInt16(tagID, 0)
                elif dt == 'int32':
                    tagValue['text'] = plcTagGetInt32(tagID, 0)
                elif dt == 'uint32':
                    tagValue['text'] = plcTagGetUInt32(tagID, 0)
                elif dt == 'int64':
                    tagValue['text'] = plcTagGetInt64(tagID, 0)
                elif dt == 'uint64':
                    tagValue['text'] = plcTagGetUInt64(tagID, 0)
                elif dt == 'float32':
                    tagValue['text'] = plcTagGetFloat32(tagID, 0)
                elif dt == 'float64':
                    tagValue['text'] = plcTagGetFloat64(tagID, 0)
                elif dt == 'custom string':
                    actualStringLength = plcTagGetInt32(tagID, 0)
                    strValBytes = []

                    i = 0
                    while i < actualStringLength:
                        strValBytes.append(plcTagGetUInt8(tagID, i + 4))
                        i += 1

                    tagValue['text'] = ''.join(map(chr, strValBytes))
                elif dt == 'string':
                    if plc == 'micro800':
                        strLength = plcTagGetUInt8(tagID, 0)
                        strValBytes = []

                        i = 0
                        while i < strLength:
                            strValBytes.append(plcTagGetUInt8(tagID, i + 1))
                            i += 1

                        tagValue['text'] = ''.join(map(chr, strValBytes))
                    elif plc == 'controllogix':
                        strLength = plcTagGetInt32(tagID, 0)
                        strValBytes = []

                        i = 0
                        while i < strLength:
                            strValBytes.append(plcTagGetUInt8(tagID, i + 4))
                            i += 1

                        tagValue['text'] = ''.join(map(chr, strValBytes))
                    else:
                        strLength = plcTagGetUInt16(tagID, 0)
                        strValBytes = []

                        i = 0
                        while i < strLength:
                            strValBytes.append(plcTagGetUInt8(tagID, i + 2))
                            i += 1

                        tagValue['text'] = ''.join(map(chr, strValBytes))
            except Exception as e:
                tagValue['text'] = str(e)
                
            root.after(500, startUpdateValue)

def stopUpdateValue():
    global updateRunning
   
    if updateRunning:
        updateRunning = False
        tagValue['text'] = '~'
        btnStart['state'] = 'normal'
        btnStop['state'] = 'disabled'
        btnGetTags['state'] = 'normal'
        lbPLC['state'] = 'normal'
        lbDataType['state'] = 'normal'
        tbIPAddress['state'] = 'normal'
        tbPath['state'] = 'normal'
        tbTag['state'] = 'normal'

def set_bool_display(boolValue):
    boolFormat = selectedBoolDisplay.get()

    if boolValue == 1:
        if boolFormat == 'True : False':
            return 'True'
        elif boolFormat == 'One : Zero':
            return '1'
        else:
            return 'On'
    elif boolValue == 0:
        if boolFormat == 'True : False':
            return 'False'
        elif boolFormat == 'One : Zero':
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
            selectedIPAddress.set('192.168.1.24')
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
            for dataType in ab_mlgx_data_type:
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

def bit_select():
    if lbBit.get(ANCHOR)[0] != '~':
        selectedBit.set(lbBit.get(ANCHOR))

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

if __name__=='__main__':
    main()
