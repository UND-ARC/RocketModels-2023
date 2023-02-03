"""
    Description: Converts a '.pf2' file to a '.csv'

    Output: Output File will be in 'output' Folder / Directory inside 'pf2_to_csv'

    Dependencies: 
        FileUtils.py - Must be in the same 'Folder' / 'Directory' as this file

    Author: 
        Mason Motschke

    Contributors:
        FileUtil.py - Tom Stokke
"""
import csv
import os
import shutil
from FileUtils import selectOpenFile as SOF

def main ():
    fileName = SOF('Choose a File: ')
    try:
        openFile = open(fileName)
    except:
        pass

    csvFileName = fileName[:-4] + '.csv'

    data = []; i = 0
    for line in openFile:
        if (line[0].isnumeric()):
            line = line.strip().split(', ')
            data.append(line)
            i += 1

    with open(csvFileName, 'w', newline='') as file:
        fieldNames = ['Time', 'Altitude', 'Velocity', 'Temperature (F)', 'Voltage']
        writer = csv.DictWriter(file, fieldnames=fieldNames)

        writer.writeheader()
        for j in range(0, i):
            writer.writerow({'Time':data[j][0], 'Altitude':data[j][1], 'Velocity':data[j][2], 'Temperature (F)':data[j][3], 'Voltage':data[j][4]})

    openFile.close()
    file.close()

    # Moves file to 'output' directory
    os.chdir(os.getcwd() + '\\' + 'pf2_to_csv\\')
    os.system('mkdir output')
    shutil.move(csvFileName, os.getcwd() + '\\output\\')

main();
