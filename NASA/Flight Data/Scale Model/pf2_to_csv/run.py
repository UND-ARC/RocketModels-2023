"""
    Description: Converts a '.pf2' file to a '.csv'

    Output: Output '.csv' File will be in the Same 'Spot' / 'Folder' at the Original File

    Dependencies: 
        FileUtils.py - Must be in the same 'Folder' / 'Directory' as this file

    Author: 
        run.py - Mason Motschke

    Contributors:
        FileUtils.py - Tom Stokke
"""
import csv
import os
import shutil
from FileUtils import selectOpenFile as SOF

def getFieldNames (fieldNameLine):
    # Returns a List of the Column Headers / Field Names of the CSV

    fieldNameLine = fieldNameLine[7:-1].strip().split(', ')
    return fieldNameLine

def buildRow (j, headers, data):
    # Returns a Dictionary Representing the Next Row to Print to the CSV File

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
        pass

    csvFileName = fileName[:-4] + '.csv'

    data = []; i = 0;
    for line in openFile:
        if (line.startswith('Data:')):
            fieldNameLine = line.strip();
        if (line[0].isnumeric()):
            line = line.strip().split(', ')
            data.append(line)
            i += 1

    with open(csvFileName, 'w', newline='') as file:
        fieldNames = getFieldNames(fieldNameLine)
        writer = csv.DictWriter(file, fieldnames=fieldNames)

        writer.writeheader()
        for j in range(0, i):
            row = buildRow(j, fieldNames, data)
            writer.writerow(row)

    openFile.close()
    file.close()

main();