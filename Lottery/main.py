import csv
import json
import os
import re
import requests
import tqdm
import pandas as pd


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("---  new folder...  ---")
        print("---  OK  ---")
    else:
        print("---  There is this folder!  ---")


def create_the_folder(classname):
    program_path = os.getcwd()
    mkdir(program_path + '/' + classname + '/')


def get_data(quary_type, start_date, end_date, target_file_name):
    create_the_folder("File")
    father_url = "http://www.cwl.gov.cn/cwl_admin/kjxx/findDrawNotice?name=" + quary_type + "&issueCount=&issueStart=&issueEnd=&dayStart=" + start_date + "&dayEnd=" + end_date + "&pageNo="
    headers = {
        "Host": "www.cwl.gov.cn",
        "Referer": "http://www.cwl.gov.cn/kjxx/ssq/kjgg/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    }
    response = requests.get(url=father_url, headers=headers)
    text = response.text
    jsonobj = json.loads(text)
    pageCount = jsonobj["pageCount"]
    url_list = []
    for i in range(1, pageCount + 1):
        url_list.append(father_url + str(i))

    rows = []
    for u in tqdm.tqdm(url_list):
        r = requests.get(url=u, headers=headers)
        # Get Response json Data
        text = r.text
        jsonobj = json.loads(text)
        row = []
        for item in jsonobj["result"]:
            data = item["date"] + " " + item["red"] + " " + item["blue"]
            row.append(data)
        rows.append(row)
    # Write the lottery into a csv file
    with open(os.getcwd() + "/File/" + target_file_name + ".csv", "w", encoding="utf-8") as f:
        f_csv = csv.writer(f)
        for r in rows:
            for e in r:
                f_csv.writerow([e])
        f.close()
    # Split each number of the red lottery number for the coming analysis
    data = pd.read_csv("./File/" + target_file_name + ".csv")
    if quary_type == "ssq":
        values = []
        for i in tqdm.tqdm(range(len(data))):
            content = re.split(r"\s", data.values[i][0])
            date = content[0]
            blue = content[2]
            red = re.split(r",", content[1])
            red1 = red[0]
            red2 = red[1]
            red3 = red[2]
            red4 = red[3]
            red5 = red[4]
            red6 = red[5]
            value = [date, red1, red2, red3, red4, red5, red6, blue]
            values.append(value)

        columns = ["Date", "Red1", "Red2", "Red3", "Red4", "Red5", "Red6", "Blue"]
        df = pd.DataFrame(values, columns=columns)
        df.to_csv("./File/" + target_file_name + ".csv", index=False)
    elif quary_type == "3d":
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
        df.to_csv("./File/" + target_file_name + ".csv", index=False)


get_data("ssq", "2020-01-01", "2021-08-24", "SSQ")
get_data("3d", "2020-01-01", "2021-08-24", "3d")
