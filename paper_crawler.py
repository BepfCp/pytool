"""
Crawler all papers from a given conference, currently only support ICML2022
"""
import re
import requests as rq
from bs4 import BeautifulSoup as bf
import csv

accepted_paper_url = 'https://icml.cc/Conferences/2022/AcceptedPapersInitial'

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
}

spinningup_html = rq.get(accepted_paper_url, headers=headers)
soup = bf(spinningup_html.content, 'lxml')
papers = soup.find_all(name='p')

pattern = re.compile(r'[()](.*?)[)]', re.S)
with open('out/icml2022.csv', 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['title', 'authors', 'institues'])
    for paper in papers:
        try:
            title = paper.b.string.strip()
            infos = paper.i.string.strip().split('·')
            authors, institutes = [], []
            for info in infos:
                institute = re.findall(pattern, info)
                if not institute[0] in institutes:
                    institutes += institute
                author = info[:info.find('(')].strip()
                authors.append(author)
            writer.writerow([title, ';'.join(authors), ';'.join(institutes)])
        except:
            pass


