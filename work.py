import  csv
import  time
import  requests
from bs4 import BeautifulSoup
URL = "https://csie.asia.edu.tw/project/semester-100{0}"


def generate_urls(url, start_page, end_page):                       # 產生urls
    urls = []
    for page in range(start_page, end_page): 
        urls.append(url.format(page))                               #收集每一頁的urls
    return urls


def get_resource(url):                                              #headers假裝是真人在瀏覽網頁防止被拒絕爬蟲!!
    headers = {
        "user-agent": "Mozilla/5.0 (Window NT 10.0; Win64; x64) ApplWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    }
    return requests.get(url, headers=headers)


def parse_html(html_str):                                           #解析html之後變成lxml的形式
    return BeautifulSoup(html_str,"lxml")


def get_contain(soup, file):
    contain = []
    count = 0
    for container_table in soup.find_all(class_="container"):         #從網站程式碼看到 標籤為class
        count += 1
        for word_entry in container_table.find_all("row"):
            new_contain = []                                           #蒐集每一個內容
            new_contain.append(file)
            new_contain.append(str(count))
            new_contain.append(word_entry.th.text)                     #先丟到new_word這個list
            new_contain.append(word_entry.td.text)
            contain.append(new_contain)                                #再丟到words這個list裡
    return contain

def web_scraping_bot(urls):
    projects = []
    for url in urls:
        file = url.split("/")[-1]                                   # -1:讓最後一個值變-1  由後往前為-1,-2,-3.....
        print("catching: ", file, "web data...")
        r = get_resource(url)
        if r.status_code == requests.codes.ok:
            soup = parse_html(r.text)
            contain = get_contain(soup, file)
            projects = projects + contain
            print("waiting 5 seconds.....")
        else:
            print("HTTP request error!!") 
        print("sleep 5 second")                                     #讓他抓完休息5秒再抓以免被發現
    return eng_words        


def save_to_csv(words, file):                                       #存起來用csv檔寫出
    with open(file, "w+", newline = "", encoding = "utf-8") as fp:  # w+:以寫入的方式存起來 newline="":不要空格
        writer = csv.writer(fp)
        for contain in new_contain:
            writer. writerow(contain)


if __name__ == "__main__":
    urlx = generate_urls(URL, 1, 3)
    projects = web_scraping_bot(urlx)
    for item in projects:
        print(item)
    save_to_csv(projects, " projectsList.csv")    