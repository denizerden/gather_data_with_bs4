import requests
from bs4 import BeautifulSoup
import json
import threading
import sqlite3 as sql


def parse(start_index,end_index, vt,im):
    with open("data.txt","a",encoding="utf-8") as data_file:
        with open("card_url.txt", "r") as file:
            lines = file.readlines()[start_index:end_index]

            for i in lines:
                r = requests.get(i)
                source = BeautifulSoup(r.content, "lxml")
                get_ul = source.find("ul", attrs={"class": "list-unstyled"})

                get_li = get_ul.find_all("li")

                place_dict = {}
                place_dict["place_group"] = ""
                place_dict["place_type"] = ""
                place_dict["area"] = ""
                place_dict["culture"] = ""
                place_dict["century"] = ""
                for li in get_li:
                    item = li.text
                    if "Grup:" in item:
                        place_dict["place_group"] = item.split(":")[1].replace("\n", "")
                    if "Tür:" in item:
                        place_dict["place_type"] = item.split(":")[1].replace("\n", "")
                    if "Bölge:" in item:
                        place_dict["area"] = item.split(":")[1].replace("\n", "")
                    if "Kültür:" in item:
                        place_dict["culture"] = item.split(":")[1].replace("\n", "")
                    if "Yüzyıl:" in item:
                        place_dict["century"] = item.split(":")[1].replace("\n", "")
                tmp = source.find("div", {"id": "modal-ready"})
                place_dict["description"] = tmp.find("p").text.replace('"',"'") if tmp.find("p") else ""
                images = tmp.find_all("img")
                place_dict["place_name"] = tmp.find("a").text
                coordinates_link = tmp.find_all("span",attrs={"class":"googlemap"})[1]
                coordinates_link = coordinates_link.find("a")["href"]
                place_dict["coordinates"] = coordinates_link.split("/")[-1]
                images_list = []
                for img in images:
                    images_list.append(img["data-src"])
                place_dict["images"] = images_list
                place_dict["link"] = i
                # print(place_dict)
                data_file.write(str(place_dict)+"\n")
                query = """INSERT INTO data_table(place_name, description, images, place_group, place_type, area, culture, century, cooordinates, link) VALUES("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")"""%(place_dict["place_name"], place_dict["description"], str(place_dict["images"]), place_dict["place_group"], place_dict["place_type"], place_dict["area"], place_dict["culture"], place_dict["century"], place_dict["coordinates"], place_dict["link"])
                print(query)
                im.execute(query)
                vt.commit()







if __name__=="__main__":

    vt = sql.connect('kultur_app.sqlite3')
    im = vt.cursor()
    im.execute(
        """CREATE TABLE IF NOT EXISTS data_table ("place_name","description","images","place_group","place_type","area","culture","century","cooordinates","link")""")
    parse(931,24360,vt,im)
    im.close()
    # t1 = threading.Thread(target=parse, args=(0,4872,vt,im))
    # t2 = threading.Thread(target=parse, args=(4873,9744,vt,im))
    # t3 = threading.Thread(target=parse, args=(9744, 14616,vt,im))
    # t4 = threading.Thread(target=parse, args=(14617, 19488,vt,im))
    # t5 = threading.Thread(target=parse, args=(19489, 24360,vt,im))
    #
    # t1.start()
    # t2.start()
    # t3.start()
    # t4.start()
    # t5.start()


