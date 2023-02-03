"""
    Description: Converts a '.pf2' file to a '.csv'

    Output: Output '.csv' File will be in the Same 'Folder' / 'Directory' as the Original '.pf2' File

    Dependencies: 
        FileUtils.py - Must be in the same 'Folder' / 'Directory' as this file

    Author: 
        run.py - Mason Motschke

    Contributors:
        FileUtils.py - Tom Stokke
"""
from csv import DictWriter
from time import sleep
from FileUtils import selectOpenFile as SOF

def getFieldNames (fieldNameLine):  # Returns a List of the Column Headers / Field Names of the CSV

    fieldNameLine = fieldNameLine[7:-1].strip().split(', ')
    return fieldNameLine

def buildRow (j, headers, data):  # Returns a Dictionary Representing the Next Row to Print to the CSV File

    row = {}; i = 0
    for head in headers:
        row[head] = data[j][i]
        i += 1
    return row

def main ():
    fileName = SOF('Choose a File: ')
    try:
        openFile = open(fileName)
    except:
        print('\n' * 5)
        print(" -- Error: File Conversion Canceled\n\n -- Closing Application...\n")
        print('\n' * 5)
        sleep(5); exit()

    print("\n" * 5); print(" -- File Selected: " + str(fileName) + "\n\n"); sleep(3)
    csvFileName = fileName[:-4] + '.csv'
    print(" -- CSV File Name: " + str(csvFileName) + "\n\n\n -- Converting...\n\n"); sleep(3)

    data = []; i = 0;
    for line in openFile:
        if (line.startswith('Data:')):
            fieldNameLine = line.strip();
        if (line[0].isnumeric()):
            line = line.strip().split(', ')
            data.append(line)
            i += 1
    openFile.close()

    with open(csvFileName, 'w', newline='') as file:
        fieldNames = getFieldNames(fieldNameLine)
        writer = DictWriter(file, fieldnames=fieldNames)

        writer.writeheader()
        for j in range(0, i):
            writer.writerow(buildRow(j, fieldNames, data))
    file.close()
    
    print(" -- Success: File Converted to '.csv'\n\n\n -- Closing Application...\n\n")
    sleep(5)

main();
