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
    base_url = "https://www.netmeds.com"
    template = 'https://www.netmeds.com/catalogsearch/result?q={}'
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
        base_url = "https://www.netmeds.com"
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        result = soup.find_all('div', {'class':'drug_c'})

        for item in result:
            link = [base_url + div.a['href'] for div in result]
            for x in link:
                print (x)
    return x

def extract_records(item):
    link = get_inner_link(item)
    header = {'Origin': 'https://www.netmeds.com',
    'Referer': 'link',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
    }

    html = requests.get(url = link, headers = header)
    html.status_code

    bsobj = BeautifulSoup(html.content,'html.parser')
    bsobj

    bsob = bsobj.findAll('div',{'class':'content-section'})

    Name = bsobj.find(attrs = {'class':'black-txt'}).text
    Uses = bsobj.find(attrs = {'class':'col-md-12'}).text
    Precautions = bsobj.find(attrs = {'id':'np_tab3'}).text
    Side_effects = bsobj.find(attrs = {'class':'druginfo-dv'}).text
    Usage = bsobj.find(attrs = {'id':'np_tab4'}).text
    
    
    result = [[Name, Precautions, Uses, Side_effects, Usage]]
    df = pd.DataFrame(result, columns = ['Name', 'Uses', 'Precautions', 'Side Effects', 'Usage'])
    df.to_csv('netmedresults.csv')

extract_records('amodep at 14')
