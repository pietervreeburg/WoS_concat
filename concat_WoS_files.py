# script to concatenate separate WoS-files in one big file

# possible problems with the import files are:
# files with UTF-8 BOM: script checks each file for BOM and notifies if a BOM is found. No automatic fix added for extra security 
# files with <cr> newlines (old style mac): files are opened with universal newline support to recognize all possible newlines. note: universal newline support is standard in Python 3+

import sys
import os
import glob
import codecs

source_folder = raw_input('Source folder: ')
source_path = os.path.join(r'\\campus.eur.nl\shared\departments\ESE-FD-BB-ONDERZOEK\Pieter_Vreeburg\1_Project_support\Metis_WoS_checker', source_folder, '*.txt')
script_path = os.path.dirname(sys.argv[0])

# generate a list of filenames
filenames = glob.glob(source_path)
if len(filenames) == 0:
    print 'Source folder is empty or not found, exiting.'
    quit()

# check for BOM in files, notify user if a BOM is found
for filename in filenames:
    content = open(filename, 'rb').read()
    if content.startswith(codecs.BOM_UTF8):
        print 'BOM detected in file', filename, ', exiting'
        quit()

# concatenate files and skip header lines
line_nr = 0
output_file = os.path.join(script_path,'WoS_concat_' + source_folder + '.txt')
try: # remove earlier output file (if it exists)
    os.remove(output_file)
except OSError:
    pass
for filename in filenames:
    content = open(filename, 'rU').read().splitlines()
    with open(output_file, 'a') as f_out:
        for line in content:
            if line.startswith('PT\t'):
                continue
            f_out.write(line + '\n')
            line_nr += 1

print 'total lines:', line_nr
print 'Done'