import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import csv
import pandas as pd

def get_url(search_term):
    '''
    This function fetches the URL of the item that you want to search
    '''
    base_url = "https://www.1mg.com/"
    template = 'https://www.1mg.com/search/all?name={}'
    # We'are replacing every space with '+' to adhere with the pattern 
    search_term = search_term.replace(" ","+")
    
    # add term query to url
    url = template.format(search_term)
    return url

def get_inner_link(search_term):
    '''Post the url extraction, we extract the link to the particular medicine page'''
    for page in range(0,1):
        url = get_url(search_term)
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url.format(page))
        base_url = "https://www.1mg.com"
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        result = soup.find_all('div', {'class':'col-xs-12 col-md-9 col-sm-9 style__container___cTDz0'})

        for item in result:
            link = [base_url + div.a['href'] for div in result]
            for x in link:
                print (x)
    return x

def extract_records(item):
    link = get_inner_link(item)
    header = {'Origin': 'https://www.1mg.com',
    'Referer': 'link',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    }

    html = requests.get(url = link, headers = header)
    html.status_code

    bsobj = BeautifulSoup(html.content,'html.parser')
    bsobj

    bsob = bsobj.findAll('div',{'id':'drug-main-header'})

    Name = bsobj.find(attrs = {'class':'DrugHeader__title-content___2ZaPo'}).text
    Info = bsobj.find(attrs = {'class':'DrugOverview__content___22ZBX'}).text
    Side_effects = bsobj.find(attrs = {'class':'DrugOverview__list-container___2eAr6 DrugOverview__content___22ZBX'}).text
    Uses = bsobj.find(attrs = {'id':'how_drug_works'}).text
    Works = bsobj.find(attrs = {'id':'how_to_use'}).text
    
    
    result = [[Name, Info, Uses, Side_effects, Works]]
    df = pd.DataFrame(result, columns = ['Name', 'Info', 'Uses', 'Side Effects', 'Working'])
    df.to_csv('medresults.csv')

extract_records('amodep at 14')
