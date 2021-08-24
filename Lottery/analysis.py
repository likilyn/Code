import collections
import os
import pandas as pd
import matplotlib.pyplot as plt
from main import create_the_folder


# Statistics the frequency of each lottery number and draw a pic for it
def statistics(columns_name, target_file_folder, data_source):
    create_the_folder("Pic/" + target_file_folder + "/")
    name = data_source[columns_name]
    statis = collections.Counter(name)
    # the drawing code is from https://www.lanqiao.cn/courses/764/learning/?id=3461
    fig, ax = plt.subplots(figsize=(20, 10))
    x_bar = list(statis.keys())
    y_bar = list(statis.values())
    bars = ax.bar(x_bar, y_bar)
    for i, rect in enumerate(bars):
        x_text = rect.get_x() + 0.25
        y_text = rect.get_height() + 0.3
        plt.text(x_text, y_text, "%.0f" % y_bar[i])
    ax.set_xlabel(columns_name)
    ax.set_ylabel("Times")
    plt.xticks(x_bar)
    plt.savefig(os.getcwd() + "/Pic/" + target_file_folder + "/" + columns_name + ".jpg")
    plt.show()


# Statistics the frequency of all red lottery numbers and draw a pic for it
def statistics2(target_file_folder, method, data_source, n1, n2, color):
    create_the_folder("Pic/" + target_file_folder + "/")

    code = data_source.iloc[:, n1:n2]
    df = code.apply(pd.value_counts).fillna(0)

    # pic(df, target_file_folder)
    # The code below is from https://blog.csdn.net/yangshuo1281/article/details/110264399
    df['Col_sum'] = df.apply(lambda x: pd.to_numeric(x, errors='coerce').sum(), axis=1)
    x_bar = list(df.index)
    y_bar = list(df["Col_sum"])

    # the drawing code is from https://www.lanqiao.cn/courses/764/learning/?id=3461
    fig, ax = plt.subplots(figsize=(20, 10))
    bars = ax.bar(x_bar, y_bar)
    for i, rect in enumerate(bars):
        x_text = rect.get_x() + 0.1
        y_text = rect.get_height() + 0.3
        plt.text(x_text, y_text, "%.0f" % y_bar[i])
    ax.set_xlabel(color)
    ax.set_ylabel("Times")
    plt.xticks(x_bar)
    plt.savefig(os.getcwd() + "/Pic/" + target_file_folder + "/" + color + ".jpg")
    plt.show()


if __name__ == "__main__":
    data1 = pd.read_csv("./File/Lottery.csv")
    data2 = pd.read_csv("./File/3D.csv")

    create_the_folder("Pic")
    for item in data1.columns[1:]:
        statistics(item, "SSQ", data1)
    statistics2("SSQ", "ssq", data1, 1, 7, "Red")
    for item in data2.columns[1:]:
        statistics(item, "3D", data2)
    statistics2("3D", "3D", data2, 1, 3, "Blue")
