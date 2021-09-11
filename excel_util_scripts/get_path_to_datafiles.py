import os


def get_path_to_data_file(fileName):    
    curDir = os.path.abspath(os.path.dirname(__file__))
    baseDir = os.path.abspath(os.path.dirname(curDir))
    filePath = os.path.join(baseDir,f"DataOutput/{fileName}")
    return filePath