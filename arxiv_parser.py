import urllib2
from bs4 import BeautifulSoup
import re
import requests
from IPython.display import HTML
import sys, getopt

url = sys.argv[1]
url = 'http://biorxiv.org/content/early/2017/05/10/136473'

manuscript_title = ''
authors = ''
url_pdf = ''
if 'arxiv' in url: #if its arxviv then url_pdf = url + 'https://arxiv.org/abs/1704.05826'
    url_pdf = re.sub('abs', 'pdf', url)
    url_pdf = url_pdf + '.pdf'
    url_pdf = re.sub('https:', 'http:', url_pdf)
    page = requests.get(url)
    soup = BeautifulSoup(page.content)
    #Get Title
    manuscript_title = soup.title.text
    manuscript_title = re.sub('title:', '',manuscript_title )
    manuscript_title = re.sub('[\n]', '', manuscript_title)
    manuscript_title = re.sub('\[.*?\]','', manuscript_title)
    manuscript_title = re.sub(' +',' ',manuscript_title)
    manuscript_title = manuscript_title.lstrip()
    #Get Authors
    for author in soup.find_all('div',attrs={"class":"authors"}):
        authors +=author.text
    line = re.sub('[\n]', '', authors)
    authors = re.sub('Authors:', '', line)
elif 'biorxiv' in url: #if its bioarxiv then url_pdf = url + '.full.pdf'\
    url_pdf = url + '.full.pdf'
    url_pdf = re.sub('https:', 'http:', url_pdf)
    page = requests.get(url)
    soup = BeautifulSoup(page.content)
    #Get Title
    manuscript_title = soup.title.text
    manuscript_title = re.sub('bioRxiv', '',manuscript_title )
    manuscript_title = re.sub('[\n]', '', manuscript_title)
    manuscript_title = re.sub('\|', '', manuscript_title)
    manuscript_title = re.sub('\[.*?\]','', manuscript_title)
    manuscript_title = re.sub(' +',' ',manuscript_title)
    manuscript_title = manuscript_title.lstrip()
    #Get Authors
    for author in soup.find_all('meta',{"name":"citation_author"}):
        authors +=author['content']  + ', '
    #authors = ','.join([str(x) for x in authors])    
    line = re.sub('[\n]', '', authors)
    authors = re.sub('Authors:', '', line)
    authors = authors[:-2]
#Add twitter automatic tweet
inject_this = '<p><a href="' + url + '">"' +  manuscript_title + '"</a>' +  authors + ' (<a class="publinks" href="' + url_pdf + '">pdf</a>)'
print inject_this
