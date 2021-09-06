# SGCO-Scraper-Oct8
Internship project to automate marketing & sales team work.<br>
This scraper scrape all the types, categories and details of the Singapore Companies that are listed on the [web](http://singapore-companies-directory.com/sitemap.htm)
<br><br>

### Note !
NotebookReview is just a dir that runs the exact scraper from jupyter notebook<br>
Upon cloning the repo if you don't want to view the Notebook you can simply delete it as the <br>
executable **python script** resides in **ScrapeSgCo** package and you just need to **run** the **main.py** as located in the base dir<br>
**Output** of the main.py script will be the cleaned scraped data stored in data.json located in DataOutput dir<br>
**To convert the data.json to excel file** simply execute convert_to_excel.py<br>
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
#### _Optional (convert data.json to excel file for excel experts)_
```bash
(venv) $ python convert_to_excel.py
```
## License
This project is licensed under the GNU General Public License v3.0 - see the [LICENSE.md](https://github.com/shahan007/SGCO-Scraper/blob/main/LICENSE) file for details
