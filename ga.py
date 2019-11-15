# -*- coding:utf8 -*-
import multiprocessing
# Last Modified : Fri Nov 15 23:11:06 2019


def get_data():
    return {"mihui":"baidu"}, {"mihui":{"url":"https://ccsight.cn/", "name":"mihui"}, "baidu":{"url":"https://www.baidu.com", "name":"baidu"}}
    return json.loads(open("datafile").read())

def write_data(data):
    with open("datafile", "w") as fw:
        fw.write(json.dumps(data))

class MyThread:
    def logic(self, product):
        url = product["url"]
        from selenium import webdriver
        from selenium.webdriver.support.ui import WebDriverWait
        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("--proxy-server=http://172.16.1.252:8123/")
        driver = webdriver.Chrome(chrome_options = chromeOptions)
        # driver = webdriver.Chrome()
        driver.implicitly_wait(8)
        driver.get("https://developers.google.com/speed/pagespeed/insights/") 
        inputt = driver.find_element_by_xpath(r'//*[@id="page-speed-insights"]/div[1]/form/div/input')
        inputt.clear()
        inputt.send_keys(url)
        inputt.send_keys(Keys.ENTER)
        wait = WebDriverWait(driver, 120)
        try:
            tag1 = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text() = '实测数据']")))
        except Exception:
            driver.refresh()  # 刷新方法 重新检查
            try:
                tag1 = wait.until(EC.presence_of_element_located((By.XPATH, "//span[text() = '实测数据']")))
            except Exception:
                return
        driver.find_element_by_xpath("//div[@class='tab-title tab-desktop']").click()
        try:
            score1 = driver.find_element_by_xpath(
                r'/html/body/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/div[1]/a/div[2]')
        except Exception:
            driver.refresh()  # 刷新方法 重新检查
            try:
                score1 = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div[2]/div[2]/div[1]/div/div[1]/a/div[2]")))
            except Exception:
                return
        score = score1.text
        if score != '' and score != '?':  # 检测出错偶会出现分数为？ 的情况
            score = int(score)  # 获取到的分数为字符串形式，需整型化
            return product["name"], score

def sum_score(data_dict):
    return dict([(name, sum(data_dict[name]["score"])/len(data_dict[name]["score"]))for name in data_dict])

def thread(product):
    return MyThread().logic(product)

def main():
    pair_dict, product_dict = get_data()
    pool = multiprocessing.Pool(2 * multiprocessing.cpu_count())
    name_score_list = pool.map_async(thread, product_dict.values())
    for line in name_score_list.get():
        if line:
            name, score = line
            product_dict[name]["score"].append(score)
    write_data([pair_dict, product_dict])
    for p in product_dict.values():print(sum_score(p))



if __name__ == '__main__':
    main()
