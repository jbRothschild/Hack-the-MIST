import urllib.request
import time
import os
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
import pandas as pd

def remove_tags(soup):

    for data in soup(['style', 'script']):
        # Remove tags
        data.decompose()
 
    # return data by retrieving the tag content
    return ' '.join(soup.stripped_strings)

def get_links(soup):
    divs = soup.select("#search div.g")
    out = []
    for div in divs:
        results = div.find("a", href = True)

        # Check if we have found a result
        if (len(results) >= 1):

            # Print the title
            h3 = results["href"]
            out.append(h3)

    return out

def ifcontains(url_str, ignore_list):
    res = [ele for ele in ignore_list if(ele in url_str)]
    return bool(res)

def main(corpo):
    keyword = "climate"
    url = "https://google.com/search?q=" + corpo.replace(" ", "+") + "+" + keyword
    ignore_list = ["reddit", "twitter", "dailywire", "guardian", "bbc", "cbc", "forum"]
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}
    
    time.sleep(15)
    request = urllib.request.Request(url = url, headers=headers)
    raw_response = urllib.request.urlopen(request).read()
    str_html = raw_response.decode(encoding='utf-8', errors='ignore')

    soup = BeautifulSoup(str_html, 'html.parser')
    link_txt = get_links(soup)

    for link in link_txt:

        if link.endswith(".pdf") or ifcontains(link, ignore_list):
            print(link)
            continue
        else:
            url_corp = link
            print(corpo, " | ", url_corp)
            break

    time.sleep(10)
    request = urllib.request.Request(url = url_corp, headers=headers)
    raw_response = urllib.request.urlopen(request).read()

    str_html = raw_response.decode(encoding='utf-8', errors='ignore')
    soup = BeautifulSoup(str_html, 'html.parser')
    web_text = remove_tags(soup)

    output_name = '../company_data/' + corpo + '.txt'
    if os.path.exists(output_name):
        os.remove(output_name)

    with open(output_name, 'w') as f:
        f.write(web_text)

if __name__ == "__main__":
    try:  
        corpos = pd.read_csv("company_names/corporation_names.csv").name.tolist()
        for corpo in corpos:
            try:
                main(corpo)
            except:
                print("Company that Raised an Error: " + corpo)
                continue
    except KeyboardInterrupt:
        pass

