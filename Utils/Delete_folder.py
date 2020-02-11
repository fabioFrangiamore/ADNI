import pandas as pd
import os
import shutil


main_folder = os.getcwd()

folders = os.listdir(main_folder)


for folder in folders:
    MRI_types = (os.listdir(main_folder + folder))
    for MRI_type in MRI_types:
        if not any(x in str(MRI_type) for x in ['T2', 'N3', 'Mask']) or any(y in str(MRI_type) for y in ['MPR-R', 'Scaled']):
            shutil.rmtree(main_folder + folder + '/' + MRI_type)

