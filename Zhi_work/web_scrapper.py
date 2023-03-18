import urllib.request

url = 'https://google.com'

# Perform the request
request = urllib.request.Request(url)
raw_response = urllib.request.urlopen(request).read()

# Read the repsonse as a utf-8 string
html = raw_response.decode()

print(html)
