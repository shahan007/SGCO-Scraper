# --------- Imports ---------
from get_path_to_datafiles import get_path_to_data_file
import pandas as pd
import os

# --------- Script ---------
def split_to_sheet():
    """    
    Splits data in either data.xlsx or extra_cleaned_data.xlsx file 
    into sheets by WebCategory fields
    """
    fileName = "extra_cleaned_data.xlsx"    
    filePath = get_path_to_data_file(fileName)    
    outFilePath = get_path_to_data_file("data_sheets.xlsx")
    df = pd.read_excel(filePath)
    webCatArray = df["WebCategory"].unique()    
    writer = pd.ExcelWriter(outFilePath,engine="openpyxl")
    for cat in webCatArray:    
        catDf = df[df["WebCategory"] == cat].reset_index(drop=True)
        catDf.to_excel(writer,sheet_name=cat,index=False,engine="openpyxl")    
    writer.save()

if __name__ == "__main__":
    print("Running !")
    split_to_sheet()
    print("\nEnd\n")