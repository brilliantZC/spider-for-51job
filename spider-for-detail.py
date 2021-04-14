# -*- coding = utf-8 -*-
# @Time : 2021/4/13 21:20
# @Author : brilliantZC
# @File : spider-for-detail.py
# @Software : PyCharm

# 用于爬取职位的详细信息，爬5k条用于制作词云

from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException
import time
import sqlite3  #进行SQLite数据库操作
from selenium.webdriver.chrome.options import Options

def getData(url):
    opt = Options()
    opt.add_argument("--headless")
    opt.add_argument("--disbale-gpu")
    web = Chrome(options=opt)  # 把参数配置设置在浏览器中，让其不显示浏览器
    web.get(url)
    datalist = []
    for i in range(2,50):
        time.sleep(2)
        data_list = web.find_elements_by_xpath('/html/body/div[2]/div[3]/div/div[2]/div[4]/div[1]/div')
        for line in data_list:
            data = []
            line.find_element_by_xpath('./a/p[1]').click()
            web.switch_to.window(web.window_handles[-1])
            try:
                job_detail = web.find_element_by_xpath('/html/body/div[3]/div[2]/div[3]/div[1]/div').text.strip().replace('\n', '').replace('\r', '')\
                    .replace('工作职责', '').replace('专业要求', '').replace('岗位职责','').replace('综合素质','').replace(':', '').replace('：', '').replace('"', '').replace('“','')\
                    .replace('1.','').replace('1、','').replace('2.','').replace('2、','').replace('3.','').replace('3、','').replace('4.','').replace('4、','').replace('5.','').replace('5、','')\
                    .replace('6.','').replace('6、','').replace('7.', '').replace('7、', '').replace('8.','').replace('8、','').replace('9.','').replace('9、','')
            except NoSuchElementException as e:
                job_detail = ""
            data.append(job_detail)
            datalist.append(data)
            # 关掉子窗口
            web.close()
            # 回到原来的窗口中
            web.switch_to.window(web.window_handles[0])

        web.find_element_by_xpath('//*[@id="jump_page"]').clear()
        web.find_element_by_xpath('//*[@id="jump_page"]').send_keys(i)
        web.find_element_by_xpath('/html/body/div[2]/div[3]/div/div[2]/div[4]/div[2]/div/div/div/span[4]').click()
    return datalist


def saveDataDB(datalist,dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            data[index] = '"'+data[index]+'"'
        sql = '''
            insert into jobdetail(
            job_detail)
            values(%s)''' % ",".join(data)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()

def init_db(dbpath):
    sql = '''
        create table jobdetail
        (
        id integer primary key autoincrement ,
        job_detail text
        )
    '''  # 创建数据表
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    url = 'https://search.51job.com/list/150200,000000,0000,01,9,99,+,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
    datalist = getData(url)
    dbpath = "jobDetail.db"
    saveDataDB(datalist, dbpath)






