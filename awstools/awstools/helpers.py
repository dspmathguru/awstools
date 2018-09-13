import urllib.request

def getMyIP():
  return urllib.request.urlopen('https://ident.me').read().decode('utf8')

