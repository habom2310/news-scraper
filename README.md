# News Scraper 

## 1. How to run
- Requirements:
  - Python > 3.8 environment
  - Install required packages: `pip install -r requirements.txt`
  - Firefox + webdriver for Firefox (geckodriver) https://github.com/mozilla/geckodriver/releases
  - Put file `df_config.json` under `src/backend` for DB credentials

- Run Scraping:
  - Run `python scraping_main.py`

## 2. Scraper
### 2.1. Tools
- Get site's html content (in priority order): requests, selenium (Firefox driver)

### 2.1. Strategy

<p style='margin-top:1em; text-align:center'>Main site -> Category -> Article </p>

- Start from the main site, scraping all the urls for categories (e.g., world, business, ...) and sub-categories (e.g., Asia, Australia, Tech, ...). 
- Go to each categories (or sub-categories), scraping all the urls of the articles shown (use selenium and wait for the page to finish loading). Validate the article urls (some urls come from other sites, or contain only video), keep only valid ones.
- Go to each article, scraping title, metadata (author, publish date), and text.

### 2.2 Generalization
Generalize to scraping from more news sites.

- Tags and class names of certain components are parameterized and defined in the `src/backend/input/data.yml`
- Template for one field is: `<current_page>_<scraping_target>_<parameter>:<value>`

#### Example: 
- `main_category_tag: a`: in the main site, tag of category is `a`
- `main_category_class: sc-fjdhpX sc-chPdSV hnOkcW`: in the main site, class name of the category is `sc-fjdhpX sc-chPdSV hnOkcW`
- `article_title_tag: h1`: in the article site, tag of title is `h1`

**Notes**: make sure values for tag and class name are unique.


## 3. Database
- Type: postgresql 
- Host: AWS RDS db.t3.micro

## 4. Project Structure
- `src/backend/input/`: input/setting files.
- `src/backend/lib/`: code for main features: scrapping, database, ...
- `webdriver/`: web driver for selenium
- `scrapper.ipynb`: notebook for scrapping
- `RDS.ipynb`: notebook for database


## TODO
- [x] Create Postgresql Database in AWS
- [x] Code to scraping articles from CNN
- [x] Define DB structure
- [x] Logging
- [x] Clean, map and push scraping data to DB
- Analyse data
  - [ ] Sentimental
  - [ ] Statistical 
  - [ ] Relationship
- [ ] Generalize scraping strategy
- [ ] Create install file


