import argparse
import os
import requests
from datetime import datetime
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup

def save_webpage(url):
    # Fetch web page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Record metadata
    num_links = 0
    num_images = 0
    for tag in soup.find_all():
        if tag.name == 'a' and tag.get('href'):
            num_links += 1
        elif tag.name == 'img' and tag.get('src'):
            num_images += 1

    # Save web page and assets to disk
    base_url = urlparse(url).scheme + '://' + urlparse(url).netloc
    filename = os.path.join(os.getcwd(), urlparse(url).netloc + ".html")
    with open(filename, 'wb') as f:
        f.write(response.content)
    for tag in soup.find_all():
        if tag.name == 'img' and tag.get('src'):
            asset_url = tag['src']
            if asset_url.startswith('/'):
                asset_url = base_url + asset_url
            elif not asset_url.startswith('http'):
                asset_url = urljoin(url, asset_url)
            response = requests.get(asset_url)
            asset_filename = os.path.join(os.getcwd(), os.path.dirname(filename), os.path.basename(asset_url))
            with open(asset_filename, 'wb') as f:
                f.write(response.content)

    # print matadata
    print('site:', urlparse(url).netloc)
    print('num_links:', num_links)
    print('num_images:', num_images)
    print('last_fetch:', datetime.utcnow().strftime('%a %b %d %Y %H:%M:%S UTC'))
    

if __name__ == '__main__':
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Fetch web pages and save them to disk.')
    parser.add_argument('urls', nargs='+', help='URLs of the web pages to fetch')
    parser.add_argument('--metadata', action='store_true', help='Print metadata for each fetched page')
    args = parser.parse_args()

    # Save each web page and print metadata if requested
    for url in args.urls:
        save_webpage(url)
        if args.metadata:
            print()
