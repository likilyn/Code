import csv
import os
import re
import pandas as pd
import requests
import json

import tqdm

# father_url = "http://www.cwl.gov.cn/cwl_admin/kjxx/findDrawNotice?name=3d&issueCount=&issueStart=&issueEnd=&dayStart=2012-10-01&dayEnd=2021-08-24&pageNo="
# father_url = "http://www.cwl.gov.cn/cwl_admin/kjxx/findDrawNotice?name=3d&issueCount=&issueStart=&issueEnd=&dayStart=2012-10-01&dayEnd=2021-08-24&pageNo="
quary_type = "ssq"
start_date = "2020-07-01"
end_date = "2021-08-24"
father_url = "http://www.cwl.gov.cn/cwl_admin/kjxx/findDrawNotice?name=" + quary_type + "&issueCount=&issueStart=&issueEnd=&dayStart=" + start_date + "&dayEnd=" + end_date + "&pageNo="
print(father_url)
url_list = []
for i in range(1, 31):
    url_list.append(father_url + str(i))

headers = {"Host": "www.cwl.gov.cn",
                   "Referer": "http://www.cwl.gov.cn/kjxx/fc3d/kjgg/",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}
r = requests.get(url=father_url, headers=headers)
text = r.text
jsonobj = json.loads(text)
print(jsonobj)





def get_data():
    rows = []
    for url in url_list:
        headers = {"Host": "www.cwl.gov.cn",
                   "Referer": "http://www.cwl.gov.cn/kjxx/fc3d/kjgg/",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"}
        r = requests.get(url=url, headers=headers)
        text = r.text
        jsonobj = json.loads(text)
        row = []
        for j in jsonobj["result"]:
            code = j["red"]
            date = j["date"]
            data = date + " " + code
            row.append(data)
        rows.append(row)
    # print(rows)
    with open(os.getcwd() + "/File/" + "3D.csv", "w", encoding="utf-8") as f:
        f_csv = csv.writer(f)
        for r in rows:
            for e in r:
                f_csv.writerow([e])
        f.close()
    data = pd.read_csv("./File/3D.csv")

    values = []
    for i in tqdm.tqdm(range(len(data))):
        content = re.split(r"\s", data.values[i][0])
        date = content[0]
        number = content[1]
        red = re.split(r",", content[1])
        red1 = red[0]
        red2 = red[1]
        red3 = red[2]
        value = [date, red1, red2, red3]
        values.append(value)

    columns = ["Date", "Blue1", "Blue2", "Blue3"]
    df = pd.DataFrame(values, columns=columns)
    df.to_csv("./File/3D.csv", index=False)


# get_data()
