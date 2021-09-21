# import sqlite3 as sql
# import json
# vt = sql.connect('kultur_app.sqlite3')
# im = vt.cursor()
# im.execute("""CREATE TABLE IF NOT EXISTS data_table ("name","description","images","group","type","area","culture","century","cooordinates","link")""")
#
# with open("data.txt","r",encoding="utf-8") as f:
#     lines = f.readlines()
#     for line in lines:
#         place_dict = json.loads(line)
#         print(place_dict)
#
#         table_keys = ",".join([key for key in place_dict.keys()])
#         table_values = ",".join([str(value) for value in place_dict.values()])
#
#         query = "INSERT INTO data_table (" + table_keys + ") VALUES (" + table_values + ");"
#         print(query)
#         im.execute(query)
#
#         # query = """INSERT INTO data (name, description, images, group, type, area, culture, century, cooordinates, link) VALUES ("{name}","{description}","{images}","{group}","{type}","{area}","{culture}","{century}","{cooordinates}","{link}")""".format(*place_dict)
#         # im.execute(query)
#         break
import json

with open("data.txt", "r") as file:
    lines = file.readlines()
    data={
        "data":[]
    }
    for i in lines:
        line = json.loads(i)
        data["data"].append(line)

    with open("data.json","w") as wr:
        wr.write(str(data))
