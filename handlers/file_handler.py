import os

import requests


def get_file_size(url: str) -> str:
    '''
    Get file size on http/https
    '''
    with requests.get(url, stream=True) as stream:
        stream.raise_for_status()
        
        if int(stream.headers['Content-Length']) / 1024 ** 3 < 1:
            size = '%.2f' % (int(stream.headers['Content-Length']) / 1024 ** 2)
            return f'{size} MB'
        
        size = '%.2f' % (int(stream.headers['Content-Length']) / 1024 ** 3)
        return f'{size} GB'


def get_local_file_size(path: str) -> str:
    '''
    Get local file size
    '''
    if not os.path.isfile(path):
        return '0 MB'

    unformat_size = os.path.getsize(path)    
    
    if unformat_size / 1024 ** 3 < 1:
        size = '%.2f' % (unformat_size / 1024 ** 2)
        return f'{size} MB'
    
    size = '%.2f' % (unformat_size / 1024 ** 3)
    return f'{size} GB'


def download(url: str, filename: str):
    '''
    Download video
    '''
    with requests.get(url, stream=True) as stream:
        stream.raise_for_status()
        
        with open(filename, 'wb') as file:
            for chunk in stream.iter_content(chunk_size=65536):
                file.write(chunk)
