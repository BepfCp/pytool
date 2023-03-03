import os
import time
import urllib.request as url_re
import requests as rq
from bs4 import BeautifulSoup as bf

'''Automatically download all the key papers recommended by OpenAI Spinning Up.
See more info on: https://spinningup.openai.com/en/latest/spinningup/keypapers.html

Dependency:
    bs4, lxml
'''

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
}

spinningup_url = 'https://spinningup.openai.com/en/latest/spinningup/keypapers.html'

paper_id = 1

def download_pdf(pdf_url, pdf_path):
    """Automatically download PDF file from Internet

    Args:
        pdf_url (str): url of the PDF file to be downloaded
        pdf_path (str): save routine of the downloaded PDF file
    """
    if os.path.exists(pdf_path): return
    try:
        with url_re.urlopen(pdf_url) as url:
            pdf_data = url.read()
            with open(pdf_path, "wb") as f:
                f.write(pdf_data)
    except:  # fix link at [102]
        pdf_url = r"https://is.tuebingen.mpg.de/fileadmin/user_upload/files/publications/Neural-Netw-2008-21-682_4867%5b0%5d.pdf"
        with url_re.urlopen(pdf_url) as url:
            pdf_data = url.read()
            with open(pdf_path, "wb") as f:
                f.write(pdf_data)
    time.sleep(10)  # sleep 10 seconds to download next
           
def download_from_bs4(papers, category_path):
    """Download papers from Spinning Up

    Args:
        papers (bs4.element.ResultSet): 'a' tags with paper link
        category_path (str): root dir of the paper to be downloaded
    """
    global paper_id
    print("Start to ownload papers from catagory {}...".format(category_path))
    for paper in papers:
        paper_link = paper['href']
        if not paper_link.endswith('.pdf'):
            if paper_link[8:13] == 'arxiv':
                # paper_link = "https://arxiv.org/abs/1811.02553" 
                paper_link = paper_link[:18] + 'pdf' + paper_link[21:] + '.pdf' # arxiv link
            elif paper_link[8:18] == 'openreview':  # openreview link
                # paper_link = "https://openreview.net/forum?id=ByG_3s09KX"
                paper_link = paper_link[:23] + 'pdf' + paper_link[28:]
            elif paper_link[14:18] == 'nips':  # neurips link
                paper_link = "https://proceedings.neurips.cc/paper/2017/file/a1d7311f2a312426d710e1c617fcbc8c-Paper.pdf"
            else: continue
        paper_name = '[{}] '.format(paper_id) + paper.string + '.pdf'
        if ':' in paper_name:
            paper_name = paper_name.replace(':', '_')
        if '?' in paper_name:
            paper_name = paper_name.replace('?', '')
        paper_path = os.path.join(category_path, paper_name)
        download_pdf(paper_link, paper_path)
        print("Successfully downloaded {}!".format(paper_name))
        paper_id += 1
    print("Successfully downloaded all the papers from catagory {}!".format(category_path))
       

def _save_html(html_url, html_path):
    """Save requested HTML files

    Args:
        html_url (str): url of the HTML page to be saved
        html_path (str): save path of HTML file
    """
    html_file = rq.get(html_url, headers=headers)
    with open(html_path, "w", encoding='utf-8') as h:
        h.write(html_file.text)

def download_key_papers(root_dir):
    """Download all the key papers, consistent with the categories listed on the website

    Args:
        root_dir (str): save path of all the downloaded papers
    """
    # 1. Get the html of Spinning Up
    spinningup_html = rq.get(spinningup_url, headers=headers)
    
    # 2. Parse the html and get the main category ids
    soup = bf(spinningup_html.content, 'lxml')
    
    # _save_html(spinningup_url, 'spinningup.html')
    # spinningup_file = open('spinningup.html', 'r', encoding="UTF-8")
    # spinningup_handle = spinningup_file.read()
    # soup = bf(spinningup_handle, features='lxml')
    
    category_ids = []
    categories = soup.find(name='div', attrs={'class': 'section', 'id': 'key-papers-in-deep-rl'}).\
                find_all(name='div', attrs={'class': 'section'}, recursive=False)
    for category in categories:
        category_ids.append(category['id'])
    
    # 3. Get all the categories and make corresponding dirs
    category_dirs = []
    if not os.path.exitis(root_dir):
        os.makedirs(root_dir)
    for category in soup.find_all(name='h2'):
        category_name = list(category.children)[0].string
        if ':' in category_name:  # replace ':' with '_' to get valid dir name
            category_name = category_name.replace(':', '_')
        category_path = os.path.join(root_dir, category_name)
        category_dirs.append(category_path)
        if not os.path.exists(category_path):
            os.makedirs(category_path)
            
    # 4. Start to download all the papers
    print("Start to download key papers...")
    for i in range(len(category_ids)):
        category_path = category_dirs[i]
        category_id = category_ids[i]
        content = soup.find(name='div', attrs={'class': 'section', 'id': category_id})
        inner_categories = content.find_all('div')
        if inner_categories != []:
            for category in inner_categories:
                category_id = category['id']
                inner_category = category.h3.text[:-1]
                inner_category_path = os.path.join(category_path, inner_category)
                if not os.path.exists(inner_category_path):
                    os.makedirs(inner_category_path)
                content = soup.find(name='div', attrs={'class': 'section', 'id': category_id})
                papers = content.find_all(name='a',attrs={'class': 'reference external'})
                download_from_bs4(papers, inner_category_path)      
        else:
            papers = content.find_all(name='a',attrs={'class': 'reference external'})
            download_from_bs4(papers, category_path)
    print("Download Complete!")

if __name__ == "__main__":
    root_dir = "key-papers"
    download_key_papers(root_dir)