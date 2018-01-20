import urllib.request

def download_file(url, file):
    urllib.request.urlretrieve (url, file)