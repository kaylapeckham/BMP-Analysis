##########################################
# COURSE: ICS4U
# NAME: Kayla Peckham
# FILE: Peckham_Kayla_EX303.py
# DESCRIPTION: Opening MBP file and fixing it's values of RBG to show a message
# HISTORY:
# 03.23.2021: creation
# 03.24.2021: added elif for counting pixels and added algorithm to go through 3 bytes at a time, added enhancements and function to verify user string/int input
# 04.01.2021: Changed header format to more concise calculation, added function calculate_size
#####################################

import tkinter as tk
from tkinter import filedialog as fd

#importing the file choice

######################################################################################
def intconvert(number): #trying to convert to int for depth to be edited
    try:
        number = int(number)
        setting1 = False #setting becomes false to exit the loop since the input is ok
        return number, setting1
    except ValueError:
        setting1 = True
        return number, setting1
#######################################################################################
def calculate_size(list_input):
    #setting up values before hand so python knows they exist
    exp = 0
    size_calc = 0
    byte = 0
    val = 0
    for element in (range(len(list_input))): #need range and len to go through each element of list and calculate seperately
        byte = list_input[element] 
        exp = element * 2 #calculating exponenet value which changes with each element in list
        val = byte * (0x10 ** (exp)) #exponenent and 0x10 so that it's moving over each digit each time to the proper place in order to add in the right order
        size_calc += val #adding it each time to get calculated total
    return (size_calc) 
######################################################
#MAIN CODE

######handling depth input
setting = True

while setting:
    
    depth = input("What should the bit depth be? (Choose on of 1, 4, 8, 16, 24 or 32): ") #prompting for bit depth of image (0x1c location)
    depth, torF = intconvert(depth) #returning the true/false to make sure the number can be an int, as well as the number itself to make sure it's the correct value
    
    if torF== True:
        print ("Please enter a valid input.")
        print ()
    elif (torF == False) and ((depth == 1) or (depth == 4) or (depth == 8) or (depth == 16) or (depth == 24) or depth == 32): #must be one of these numbers to create a valid image
        setting = False #exit loop if conditions are met
        print ("Thank you")
        print ()
    else: #if it's False but not one of those numbers, you will get this error to try again with one of the valid depth numbers
        print ("Try again. Valid input is 1, 4, 8, 16, 24 and 32")
        print ()

#handling colour input
setter = True
while setter:
    print ("Colour options are: blue, black, green, red, yellow, grey, and white")
    colour = input ("Enter a colour: ") #prompting for colour of text
    print ()
    colour = colour.lower() #cleaning data incase it's silly errors like an upper case or space so the program should still run
    colour = colour.strip()
    if (colour == 'black') or (colour == 'blue') or (colour == 'green') or (colour == 'red') or (colour == 'yellow') or (colour == 'grey') or (colour == 'white'): #makes sure it's one of these colours
        print ("Thank you! Loading image.")
        print ()
        setter = False #leave loop
    else:
        print ("Please have a valid input. Choose black, blue, green, red, yellow, grey or white") #try again if not one of colours typed
        print ()

#handling header input
header = input ("Would you like to display the header (Y/N)?: ") #this is to display the header info (up to 0x35) that tells us all the info about the image
header = header.strip() #cleaning input for silly errors again, strip is for spaces
header = header.lower() #lower is for upper case letters to be converted to lowercase

#opening files
filename = fd.askopenfilename() #opens file directory to choose file from user
inFile = open(filename, 'rb') #will open that file in read binary mode for the rest of the code to execute
outFile = open("edited_image.bmp", 'wb') #opens file in write binary to copy with the edited pixels to display the secret code

#setting numbers that will be added to/changed to 0
count = 0
list1 = []

