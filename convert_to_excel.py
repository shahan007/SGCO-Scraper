import pandas as pd
import json


def convert_type(webtype, webtypeIndex, data):
    mainType = data[webtypeIndex][webtype]
    keys = list(map(lambda dic_: list(dic_.keys())[0], mainType))
    values = list(map(lambda dic_: list(dic_.values())[0], mainType))
    dataframes = []
    for i in range(len(keys)):
        each_key = keys[i]
        each_df = pd.Series(values[i]).apply(pd.Series)
        each_df["WebType"] = webtype
        each_df["WebCategory"] = keys[i]
        dataframes.append(each_df)
    mainTypeDf = pd.concat(dataframes)
    return mainTypeDf


def convert_data():
    with open("./DataOutput/data.json", mode="r") as infile:
        data = json.load(infile)
        productDf = convert_type("Products", 0, data)
        serviceDf = convert_type("Services", 1, data)
        mainDf = pd.concat([productDf, serviceDf])
        mainDf.to_excel("./DataOutput/data.xlsx", index=False)


if __name__ == "__main__":
    print("\n\nConverting To excel file ! Please Don't Quit !\n\n")
    convert_data()
    print("\n--- End ---\n")
