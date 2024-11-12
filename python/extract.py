import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, unquote
from mimetypes import guess_extension

def sanitize_filename(filename):
    filename = unquote(filename) 
    filename = filename.split('?')[0]  
    return re.sub(r'[\\/*?:\"<>|]', '_', filename)

def download_resources_from_url(url, folder_path='extracted'):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    resources = []
    resources.extend(soup.find_all('img', src=True))
    resources.extend(soup.find_all('script', src=True))
    resources.extend(soup.find_all('link', href=True))
    for resource in resources:
        if resource.name == 'img':
            resource_url = resource['src']
        elif resource.name == 'script':
            resource_url = resource['src']
        elif resource.name == 'link' and resource.get('rel') == ['stylesheet']:
            resource_url = resource['href']
        else:
            continue
        resource_url = urljoin(url, resource_url)
        try:
            res_response = requests.get(resource_url)
            res_response.raise_for_status()
            parsed_url = urlparse(resource_url)
            filename = os.path.basename(parsed_url.path)
            if not filename or '.' not in filename:
                content_type = res_response.headers.get('Content-Type')
                file_ext = guess_extension(content_type) or '.bin'
                filename = f'resource_{resources.index(resource)}{file_ext}'
            filename = sanitize_filename(filename)
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'wb') as file:
                file.write(res_response.content)
            print(f'Resource saved: {file_path}')
        except requests.RequestException as e:
            print(f'Error downloading resource {resource_url}: {e}')

url = 'https://www.edupedu.ro/ultima-ora-modele-de-subiecte-evaluarea-nationala-2025-publicate-de-ministerul-educatiei-descarca-test-en-viii-limba-romana-matematica-limba-materna-si-romana-pentru-etnicii-maghiari/'
download_resources_from_url(url)