byte = True
while byte: #ends when bytes dont exist in file anymore
    byte = inFile.read(1) #reading one byte at a time hence the 1

    if (0x00 <= count <= 0x1b) or (0x1d <= count <= 0x35): #if in these header ranges, the code should just be copied, excludes 0x1c since the user changes that info
        outFile.write(byte) #copies the range byte by byte
    elif count == 0x1c: #if the code reaches the point in the header that the user was prompted to edit
        depth = bytes([depth]) #must have [] for byte format to follow through since it's one byte, must be in byte format since it's an inage file being analyzed at the byte level
        outFile.write(depth) #copy into image what user had written
    elif count >= 0x36: #if its not the header
        list1.append(byte) #grouping bytes into 3 through a list approach
        
        if len(list1) == 3: #making sure its 3 bytes being read, length of list will equal how bytes are being grouped together
            
            if (ord(list1[0]) & 1 == 0) or (ord(list1[1]) & 1 == 0) or (ord(list1[2]) & 1 == 0): #looking for least significant bit to end in 0\
                #by comparing the final four digits like 0100 to 0001, this is a mask and your output will be 0001, indicating to change the bytes
                if colour == 'green':
                    outFile.write(bytes([0x00])) 
                    outFile.write(bytes([0xff])) #green pixel
                    outFile.write(bytes([0x00])) 
                elif colour == 'red':
                    outFile.write(bytes([0x00])) 
                    outFile.write(bytes([0x00])) 
                    outFile.write(bytes([0xff])) #red pixel
                elif colour == 'blue':
                    outFile.write(bytes([0xff])) #blue pixel
                    outFile.write(bytes([0x00])) 
                    outFile.write(bytes([0x00])) 
                elif colour == 'black':
                    outFile.write(bytes([0x00])) #no strong pixel makes it black
                    outFile.write(bytes([0x00]))
                    outFile.write(bytes([0x00]))
                elif colour == 'white':
                    outFile.write(bytes([0xff])) #every pixel at it's max will make the image white
                    outFile.write(bytes([0xff])) 
                    outFile.write(bytes([0xff]))
                elif colour == 'yellow':
                    outFile.write(bytes([0x00])) 
                    outFile.write(bytes([0xff])) #red and green at it's max makes yellow
                    outFile.write(bytes([0xff]))
                elif colour == 'grey':
                    outFile.write(bytes([0x80]))
                    outFile.write(bytes([0x80])) #128 or 0x80 is midway to the max 0xff
                    outFile.write(bytes([0x80]))
                    
            else:
                outFile.write(list1[0])  #can do up to 3 since we already made the if to check the length
                outFile.write(list1[1]) #copying otherwise if ending in 1
                outFile.write(list1[2])
            list1 = [] #reset the list once it's at 3 in length, so it doesn't exceed
                    
    count += 1 #just to count for ranges and print statement for header!

#closing files
inFile.close()
outFile.close()

#opening new file in read
newFile = open(filename, 'rb')

#set up values before code to be neutral
count1 = 0
size = 0
exp = -2
list1 = []
list2 = []
list3 = []
list4 = []
list5 = []
list6 = []
list7 = []
list8 = []
list9 = []
list10 = []
list11 = []

for byte_count in range(40): #40 is the size of the header so we don't need to read the whole file
    byte = newFile.read(1)
    if 0x0e <= count1 <= 0x11: #going through each part of header to append to list in order to have the values to calculate the real meaning
        list2.append(ord(byte))
    elif 0x12 <= count1 <= 0x15:
        list3.append(ord(byte))
    elif 0x16 <= count1 <= 0x19:
        list4.append(ord(byte))
    elif 0x1a <= count1 <= 0x1b:
        list5.append(ord(byte))
    elif 0x1c <= count1 <= 0x1d:
        list6.append(ord(byte))
    elif 0x1e <= count1 <= 0x21:
        list7.append(ord(byte))
    elif 0x22 <= count1 <= 0x25:
        list1.append(ord(byte))
    elif 0x26 <= count1 <= 0x29:
        list8.append(ord(byte))
    elif 0x2a <= count1 <= 0x2d:
        list9.append(ord(byte))
    elif 0x2e <= count1 <= 0x31:
        list10.append(ord(byte))
    elif 0x32 <= count1 <= 0x35:
        list11.append(ord(byte))
    count1 += 1

#calling function for calculations
header_size = calculate_size(list2)
size = calculate_size(list1)
width = calculate_size(list3)
height = calculate_size(list4)
planes = calculate_size(list5)
bitdepth = calculate_size(list6)
compression = calculate_size(list7)
horiz_res = calculate_size(list8)
ver_res = calculate_size(list9)
palette = calculate_size(list10)
important = calculate_size(list11)

#printing values
if (header == 'y') or (header == 'yes'): #print only if user asks for that info
    print ("Header size: ", header_size)
    print ("Width: ", width)
    print ("Height: ", height)
    print ("Number of colour planes: ", planes)
    print ("Bit depth: ", bitdepth)
    print ("Compression method: ", compression)
    print ("Image size: ", size) #will be off by 54 due to slight differences
    print ("Horizontal resolution: ", horiz_res)
    print ("Vertical resolution: ", ver_res)
    print ("Number of colours in palatte: ", palette) #0 is default to 2n
    print ("Number of important colours used: ", important) #prints 0 because every colour is important

newFile.close() #closing file

print ("Image loaded. Check documents.") #indicates that all loops have ended and that if the user checks on the image file, it should be loaded
