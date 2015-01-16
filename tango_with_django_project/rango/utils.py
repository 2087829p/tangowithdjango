__author__ = 'tony'

def encode_url(name):
    return name.replace(' ','_')

def decode_url(url):
    return url.replace('_',' ')