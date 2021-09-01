# ----------------Imports----------------
# mandatory
import requests as req
import json
import pandas as pd
import os
import re
from lxml import html
# optional
from bs4 import BeautifulSoup

# ----------------Script----------------


def fetch_religious_links(base_url, main_url, headers):
    """
    Fetches Absolute links for all the religious links (might be able to use it for other categories)
    """
    res = req.get(main_url, headers=headers)
    if res.ok:
        tree = html.fromstring(html=res.text)
        # you can runs the expression below, only works under browser inspector tool
        browser_express = "//table[@id='table24']/tbody/tr[7]//table/tbody/tr[not(position()=1 ) and not(position()=last())]//a/font/text()"
        # main expression to scrape all the religious institutes links; we skip the first two tr as they were blanks; returns relative links
        script_expression = "//table[@id='table24']/tr[7]//table/tr[not(position()=1 ) and not(position()=last())]//a/@href"
        relig_inst_links = tree.xpath(script_expression)
        # converts each relative link to absolute so we can follow them
        absol_links = [req.compat.urljoin(base_url, link)
                       for link in relig_inst_links]
        return absol_links
    return None


def scrape_data(link_array, headers):
    """
    Follow the absolute links provided and scrape the data
    """

    for link in link_array:
        res = req.get(link, headers=headers)
        tree = html.fromstring(html=res.text)
        expression = "(//table//table//table)[8]//tr/td[1]/descendant-or-self::text()"
        company_data = tree.xpath(expression)
        company_data_str = " ".join(company_data)

        # ----regx-----
        # compile so can use multiple timesstrip all the blank stuff
        regex_strip_expression = r'[\n\r\t\xa0]'
        regex_strip_rtn = re.compile(regex_strip_expression)
        # ----date cleaning-----
        cleaned_data = regex_strip_rtn.sub('', company_data_str).strip()
        data_needed = ['Contact', 'Address', "Tel", "Fax",
                       "e-mail", "Website", "Categories", "Company Profile"]
        data_needed_index = []
        final_data = {}
        for need in data_needed:
            data_needed_index.append(cleaned_data.index(need))
        for i in range(len(data_needed_index)-1):
            start_index = data_needed_index[i]
            stop_index = data_needed_index[i+1]
            final_data[data_needed[i]] = "".join(
                cleaned_data[start_index:stop_index].split(':')[1:]).strip() or None
        final_data[data_needed[-1]] = cleaned_data[data_needed_index[-1]:].split(':')[1].strip() or None
        final_data['Company'] = cleaned_data[:data_needed_index[0]
                                             ].strip() or None
        try:
            final_data['e-mail'] = final_data['e-mail'].split()
        except:
            pass
        try:
            categories = final_data['Categories'].split(',')
            categories = list(map(lambda cat: cat.strip(), categories))
            if categories == [""]:
                categories = None
            final_data['Categories'] = categories
        except:
            pass
        try:
            website_slash_index = final_data['Website'].index("//www")
            final_data['Website'] = final_data['Website'][:website_slash_index] + \
                ":" + final_data['Website'][website_slash_index:]
        except:
            pass
        yield final_data


def main():
    """
    Main Function
    """

    print("Starting Scraping: Please wait ! Don't quit !\n\n")

    # setting constant variables
    base_url = "http://singapore-companies-directory.com"
    # link to religion institutes to scrape
    main_url = "http://singapore-companies-directory.com/Categories/singapore_religious_institutions.htm"
    # request header
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36"
    }

    main_data = {"Religious_Institutes": []}
    relig_insts_links = fetch_religious_links(base_url, main_url, headers)
    if not relig_insts_links:
        return "\n\nOoops! Unable to fetch & scrape the data\n\n"
    for inst_data in scrape_data(relig_insts_links, headers):
        main_data["Religious_Institutes"].append(inst_data)
    baseDir = os.path.abspath(os.path.dirname(__file__))
    filename = 'DataOutput/religious_contacts.json'
    filePath = os.path.join(baseDir, filename)
    with open(filePath, mode='w') as outfile:
        json.dump(main_data, outfile, indent=4)
    print(
        f"Scraping Done! Checkout the data in the following file:{filename}\n\n")


# ----------------Utility functions----------------
def read_data(filename='./DataOutput/religious_contacts.json'):
    baseDir = os.path.abspath(os.path.dirname(__file__))
    filePath = os.path.join(baseDir, filename)
    with open(filePath, mode='r') as outfile:
        return json.load(outfile)


def json_to_excel():
    """
    Converts the json file to excel format
    """
    religious_series = pd.read_json(
        './DataOutput/religious_contacts.json')['Religious_Institutes']
    religious_df = religious_series.apply(pd.Series)
    religious_df.to_excel('./DataOutput/religious_contacts.xlsx', index=False)


if __name__ == "__main__":
    print('\n\nRunning Religious Institue Script\n\n')
    main()
    json_to_excel()
