from bs4 import BeautifulSoup
import requests
from flask import Flask,request,render_template;
import re

app = Flask(__name__)


def getjobs(keyword,location =''):
    url = f'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={keyword}&txtLocation={location}'
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'lxml')

    # Find job listings
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')


    job_list = []


 

    # Extract job details
    for job in jobs:
        comp_name = job.find('h3', class_='joblist-comp-name').text.strip()
        skills = job.find('span', class_='srp-skills').text.strip().split(',')
        location = job.find('ul', class_='top-jd-dtl clearfix').findChild('span').text.strip()
        job_desc = job.find('ul',class_='list-job-dtl clearfix').findChild('li').text.split('\n')[2]
        a    = job.find('ul',class_='list-job-dtl clearfix').findChild('a')
       
        job_list.append({'comp_name': comp_name, 'skills': skills, 'location': location,'job_desc':job_desc,'link':a['href']})

    return job_list



@app.route('/',methods=['GET','POST'])
def index():
    jobList = []
    keyword = ''  
    location = ''
    if request.method == 'POST':
        keyword = request.form['keyword']
        location = request.form['location']
        jobList = getjobs(keyword, location)
    return render_template('jobs.html', jobs=jobList,keyword=keyword,location=location)







app.run(debug=True)
