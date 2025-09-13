import csv
import multiprocessing
import random
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
from bs4.element import NavigableString


ID_LIST = []
with open(r"./blog_id_list.csv", mode="r") as f:
    lines = f.readlines()
    for _line in lines:
        url_id = _line.strip().split(",")[3].split(".")[0]
        ID_LIST.append(url_id)


def get_content(urlid, fileid):
    interval_time = random.uniform(3, 3.5)
    time.sleep(interval_time)
    url = "https://news.livedoor.com/article/detail/" + urlid + "/"
    print(url)
    try:
        with urlopen(url) as res:
            # 本文を取得する
            main_article = ""
            html = res.read().decode("euc_jp", "ignore")
            soup = BeautifulSoup(html, "html.parser")
            linelist = soup.select(".articleBody p")
            for line in linelist:
                if len(line.contents) > 0 and type(line.contents[0]) is NavigableString:
                    main_article += str(line.contents[0]).strip()
            if main_article == "":  # 本文がホームページに無かった場合は処理を抜ける
                return
            # 要約を取得する
            summary_article = ""
            summarylist = soup.select(".summaryList li")
            for summary in summarylist:
                summary_article += str(summary.contents[0]).strip() + "。"
            if summary_article == "":  # 要約がホームページに無かった場合は処理を抜ける
                return
            # 結果をcsvファイルに書き出す
            with open(r"./output_result_{a}.csv".format(a=fileid), mode="a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([summary_article, main_article])
    except Exception as e:
        print(e)


def main_01(_from, _to):
    for i in range(_from, _to):
        print("{a}つ目".format(a=i+1))
        get_content(urlid=ID_LIST[i], fileid="01")


def main_02(_from, _to):
    for i in range(_from, _to):
        print("{a}つ目".format(a=i+1))
        get_content(urlid=ID_LIST[i], fileid="02")


def main_03(_from, _to):
    for i in range(_from, _to):
        print("{a}つ目".format(a=i+1))
        get_content(urlid=ID_LIST[i], fileid="03")


if __name__ == "__main__":
    process_pool = multiprocessing.Pool(3)
    process_pool.apply_async(main_01, args=(0, 10))
    process_pool.apply_async(main_02, args=(10, 20))
    process_pool.apply_async(main_03, args=(20, 30))
    print("process runs")
    process_pool.close()
    process_pool.join()
    print("process done")
