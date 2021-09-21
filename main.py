import requests
from bs4 import BeautifulSoup

PAGE_URL = "https://kulturenvanteri.com/arastir/d/?_paged="

for i in range(1, 477):
    print("syafa : ", i)
    r = requests.get(PAGE_URL + str(i))
    source = BeautifulSoup(r.content, "lxml")
    print(PAGE_URL + str(i))
    get_card_class = source.find_all("a", attrs={"class": "modal-link"})
    with open("card_url.txt", "a") as file:
        for i in get_card_class:
            url = str(i["href"])
            if "/yer/" in url:
                file.write(url + "\n")
                print(url)
