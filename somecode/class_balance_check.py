import os
import argparse
import time
import random
import shutil

from pathlib import Path
from math import ceil

from somenlp.utils import get_time_marker
from somenlp.feature_engineering import calculate_features_parallel


import os
from os import listdir 
from collections import Counter

import os
from os import listdir 
from collections import Counter


in_path = '/home/beck/Desktop/SoMeNLP/data/PLoS_methods_bio/'
out_path = '/home/beck/Desktop/SoMeNLP/data/PLoS_methods/'

def split_data(in_path, out_path, file_ext =".data.txt", 
               ratio =[60, 20, 20], set_names = ['train', 'devel', 'test']):
    
    in_path = in_path.rstrip('/')
    out_path = out_path.rstrip('/')

    if not os.path.isdir(in_path):
        raise(RuntimeError("Input path does not exist"))
        
    if not os.path.isdir(out_path):
        os.mkdir(out_path)
    
    if sum(ratio) != 100:
        raise(RuntimeError("Input ratio {} does not sum to 100".format(ratio)))
    if len(ratio) != len(set_names):
        raise(RuntimeError("Number of ratios and setnames has to match: {} vs {}".format(ratio, set_names)))

    #print("Loading files")
    single_files = list(Path(in_path).rglob('*{}'.format(file_ext)))
    
    all_files = []
    for entry in single_files:
        
        base_file_name = entry.name.split(file_ext)[0]
        
        base_file_entries = list(Path(in_path).rglob('{}*'.format(base_file_name)))
        
        all_files.append(base_file_entries)
    
    random.seed()
    random.shuffle(all_files)

    #print("Copying files")
    cut_sum = 0
    prev_cut_idx = 0
    for cut, name in zip(ratio, set_names):
        cut_sum += cut
        cut_idx = ceil(len(all_files) * cut_sum / 100) 
        
        out_folder_name = in_path.rsplit('/')[-1]
        new_output_location = '{}/{}_{}'.format(out_path.rstrip('/'), out_folder_name, name) 
        
        if not os.path.isdir(new_output_location):
            os.makedirs(new_output_location)
            
        for files in all_files[prev_cut_idx:cut_idx]:
            for f in files:
                source_path = str(f)
                target_path = '{}/{}'.format(new_output_location, f.name)
                shutil.copy(source_path, target_path)
        prev_cut_idx = cut_idx
    
    print("Done")
    

def purposeLabel_counter(path):
    
    import os
    from os import listdir 
    from collections import Counter
    
    
    def list_file_names(path, file_ext='.labels.txt'):
    
        file_names_list = []

        for file_name in os.listdir(path):
            if not file_name.endswith(file_ext): continue
            file_names_list.append(file_name) 

        file_names_list.sort()

        return file_names_list
    
    file_name_list = list_file_names(path)
    
    interest_list = ["Analysis", "Modelling", "Stimulation", "DataCollection", "DataPreProcss", 
                 "Simulation", "Visualization", "Programming"]
    
    all_purpose_labels = []
    
    for file_name in file_name_list[:]:
        file_path = path + file_name
        
        with open(file_path, 'r') as f:
            
            list_lines = f.readlines()
            
            #print(list_of_lebs)
            list_of_tokens = ' '.join(list_lines).split()
            
            for tok in list_of_tokens:
                if tok != 'O' and (len(tok.split('-')[1].split('_')) == 3 ):
                    if tok.split('-')[1].split('_')[2] in interest_list:
                        
                        purpose = tok.split('-')[1].split('_')[2]
                        
                        all_purpose_labels.append(purpose)
    
                        
    return  dict(Counter(all_purpose_labels))

def train_test_dev(whole_path, train_path, test_path, dev_path):
    
    _whole = purposeLabel_counter(whole_path)
    _train = purposeLabel_counter(train_path)
    _test  = purposeLabel_counter(test_path)
    _dev   = purposeLabel_counter(dev_path)
    
    
    
    _whole_sorted = dict(sorted(_whole.items()))
    _train_sorted = dict(sorted(_train.items()))
    _test_sorted  = dict(sorted(_test.items()))
    _dev_sorted   = dict(sorted(_dev.items()))
    
    return _whole_sorted, _train_sorted, _test_sorted, _dev_sorted

def __proportion_calculator_with_key(whole_dict, train_dict, test_dict, dev_dict ):
    
    train_purpose_props = []
    for (k,v), (k2,v2) in zip(whole_dict.items(), train_dict.items()):
        if k2 == k: 
            train_percentage = int(v2 / v * 100)
            train_purpose_props.append((train_percentage, k))
            
    dev_purpose_props = []
    for (k,v), (k2,v2) in zip(whole_dict.items(), dev_dict.items()):
        if k2 == k:
            
            dev_percentage = int(v2 / v * 100)
            dev_purpose_props.append((dev_percentage,k))
            
    test_purpose_props = []       
    for (k,v), (k2,v2) in zip(whole_dict.items(), test_dict.items()):
        if k2 == k:
            
            test_percentage = int(v2 / v * 100)
            test_purpose_props.append((test_percentage, k))
            
    return train_purpose_props, dev_purpose_props, test_purpose_props


def __proportion_calculator(whole_dict, train_dict, test_dict, dev_dict ):
    
    train_purpose_props = []
    for (k,v), (k2,v2) in zip(whole_dict.items(), train_dict.items()):
        if k2 == k: 
            train_percentage = int(v2 / v * 100)
            train_purpose_props.append(train_percentage)
            
    dev_purpose_props = []
    for (k,v), (k2,v2) in zip(whole_dict.items(), dev_dict.items()):
        if k2 == k:
            
            dev_percentage = int(v2 / v * 100)
            dev_purpose_props.append(dev_percentage)
            
    test_purpose_props = []       
    for (k,v), (k2,v2) in zip(whole_dict.items(), test_dict.items()):
        if k2 == k:
            
            test_percentage = int(v2 / v * 100)
            test_purpose_props.append(test_percentage)
            
    return train_purpose_props, dev_purpose_props, test_purpose_props



def _within_range(list_):
    
    bool_list = []
    for val in list_:
        if val in range(55,65):
            bool_list.append(True)
        else:
            bool_list.append(False)
            
    return all(bool_list)   # apply & to all and return


def _within_range_pubmed(list_):
    
    bool_list = []
    for val in list_:
        if val in range(50,70):
            bool_list.append(True)
        else:
            bool_list.append(False)
            
            
    withn_range_bool = all(bool_list) # apply & to all and return
    
    # check if all class labels are included , class label stimulation is missing in the PubMed 
    if (len(bool_list) == 7):
        all_classes_included = True
    else:
        all_classes_included = False
        
    result = all_classes_included and withn_range_bool
            
    return result   


def _within_range_dev_test(list_):
    
    bool_list = []
    for val in list_:
        if val in range(15,25):
            bool_list.append(True)
        else:
            bool_list.append(False)
            
    return all(bool_list)   # apply & to all and return