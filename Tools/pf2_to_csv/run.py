"""
    PF2 to CSV Converter Project

    Project Description: Converts a '.pf2' file to a '.csv'

    Python Version: 3.11.0

    Output: Output '.csv' File will be in the Same 'Folder' / 'Directory' as the Original '.pf2' File

    Dependencies: 
        FileUtils.py - Must be in the same 'Folder' / 'Directory' as this file

    Author: 
        run.py - Mason Motschke

    Project Contributor(s):
        FileUtils.py - Tom Stokke
"""
from csv import DictWriter
from time import sleep
from FileUtils import selectOpenFile as SOF

def buildRow (headers, data):  # Returns a Dictionary Representing the Next Row to Print to the CSV File
    row = {}; i = 0
    for head in headers:
        row[head] = data[i]
        i += 1
    return row

def getCSVFileName (fileName):  # Returns Name of the '.csv' File that will be Created from '.pf2'
    temp = fileName.strip().split('.')
    temp.append('csv')
    temp.pop(-2)
    return '.'.join(temp)

def getFieldNames (fieldNameLine):  # Returns a List of the Column Headers / Field Names of the CSV
    return fieldNameLine[7:-1].strip().split(', ')

def getPF2Data (pf2File):  # Returns tuple consisting of needed '.pf2' data : [Data Rows, # of Lines Read, Field Names]
    data = []; i = 0
    for line in pf2File:
        if (line.startswith('Data:')):
            fieldNameLine = line.strip();
        if (line[0].isnumeric()):
            line = line.strip().split(', ')
            data.append(line)
            i += 1
    pf2File.close()
    return [data, i, getFieldNames(fieldNameLine)]

def main ():
    try:
        try:
            fileName = SOF(msg='Choose a File: ', title='Files', default='*', filetypes='*.pf2')

            test = fileName.strip().split('.')
            if (test[-1] != 'pf2'): raise TypeError

            selectedFile = open(fileName)
        except TypeError:
            print("\n\n\n\n\n -- Error: Invalid File Extension\n\n\n      - Valid Extensions: '.pf2'\n\n\n -- File Conversion Canceled\n\n\n -- Closing Application...\n\n\n\n\n\n")
            sleep(5); return

        print("\n\n\n\n\n -- File Selected: " + str(fileName) + "\n\n"); sleep(3)

        csvFileName = getCSVFileName(fileName)

        print(" -- CSV File Name: " + str(csvFileName) + "\n\n\n -- Converting...\n\n"); sleep(3)

        tuple = getPF2Data(selectedFile)  # Inside of tuple : ['.pf2' Data, Number of Lines Read, Field Names]
                                          #                   [      0                1                2     ] 

        with open(csvFileName, 'w', newline='') as file:
            writer = DictWriter(file, fieldnames=tuple[2])  #  <------------- #2

            writer.writeheader()
            for j in range(0, tuple[1]):  #  <------------------------------- #1
                writer.writerow(buildRow(tuple[2], tuple[0][j]))  #  <------- #0 and #2
        file.close()
        
        print(" -- Success: File Converted to '.csv'\n\n\n -- Closing Application...\n\n")
        sleep(5); return
    except:
        print(" -- Error: An Error has Occured!\n\n\n -- File Conversion Cancelled\n\n\n -- Closing Application...\n\n")
        sleep(5); return

main();
