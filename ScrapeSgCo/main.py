# ------------------ Imports ------------------
# mandatory
import requests as req
import json
import pandas as pd
import os
import re
from lxml import html
from .generate_header import RotateHeader
from .utility_helper_methods import (
    zipper, convert_to_absolute_links, generate_prod_serv_names)
# optional
from bs4 import BeautifulSoup

# ------------------ Main Scraper Script ------------------


def fetch_prod_serv_links(rotate_header):
    """
    Fetches the name and absolute links of all the available categories of Singapore Listed Companies
    """

    base_url = "http://singapore-companies-directory.com"
    main_url = "http://singapore-companies-directory.com/sitemap.htm"
    headers = rotate_header.fetch_header()
    res = req.get(main_url, headers=headers)
    tree = html.fromstring(html=res.text)
    expression = "//*[@id='table16']/tr[not(position()=3)]"
    browser = "//*[@id='table16']//tr[not(position()=3)]"
    products, services = tree.xpath(expression)
    products_categories_links = convert_to_absolute_links(
        products.xpath(".//p//a/@href"), base_url)
    services_categories_links = convert_to_absolute_links(
        services.xpath("./td[2]//a/@href"), base_url)
    products_categories_names = generate_prod_serv_names(
        products, ".//p//a/font/text()")
    services_categories_names = generate_prod_serv_names(
        services, "./td[2]//a//font/text()")
    productLinkName = zipper(products_categories_links,
                             products_categories_names)
    serviceLinkName = zipper(services_categories_links,
                             services_categories_names)
    return productLinkName, serviceLinkName


def fetch_category_inst_links(base_url, main_url, rotate_header):
    """
    Fetches Absolute links for each category link
    """
    res = req.get(main_url, headers=rotate_header.fetch_header())
    if res.ok:
        tree = html.fromstring(html=res.text)
        # you can runs the expression below, only works under browser inspector tool
        browser_express = "//table[@id='table24']/tbody/tr[7]//table/tbody/tr[not(position()=1 ) and not(position()=last())]//a/font/text()"
        # main expression to scrape all the  institutes links; we skip the first two tr as they were blanks; returns relative links
        script_expression = "//table[@id='table24']/tr[7]//table/tr[not(position()=1 ) and not(position()=last())]//a/@href"
        inst_links = tree.xpath(script_expression)
        # converts each relative link to absolute so we can follow them
        absol_links = convert_to_absolute_links(inst_links, base_url)
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
        unavail = []
        data_needed_index = []
        final_data = {}
        for need in data_needed:
            try:
                data_needed_index.append(
                    cleaned_data.lower().index(need.lower()))
            except:
                unavail.append(need)
        for unavaildata in unavail:
            data_needed.remove(unavaildata)
        for i in range(len(data_needed_index)-1):
            start_index = data_needed_index[i]
            stop_index = data_needed_index[i+1]
            final_data[data_needed[i]] = "".join(
                cleaned_data[start_index:stop_index].split(':')[1:]).strip() or None
        try:
            final_data[data_needed[-1]] = cleaned_data[data_needed_index[-1]                                                       :].split(':')[1].strip() or None
            final_data['Company'] = cleaned_data[:data_needed_index[0]
                                                 ].strip() or None
        except:
            pass
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


def scrape_type(array_type, array, base_url, main_data, rotate_header):

    if array_type == "Products":
        index = 0
    else:
        index = 1

    print(f"\n\nScraping Type: {array_type}\n\n")
    for array_name, array_link in array:
        print(f"\n\n\tScraping Cat: {array_name}\n\n")
        institute_links = fetch_category_inst_links(
            base_url, array_link, rotate_header)
        if not institute_links:
            continue
        local_data = {array_name: []}
        for inst_data in scrape_data(institute_links, rotate_header.fetch_header()):
            local_data[array_name].append(inst_data)
        main_data[index][array_type].append(local_data)
    print(f"\n\nScraping Type: {array_type} Done !\n\n")


def main():
    """
    Main Function
    """

    print("Starting Scraping: Please wait ! Don't quit !\n\n")

    # setting constant variables
    base_url = "http://singapore-companies-directory.com"
    rotate_header = RotateHeader()
    main_data = [
        {
            "Products": []
        },
        {
            "Services": []
        }
    ]

    productLinkName, serviceLinkName = fetch_prod_serv_links(rotate_header)
    scrape_type("Products", productLinkName,
                base_url, main_data, rotate_header)
    scrape_type("Services", serviceLinkName,
                base_url, main_data, rotate_header)
    baseDir = os.path.abspath(os.path.dirname(__name__))
    filename = 'DataOutput/data.json'
    filePath = os.path.join(baseDir, filename)
    with open(filePath, mode='w') as outfile:
        json.dump(main_data, outfile, indent=4)
    print(
        f"Scraping Done! Checkout the data in the following file:{filename}\n\n")
