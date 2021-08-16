import requests

from bs4 import BeautifulSoup

URL = 'https://stackoverflow.com/jobs?q=python'


def extract_max_page(url):
  request = requests.get(url)
  soup = BeautifulSoup(request.text,"html.parser" )
  pages = soup.find('div',{'class': 's-pagination'}).find_all('a')
  last_page = int(pages[-2].get_text(strip=True))
  return last_page

def extract_job(html):
  title = html.find('h2').find('a').text
  company_row = html.find('h3').find_all('span')
  company = company_row[0].get_text(strip=True)
  location = company_row[1].get_text(strip=True)
  job_id = html['data-jobid']
  link = f'https://stackoverflow.com/jobs/{job_id}/'
  return {'title': title, 'company': company, 'location': location, 'link': link}

def extract_jobs(last_page, url):
  jobs = []
  for page in range(last_page):
    print(f'StackOverflow: парсинг страницы {page}')
    result = requests.get(f'{url}&pg={page+1}')
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all('div', {'class':'-job'})
    for result in results:
      job = extract_job(result)
      jobs.append(job) 
  return jobs 

def get_jobs_so(keyword_2):
  url = f'https://stackoverflow.com/jobs?q={keyword_2}'
  max_page = extract_max_page(url)
  jobs = extract_jobs(max_page, url)
  return jobs