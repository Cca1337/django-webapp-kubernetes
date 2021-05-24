import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0',
           'Accept': "text/html",
           'Accept-Language': "sk-SK",
           'Content-Language': "sk-SK",
           "Accept-Encoding": "gzip, deflate"
}

def get_weather_scrape(mesto):

    mesto = mesto.lower()

    search = f"pocasie+{mesto}"
    URL = f"http://www.google.sk/search?q={search}"

    req = requests.get(URL, headers=headers)

    soup = BeautifulSoup(req.content, "html.parser")

    temperature = soup.find("div", {"class": "BNeawe iBp4i AP7Wnd"}).get_text()
    region = soup.find("span", {"class": "BNeawe tAd8D AP7Wnd"}).get_text()
    day_and_weather_condition = soup.find("div", {"class": "BNeawe tAd8D AP7Wnd"}).get_text()

#    prevodteploty = float(temperature.split("°")[0])
#    prevodteploty = round((prevodteploty - 32) / 1.8, 1)

    list1 = day_and_weather_condition.split(" ")
    list2 = list1[1].split("\n")

    pocasie = f"V meste {region} je momentalne {list1[0]}  {list2[0]} a aktualne je {list2[1].lower()} s teplotou {temperature}"

    return pocasie
