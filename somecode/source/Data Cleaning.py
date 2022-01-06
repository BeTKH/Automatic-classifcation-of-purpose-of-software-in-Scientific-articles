import os
from os import listdir
from os.path import isfile, join

# we are interested only on annotations set of:  (software_usage and purpose annotations)

interest_list = ['Application_Usage', 'Purpose_Analysis', 'Purpose_Modelling', 'Purpose_Stimulation',
                 'Purpose_DataCollection', 'Purpose_DataPreProcss', 'Purpose_Simulation', 'Purpose_Visualization',
                 'Purpose_Programming']

# file path
path = 'SoMeSci/PLoS_methods/'

# ---------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------
# STEP1: GET file names for all .ann PLoS_methods files
# ---------------------------------------------------------------------------------------------------------------------------------------

PLOS_filesList = []

# iterating over all files in the dir
for file_name in os.listdir(path):

    # if the file is .ann
    if file_name.endswith('.ann'):
        PLOS_filesList.append(file_name)
    else:
        continue

PLOS_filesList.sort()

print('.ann PLosMethods file count : ', len(PLOS_filesList), '\n')
print('Firts 5 files: ', PLOS_filesList[:5])


# ---------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------
# STEP2: CREATE A DICTIONARY OF FILE NAMES VS LIST OF ANNOTATIONS
# ---------------------------------------------------------------------------------------------------------------------------------------

# stores ORIGIAL list of annotations in a file (BEFORE MERGING)
fileAn_dict = {}

# store all annotations in the file ( format: list-of-list)
annotation_filelist = []

# loop over each file
for indx, file in enumerate(PLOS_filesList[:]):

    # path to each file
    file_path = path + file

    with open(file_path, "r") as a_file:

        # stores annotation line
        annotation_line = []

        # check if the annotation is what we want (usage, purpose, starts with T )
        for line in a_file:

            # grab the type of annotation
            annotataion = line.split()[1:2][0]

            if (line.startswith('T') & (annotataion in interest_list)):

                if (line.split()[2:4]) not in annotation_line:

                    annotation_line.append(line.split())
                    print(indx, file, line.split())

                else:
                    pass

        fileAn_dict[file] = annotation_line


"""

There are different kinds of annotations in the .ann file. 
-----------------------------------------------------------

TYPES OF ANNOTATIONS

T - text bound annotations
R - relations
E - event
A - attribute
M - modification
N - Normalization 
-----------------------------------------------------------

We are interested in "text bound annotations only" that indicate software_usage and software_purpose.

Therefore get a list of all annotations in the .ann file iff:

        1. annotations are text bound ( start with T) & 
        2. annotations indicate software_usage or software_purpose

the result is then stored in a dictionary 

where,

    key of dict == name of the file 
    Value of dict == list of list of annotation lines in the file
"""



# ---------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------
# STEP3: MERGE ANNOTATIONS
# ---------------------------------------------------------------------------------------------------------------------------------------

'''

each annotation line has a form of:

     [Tx | Annotation | START | STOP | nameOfSoftware]

     example: 'T2', 'Application_Usage', '13536', '13539', 'SAS'

mergeList() merges two lines of annotations if their start is the same

'''
# ---------------------------------------------------------------------------------------------------------------------------------------
# STEP 3.1: DEFINE A FUNCTION THAT WOULD MERGE TWO ANNOTATIONS
# ---------------------------------------------------------------------------------------------------------------------------------------

def mergeList(list_1, list_2):
    # stores merged annotations
    result_list = []

    '''

     list_1[2:3] is START number 
     merge two annotations if their start number is the same

    '''

    for x, y in [(x, y) for x in list_1[2:3] for y in list_2[2:3]]:

        # if the starting positions are the same x=y
        if (x == y):

            # get id of the firt annotation
            result_list.append(list_1[0])

            # merge annotations by :
            result_list.append(list_1[1] + ':' + list_2[1])

            # start number
            result_list.append(list_1[2])

            # end number
            result_list.append(list_1[3])

            # get name of the software
            software_name_splitted = list_1[4:]
            software_name_joined = ' '.join(software_name_splitted)

            result_list.append(software_name_joined)


        else:
            pass
    return result_list

# ---------------------------------------------------------------------------------------------------------------------------------------
# STEP 3.2: MERGE ANNOTATIONS
# ---------------------------------------------------------------------------------------------------------------------------------------

# stores MERGED LIST of annotations in each file
merged_dict = {}

# stores list of list of all annotations
all_annotations_list = []

# for each file in the dict
for key in list(fileAn_dict):

    # stores list of merged annotations
    merged_annotationlist_perfile = []
    # print(key)
    """
    compare all annotations to each other and grab those that share the same "start number"

    """

    lookup_list1 = []
    for ls1 in fileAn_dict.get(key):

        lookup_list2 = []
        for ls2 in fileAn_dict.get(key):

            # compare each annotation with another but not to itself
            if (ls1 != ls2):

                # merge annotations
                r = mergeList(ls1, ls2)

                # if the
                if len(r) != 0:
                    # print(ls1[0],ls2[0], ls1[2:4], ls2[2:4])

                    if (r[2] not in lookup_list1) | (r[3] not in lookup_list1):

                        merged_annotationlist_perfile.append(r)
                        all_annotations_list.append(r)

                        lookup_list2.extend(r[2:4])

                    else:
                        pass
        # save already merged list on the lookup list
        lookup_list1.extend(lookup_list2)
        # break

    merged_dict[key] = merged_annotationlist_perfile



# ---------------------------------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------------------------
# STEP4: WRITE MERGED ANNOTATIONS TO FILES ( CLEANING DATA)
# ---------------------------------------------------------------------------------------------------------------------------------------
for file in list(merged_dict):

    path2 = 'SoMeSci/PLoS_methodsClean/'
    file_path = path2 + file

    print(file_path)

    with open(file_path, "w") as f1:

        for line in merged_dict.get(file):
            txt = '\t'.join(line)

            print('Writing To ->', file, '<-', txt)

            # write merged annotation to the file
            f1.write(txt + '\n')

        print("-------------------------------------------------")