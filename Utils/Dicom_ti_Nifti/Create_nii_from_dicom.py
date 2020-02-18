import os
import subprocess
import time
import pandas as pd

# the program for the conversion dcm --> nii is always in the same path
dcm2niix_ = 'dcm2niix/build/bin/dcm2niix'
CSF_csv = 'ADNI/Prime_analisi/Output/ADNI1.csv'

# Method to retrieve all the folder with dcm files inside to be processed and the subject id
# Takes the main folder with MRI data as argument
def return_folder(dirs_main):

    root_dir_list = []
    subject = []

    for dir in os.listdir(dirs_main):
        for root, dirs, files in os.walk(dirs_main + dir):

            last_dir = root.split('/')[-1]
            # The last folder is the one with "S" at the beggining
            if last_dir[0] == 'S' and not any(s in root.upper() for s in ('REPEAT', 'REPET')):

                subject.append(root.split('/')[-4])
                root_dir_list.append(root)
        
        # return only unique values of subjects
        subject_list = unique(subject)

    return root_dir_list, subject_list




# Method to convert all my dcmfiles in to a unique nii file for every subjects
def convert_dcmtonii(dirs_main, dcm_folder, new_folder, csf_folder):
    root_dir_list, subject_list = return_folder(dirs_main)
    dcm2niix_dir = return_file_path(dcm_folder, dcm2niix_)
    csf_path = return_file_path(csf_folder, CSF_csv)

    csf = pd.read_csv(csf_path)
    csf_new = csf[csf['PTID'].isin(subject_list)]
    

    try:
        os.makedirs(new_folder)
    except:
        print("Folder already created")

    for i, dirs in enumerate(root_dir_list):
        print(dirs)
        print("++++++++++++++++++")
        print("\n"+ str(i) + '/' + str(len(root_dir_list)))
        command = [dcm2niix_dir,'-o', new_folder, dirs]
        SUBJ = dirs.split('/')[-4]
        subject_id = csf_new.index[csf_new['PTID'] == SUBJ].values[0]
        csf_new.loc[subject_id, 'SUBJ'] = dirs.split('/')[-1]
        registration = subprocess.Popen(command, stdout=subprocess.PIPE)
        output, errors = registration.communicate()
        print ([registration.returncode, errors, output])
        time.sleep(3)
    csf_new.to_csv('csf_adni.csv')
'''
##########################
    Some useful methods 
##########################
'''

# method to retrieve the entire path
def return_file_path(folder_path, subfolder_path):

    return '/'.join([folder_path, subfolder_path])


# Simple method to return only unique values from a list
# Takes the list to be processed as argument
def unique(list1):

    unique_list = []

    for x in list1:
        if x not in unique_list:

            unique_list.append(x)

    return unique_list

