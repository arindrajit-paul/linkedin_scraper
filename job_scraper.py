import csv
import requests
from bs4 import BeautifulSoup

file = open('data-analyst-jobs.csv', mode='a')
writer = csv.writer(file)
writer.writerow(['Title', 'Company', 'Location', 'Link'])

def scraper(web_page, page_number):
    next_page = web_page + str(page_number)
    print(str(next_page))
    response = requests.get(str(next_page))
    soup = BeautifulSoup(response.content, 'html.parser')

    jobs = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card')
    for job in jobs:
        try:
            title = job.find('h3', class_='base-search-card__title').text.strip()
            company = job.find('h4', class_='base-search-card__subtitle').text.strip()
            location = job.find('span', class_='job-search-card__location').text.strip()
            link = job.find('a', class_='base-card__full-link')['href']
        except IndexError:
            title = ''
            company = ''
            location = ''
            link = ''
        writer.writerow([title, company, location, link])

        writer.writerow([
        title.encode('utf-8'),
        company.encode('utf-8'),
        location.encode('utf-8'),
        link.encode('utf-8')
        ])
    print('Data has been scraped successfully!')

url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Data%20Analyst&location=United%20States&geoId=103644278&f_TPR=&f_E=2&position=1&pageNum='
page_num = 0
if page_num < 25:
    page_num += 25
    scraper(url, page_num)
else:
    file.close()
    print('File has been closed!')

scraper(url, page_num)
