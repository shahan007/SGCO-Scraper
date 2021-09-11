# SGCO-Scraper-Oct8
Internship project to automate marketing & sales team work.<br>
This scraper scrape all the types, categories and details of the Singapore Companies that are listed on the [web](http://singapore-companies-directory.com/sitemap.htm)<br>
Scraped & Cleaned data is located in DataOutput: [data.json](https://github.com/shahan007/SGCO-Scraper/blob/main/DataOutput/data.json) ; [data.xlsx](https://github.com/shahan007/SGCO-Scraper/blob/main/DataOutput/data.xlsx) ; [extra_cleaned_data.xlsx](https://github.com/shahan007/SGCO-Scraper/blob/main/DataOutput/extra_cleaned_data.xlsx) ; [data_sheets.xlsx](https://github.com/shahan007/SGCO-Scraper/blob/main/DataOutput/data_sheets.xlsx)
<br><br>

### Note !
**ScrapeSgCo** package is the scraper<br>
executable **python script** resides in **ScrapeSgCo** package and you just need to **run** the **main.py** as located in the base dir<br>
**Output** of the main.py script will be the cleaned scraped data stored in data.json located in DataOutput dir<br>
**To convert the data.json to excel file** simply execute convert_to_excel.py located in **excel_util_scripts**<br>
<br><br>

## How to run ?

#### Clone the repo
```bash
$ git clone https://github.com/shahan007/SGCO-Scraper-Oct8
```

#### Setting up the environment
```bash
$ python -m venv venv
$ source venv/Scripts/activate
(venv) $ pip install -r requirements.txt
```

#### Run the Scraper
```bash
(venv) $ python main.py
```
<br><hr>
#### _Optional (convert data.json to excel file for excel experts)_
```bash
(venv) $ python ./excel_util_scripts/convert_to_excel.py
```

#### _Optional (further clean the generated excel file)_
_(further clean data.xlsx file for easier usage of the data) (pre-req is the availability of data.xlsx file resulted from the execution of the convert_to_excel.py )_ <br>
```bash
(venv) $ python ./excel_util_scripts/xtra_clean_excel.py
```

#### _Optional (further splits the clean generated excel file into sheets by WebCategory field)_
```bash
(venv) $ python ./excel_util_scripts/cat_to_sheet.py
```

## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](https://github.com/shahan007/SGCO-Scraper/blob/main/LICENSE) file for details
