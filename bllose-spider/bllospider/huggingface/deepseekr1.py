import requests
from bs4 import BeautifulSoup

def get_download_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    download_links = []
    
    for link in soup.find_all('a', href=True):
        href = link['href']
        if 'resolve/main' in href and 'download=true' in href:
            download_links.append(href)
    
    return download_links

url = 'https://hf-mirror.com/deepseek-ai/DeepSeek-R1/tree/main'
download_links = get_download_links(url)

for link in download_links:
    print(link)
