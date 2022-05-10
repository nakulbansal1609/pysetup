import os
import sys
import pandas as pd 
import json
import re
import openpyxl
from yaml import safe_load
from flatten_json import flatten, unflatten_list
from .obfuscation_rules import data_obsfuscation

class Obfuscation:
    def __init__(self):
        pass

    def read_workbook(self, filepath):
        wb = openpyxl.load_workbook(filepath)
        ws = wb.active
        sheet = ws.values
        cols = next(sheet)
        sheet = list(sheet)
        sheetDF = pd.DataFrame(sheet, columns=cols)
        return sheetDF

    """
    This is main driving function for obfusction process
    """
    def obfuscated_process(self, actual_jsondata,entity_name, filepath):
        print('Reading file ')
        actual_list_of_dict = actual_jsondata

        print('Flattening Data... ')
        flattened_list_of_dict = self.generate_flatten_list(actual_list_of_dict)
        obfuscated_flt_list_of_dict = flattened_list_of_dict.copy()
    
        nested_array_cols_dict = self.generate_flt_col_names(flattened_list_of_dict)
    

        sheetDF = self.read_workbook(filepath)
        entitySheetDF = sheetDF[sheetDF['Entity'] == entity_name]
        for index, each_dict in enumerate(flattened_list_of_dict):
            if index % 100 == 0:
                print('Processed :', index)
            for each_key in each_dict.keys():
                nested_nonarray_col = nested_array_cols_dict.get(each_key)
                if nested_nonarray_col is None:
                    current_key = each_key
                else:
                    current_key = nested_nonarray_col
            
                obfuscation_type = \
                    entitySheetDF['Obfuscation applied'][entitySheetDF['Column'] == current_key].unique()
                if len(obfuscation_type) == 0:
                    pass #todo
                actual_value = each_dict[each_key]
                if actual_value is not None:
                    #print(each_key, actual_value, type(actual_value), obfuscation_type[0])
                    obfuscated_value = self.perform_obfuscation(actual_value, obfuscation_type, current_key)
                    if obfuscated_value is None:
                        print("Obfuscation not done..", current_key, actual_value)
                    else:
                        obfuscated_flt_list_of_dict[index][each_key] = \
                            obfuscated_value
                    
        print('Unflattening Data...')
        unflattened_list_of_dict = self.generate_unflatten_list(obfuscated_flt_list_of_dict)
        return unflattened_list_of_dict

    """
    This function converts the list of json/dicts into a list of json/dict
    with the flattened structures
    """
    def generate_flatten_list(self, actual_list_of_dict):
        return [flatten(each_dict, '_') for each_dict in actual_list_of_dict]

    """
    This function identifies those keys in a dictionary which have the keys
    like a pattern '.\d{1}.' . This is needed to know which keys were having 
    the nested array structure before flattening
    """
    def generate_flt_col_names(self, flattened_list_of_dict):
        dataDF = pd.DataFrame(flattened_list_of_dict)
        nested_array_cols_dict = dict()
        col_names = list(dataDF.columns)
        pattern = r'.\d{1}.'
        for each_col in col_names:
            if re.search(pattern, each_col) is not None:
                value = re.sub(pattern, '.', each_col)
                nested_array_cols_dict[each_col] = value
            
        return nested_array_cols_dict


    """
    The function will perform the actual obfuscation on the python
    object/string passsed inside the function
    """
    def perform_obfuscation(self, actual_value, obfuscation_type, current_key):
        if len(obfuscation_type) == 0:
            obfuscated_value = actual_value
        elif isinstance(actual_value, (list, dict)) and len(actual_value) == 0:
            obfuscated_value = actual_value
        else:
            obfuscation_rule = list(obfuscation_type)[0]
            obfuscated_value = data_obsfuscation(actual_value, obfuscation_rule)
            
        return obfuscated_value



    
    """
    This function unflattens the already flattened llist of json/dict into the 
    list of json/dict with their previous nested structuring.
    """
    def generate_unflatten_list(self, flattened_list_of_dict):
        return [unflatten_list(each_dict, '_') for each_dict in flattened_list_of_dict]


    
        



__all__ = [
    "Obfuscation",
]