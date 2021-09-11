# --------- Imports ---------
from get_path_to_datafiles import get_path_to_data_file
import re
import pandas as pd
import numpy as np

# ---- helper functions -----
def check_intial_addr(s):
    s = s.strip()
    return s[0].isdigit() or s[0] == "#" or s[:3].lower() == "blk" or s[:2].lower() == "no"


def no_digit(s):
    s = s.strip()
    return bool(re.search(r"\d", s))


def check_address_in(array):
    index = None
    for i in range(len(array)):
        x = array[i].lower().strip()
        if (x in ["block", "blk", "#", 'no', 'number', 'building', 'street', 'str', 'bldg', 'plot', "@"]) or (x.isdigit()) or (any(x_.isdigit() for x_ in x)):
            index = i
            break
    if index != None:
        if index == 0:
            return [np.nan, " ".join(array[index:])]
        return [" ".join(array[:index]), " ".join(array[index:])]
    return [" ".join(array), np.nan]



# --------- Script ---------
def main():
    try:        
        fileName = "data.xlsx"
        filePath = get_path_to_data_file(fileName)
        df = pd.read_excel(filePath)
    except:
        print("\n\nOoops File doesn't exists !\n\n")
    else:
        print("\n\nStarting Conversion ! Please Wait !\n\n")
        
        missingAddress = df[df.loc[:,"Address"].isna() & df.loc[:,'Contact'].notna()].loc[:,['Contact',"Address"]]
        sub_missingAddress= missingAddress[missingAddress.loc[:,"Contact"].apply(check_intial_addr)]        
        sub_missingAddress.loc[:,"Address"] = sub_missingAddress.loc[:,"Contact"]
        sub_missingAddress.loc[:,"Contact"] = np.nan
        df.loc[sub_missingAddress.index,["Contact","Address"]] = sub_missingAddress.values
        second_missAddrr = df[df["Address"].isna() & df["Contact"].notna()]
        second_missAddrr = second_missAddrr[second_missAddrr["Contact"].apply(no_digit)]
        second_missAddrr = second_missAddrr['Contact'].str.split().apply(check_address_in).apply(pd.Series).rename(columns={0:"Contact",1:"Address"})
        df.loc[second_missAddrr.index,["Contact","Address"]] = second_missAddrr.values        
        outFilePath = get_path_to_data_file("extra_cleaned_data.xlsx")
        df.to_excel(outFilePath,index=False,engine="openpyxl")
        
        print("\n\nCleaning done: you can find the cleaned excel file ./DataOutput/extra_cleaned_data.xlsx\n\n")

if __name__ == "__main__":
    print("Running ! ")
    main()
    print("\nEnd\n")