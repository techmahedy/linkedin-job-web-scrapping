import time
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
import bs4
from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import DataFrame
import csv

job_id              = []
job_name            = []
company_name        = []
date                = []
location            = []
description         = []
level_of_experience = []
employment_type     = []
job_function        = []
industry            = []
data                = []

exp_main            = ""
emp_main            = ""
job_main            = ""
industry_main       = ""

# url = "https://www.linkedin.com/jobs/search/?f_TPR=r604800&geoId=101174742&keywords=data%20analyst&location=Canada&sortBy=DD"
# url = "https://www.linkedin.com/jobs/search?keywords=Data%20Analyst&location=Bangladesh&locationId=&geoId=106215326&sortBy=R&f_TPR=&f_JT=F&position=1&pageNum=0"
# url = "https://www.linkedin.com/jobs/search?keywords=Software%20Engineer&location=Bangladesh&geoId=106215326&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"
# url = "https://www.linkedin.com/jobs/search?keywords=Laravel&location=Bangladesh&geoId=106215326&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"
url = "https://www.linkedin.com/jobs/search?keywords=CEO&location=Dhaka%2C%20Bangladesh&geoId=103363366&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0"

time.sleep(1)

try:

    page = requests.get(url)
    
    soup = BeautifulSoup(page.content,"html.parser")
    
    soup_link = soup.findAll("div", attrs={"class": 'base-card base-card--link base-search-card base-search-card--link job-search-card'})
    
    for x in range(len(soup_link)):
        jb_name = soup_link[x].find('span', { "class": "screen-reader-text" })
        job_name.append(jb_name.text.strip())
        
        print('trace 1')
        job_ids = soup_link[x].find('a', href=True)['href']
        job_ids = re.findall(r'(?!-)([0-9]*)(?=\?)',job_ids)[0]
        job_id.append(job_ids)

        print('trace 2')
        cp_name = soup_link[x].find('a', { "class": "hidden-nested-link" })
        company_name.append(cp_name.text.strip())
        
        
        print('trace 3')
        t_date = soup_link[x].find('time')['datetime']
        date.append(t_date)

        
        print('trace 4')
        cp_location = soup_link[x].find('span', { "class": "job-search-card__location" })
        location.append(cp_location.text.strip())

        
        print('trace 5')
        detail_page_src = soup_link[x].find('a', { "class": "base-card__full-link" })['href']


        
        print('trace 6')
        detail_page_content = requests.get(detail_page_src)
        detail_soup = BeautifulSoup(detail_page_content.content,"html.parser")

        
        print('trace 7')
        cp_description = detail_soup.find('div', { "class": "show-more-less-html__markup" })
        description.append(cp_description.text.strip())

        li = detail_soup.findAll("li", attrs={"class": 'description__job-criteria-item'})

        

        for child in li:
            print('trace 8')
            check_exp_level_text = child.find('h3', { "class": "description__job-criteria-subheader" })
            get_only_text = check_exp_level_text.text.strip()

            
            
            if get_only_text == 'Seniority level':
                cp_experience = child.find('span', { "class": "description__job-criteria-text description__job-criteria-text--criteria" })
                exp_main      = cp_experience.text.strip()
                if not exp_main:
                    exp_main = ""
                level_of_experience.append(cp_experience.text.strip())
                print('trace 9')

                
            
            elif get_only_text == 'Employment type':
                cp_employment = child.find('span', { "class": "description__job-criteria-text description__job-criteria-text--criteria" })
                emp_main      = cp_employment.text.strip()
                if not emp_main:
                    emp_main = ""
                employment_type.append(cp_employment.text.strip())
                print('trace 10')

                

            elif get_only_text == 'Job function':
                cp_job_function = child.find('span', { "class": "description__job-criteria-text description__job-criteria-text--criteria" })
                job_main        = cp_job_function.text.strip()
                if not job_main:
                    job_main = ""
                job_function.append(cp_job_function.text.strip())
                print('trace 11')


            elif get_only_text == 'Industries':
                cp_industry   = child.find('span', { "class": "description__job-criteria-text description__job-criteria-text--criteria" })
                industry_main = cp_industry.text.strip()
                if not industry_main:
                    industry_main = ""
                industry.append(cp_industry.text.strip())
                print('trace 12')

        child = {
            'job_title'          : jb_name.text.strip(),
            'job_id'             : job_ids,
            'company_name'       : cp_name.text.strip(),
            'publish_date'       : t_date,
            'location'           : cp_location.text.strip(),
            'description'        : cp_description.text.strip(),
            'job_level'          : exp_main,
            'job_type'           : emp_main,
            'job_function'       : job_main,
            'categories'         : industry_main     
        }
        print('child', child)
        # break
        data.append(child.copy())
    
    print(data)

    # df = pd.DataFrame.from_dict(data, orient='index')
    # df = df.transpose()
    # df.to_csv('data.csv')

except Exception as error:
    print("Something went wrong!", error)