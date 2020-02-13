import pandas as pd
import os
import shutil
import subprocess
import nibabel as nib

main_folder = '/media/fabio/Disco locale/Scaricati/ADNI1_ex/ADNI'

folders = os.listdir(main_folder)

fixed_image = '/media/fabio/Disco locale/Scaricati/ADNI1_ex/ADNI/002_S_0559/MPR-R__GradWarp__B1_Correction__N3/2006-05-23_15_09_38.0/S14876/ADNI_002_S_0559_MR_MPR-R__GradWarp__B1_Correction__N3_Br_20070216235035331_S14876_I40678.nii'

'''
for folder in folders:
    print(folder)
    print(main_folder)
    MRI_types = (os.listdir(main_folder + '/' +folder))
    
    for MRI_type in MRI_types:

        if not any(x in str(MRI_type) for x in ['T2', 'N3', 'Mask']) or any(y in str(MRI_type) for y in ['MPR-R', 'Scaled']):
            shutil.rmtree(main_folder + '/' + folder + '/' + MRI_type)

        print(main_folder + '/' + folder + '/' + MRI_type)'''

for folder in folders:
    for roots, dirs, files in os.walk(main_folder + '/' + folder):
        print()
        
        if '.nii' in str(files):
            #print(dirs)
            print(roots + '/' + str(files[0]))
            moving_image = roots + '/' + str(files[0])
            print(moving_image)
            if 'txt' not in files[0]:
                my_txt = os.path.join(main_folder + '/' + folder, files[0] +'.txt')
                file = open(my_txt, "w")
                file.write("[GLOBAL] \n\nfixed = " + fixed_image +"\nmoving = " + moving_image + "\nimg_out = " + roots + '/' + 'registrata_' + str(files[0])+
                "\n\n[STAGE] \n\nxform=rigid \noptim=versor \nmax_its=30 \nres=4 4 2")
                file.close()

                command = ['plastimatch', 'register' ,  my_txt]
                registration = subprocess.Popen(command, stdout=subprocess.PIPE)
                output, errors = registration.communicate()
                print ([registration.returncode, errors, output])



