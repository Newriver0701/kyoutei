import glob
import os
import lhafile

B_files = glob.glob('./downloads/racelists/*.lzh')
K_files = glob.glob('./downloads/results/*.lzh')

os.makedirs('./input/boat_B/TXT', exist_ok=True)
os.makedirs('./input/boat_K/TXT', exist_ok=True)

for b_filepath in B_files:
    lha = lhafile.Lhafile(b_filepath)
    for info in lha.infolist():
        extracted_file = lha.read(info.filename)
        output_filename = os.path.join('./input/boat_B/TXT', os.path.basename(info.filename)[:-4] + '.txt')
        with open(output_filename, 'wb') as output_file:
            output_file.write(extracted_file)

for k_filepath in K_files:
    lha = lhafile.Lhafile(k_filepath)
    for info in lha.infolist():
        extracted_file = lha.read(info.filename)
        output_filename = os.path.join('./input/boat_K/TXT', os.path.basename(info.filename)[:-4] + '.txt')
        with open(output_filename, 'wb') as output_file:
            output_file.write(extracted_file)

print('finished!')
