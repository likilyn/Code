import collections
import os
import pandas as pd
import matplotlib.pyplot as plt
from main import create_the_folder


# Statistics the frequency of each lottery number and draw a pic for it
def statistics(columns_name):
    name = data[columns_name]
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
    plt.savefig(os.getcwd() + "/Pic/" + columns_name + ".jpg")
    plt.show()


# Statistics the frequency of all red lottery numbers and draw a pic for it
def statistics2():
    code = data.iloc[:, 1:7]
    df = code.apply(pd.value_counts).fillna(0)
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
    ax.set_xlabel("Red")
    ax.set_ylabel("Times")
    plt.xticks(x_bar)
    plt.savefig(os.getcwd() + "/Pic/" + "Red" + ".jpg")
    plt.show()


if __name__ == "__main__":
    data = pd.read_csv("./File/Lottery.csv")
    create_the_folder("Pic")
    for item in data.columns[1:]:
        statistics(item)
    statistics2()
