"""
This is currently a bunch of functions but should turn into an object 
so it doesn't have to open and close files so often

17 Jan 2018 - Updating to an object so the object can be instantiated once
and used multiple times
"""

import os, sys
import json
#
class seq_seq_defaults():
    """
    Purpose - This object instantiates the naming defaults for the sequence to 
    sequence processing and provide the methods to access the special file names

    Inputs:
    default_dir, the default value is "."
    default_file, the default value is "defaults.json

    """
    def __init__(self, default_dir=".",default_file="defaults.json"):
        """
        Purpose:  Initialize the defaults
        
        Keyword Arguments:
            default_dir {str} -- [The default directory for the default file.] (default: {"."})
            default_file {str} -- [The default json file name.] (default: {"defaults.json"})

        Side Effects:
            json_default_file {str} -- [Defines the full path name for the json default file]
        """

        self.default_dir = default_dir
        self.default_file = default_file
        self.json_default_file = os.path.join(self.default_dir, self.default_file)
        self.default_json = None
        self.__process_defaults__()
    #
    def get_json_default_file(self):
        """
        Purpose:  returns the name of the json default file
        
        Returns:
            self.json_default_file [str] -- [The json default file name.]
        """
        return self.json_default_file
    #
    def get_defaults_json(self):
        """
        Purpose:  Returns the default values in the json default file
        
        Returns:
            default_json [dict] -- [Dictionary of the default values in the json default file.]
        """
        return self.default_json
    #
    def __process_defaults__(self):
        """
        Purpose:  Process the defaults and ensure there are keys in all lower case

        Side Effects:  Updates self.default_json so that thre are keys in all lower case
        """
        if os.path.isfile(self.json_default_file):
            with open(self.json_default_file,'r') as fn:
                self.default_json = json.load(fn)
        else:
            self.default_json = None
        print(self.default_json)
        for key, value in self.default_json.items():
            t_key = key.lower().strip()
            if not key == t_key:
                self.default_json[t_key] = value

    #
    def __get_default_value__(self, in_val=None):
        """
        Purpose:  Internal method to get a default value from the dictionary
        
        Keyword Arguments:
            in_val {str} -- [The key in the default_json dictionary.] (default: {None})
        
        Returns:
            out_val {str or None} -- [The string associated with the key.]
        """
        if not isinstance(in_val,str) :
            return None  
        return self.default_json.get(in_val.lower().strip()) #Simplifications to match the lower case keys
    #
    def get_glove_dir_name(self):
        glove_dir_name = self.__get_default_value__("glove_dir_name")
        return os.path.join(self.default_dir,glove_dir_name)
    #
    def get_vec_len(self):
        return self.__get_default_value__("vec_len")
    #
    def get_work_dir_name(self):
        return self.__get_default_value__("work_dir")
    # 
    def get_glove_sizes(self):
        return self.__get_default_value__("glove_sizes")
    #
    def get_vector_lengths(self):
        return self.__get_default_value__("vector_lengths")
    #
    def get_size(self):
        return self.__get_default_value__("size")
    #
    def __get_glove_vector_name__(self):
        glove_size = self.get_size()
        vec_len = self.get_vec_len()
        if not glove_size in self.get_glove_sizes():
            raise ValueError('glove size must be one of {}'.format(self.get_glove_sizes()))
        if not vec_len in self.get_vector_lengths():
            raise ValueError('glove vector length must be one of {}'.format(self.get_vector_lengths()))
        return str(glove_size) + "B." + str(vec_len) + "d"
    #
    def __get_glove_file_name__(self):
        return "glove." + self.__get_glove_vector_name__() + ".txt"
    #
    def __get_transcript_dirs__(self):
        return self.__get_default_value__("transcript_dirs")

    def get_transcript_dirs(self):
        return [os.path.join(self.default_dir,d) for d in self.__get_transcript_dirs__()]
    #
    def get_glove_file_name(self):
        return os.path.join(self.get_glove_dir_name(),self.__get_glove_file_name__())
    #
    def get_working_glove_file_name(self):
        return os.path.join(self.get_work_glove_dir(),self.__get_glove_file_name__())
    #
    def get_work_glove_dir(self):
        return os.path.join(self.get_work_dir_name(),self.get_glove_dir_name())
    #
    def get_glove_vector_dta(self):
        return os.path.join(self.get_work_glove_dir(), "glove." + self.__get_glove_vector_name__() + ".hd5")

