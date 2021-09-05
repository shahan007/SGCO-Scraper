# ------------------ Imports ------------------
import requests as req
import re

# ------ Helper Methods ------


def generate_prod_serv_names(xpath_data, expression):
    """
    Generate Products and Service Names. It takes in expression for each type and fetched the cleaned data
    """

    regex_strip_expression = r'[\n\r\t\xa0]'
    regex_strip_rtn = re.compile(regex_strip_expression)
    xpath_data_name = xpath_data.xpath(expression)
    xpath_data_name = [regex_strip_rtn.sub(
        '', str_).strip() for str_ in xpath_data_name]
    return xpath_data_name


def zipper(links, names):
    """
    Zips relative links and link associated text name
    """

    return list(zip(names, links))


def convert_to_absolute_links(linkArray, base_url):
    """
    Transform the relative links to absolute links
    """

    return [req.compat.urljoin(base_url, link) for link in linkArray]
