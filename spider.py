# -*- coding = utf-8 -*-
# @Time : 2021/4/12 16:11
# @Author : brilliantZC
# @File : spider.py
# @Software : PyCharm

# 爬虫程序，用于爬取51job上的合肥城市IT工作的1w条数据

from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException
import xlwt  # 进行excel操作
import time
import sqlite3  #进行SQLite数据库操作

def getData(url):
    web = Chrome()
    web.get(url)
    datalist = []
    for i in range(2,201):
        time.sleep(2)
        data_list = web.find_elements_by_xpath('/html/body/div[2]/div[3]/div/div[2]/div[4]/div[1]/div')
        for line in data_list:
            data = []
            job_name = line.find_element_by_xpath('./a/p[1]/span[1]').text
            data.append(job_name)  # 工作名

            job_price = line.find_element_by_xpath('./a/p[2]/span[1]').text
            data.append(job_price)  # 工资

            # 这里数据不完整，需要处理
            if len(line.find_element_by_xpath('./a/p[2]/span[2]').text.split('|')) == 2:
                job_address = line.find_element_by_xpath('./a/p[2]/span[2]').text.split('|')[0].strip()
                data.append(job_address)  # 工作地点
                job_age = ""
                data.append(job_age)

                job_education = ""
                data.append(job_education)

                job_num = line.find_element_by_xpath('./a/p[2]/span[2]').text.split('|')[1].strip()
                data.append(job_num)  # 招人数

            elif len(line.find_element_by_xpath('./a/p[2]/span[2]').text.split('|')) == 3:
                job_address = line.find_element_by_xpath('./a/p[2]/span[2]').text.split('|')[0].strip()
                data.append(job_address)  # 工作地点

                job_age = ""
                data.append(job_age)

                job_education = line.find_element_by_xpath('./a/p[2]/span[2]').text.split('|')[1].strip()
                data.append(job_education)  # 工作学历

                job_num = line.find_element_by_xpath('./a/p[2]/span[2]').text.split('|')[2].strip()
                data.append(job_num)  # 招人数

            else:
                job_address = line.find_element_by_xpath('./a/p[2]/span[2]').text.split('|')[0].strip()
                data.append(job_address)  # 工作地点

                job_age = line.find_element_by_xpath('./a/p[2]/span[2]').text.split('|')[1].strip()
                data.append(job_age)  # 工作经验

                job_education = line.find_element_by_xpath('./a/p[2]/span[2]').text.split('|')[2].strip()
                data.append(job_education)  # 工作学历

                job_num = line.find_element_by_xpath('./a/p[2]/span[2]').text.split('|')[3].strip()
                data.append(job_num)  # 招人数

            try:
                 job_welfare = line.find_element_by_xpath('./a/p[3]/span').text.strip().replace('\n', ',').replace('\r', '').replace(',...', '')
            except NoSuchElementException as e:
                 job_welfare = ""
            data.append(job_welfare)  # 福利

            job_company = line.find_element_by_xpath('./div[2]/a').text
            data.append(job_company)  # 公司名

            job_catacom = line.find_element_by_xpath('./div[2]/p[1]').text
            data.append(job_catacom)  # 公司类别

            job_classify = line.find_element_by_xpath('./div[2]/p[2]').text
            data.append(job_classify)  # 工作类别

            datalist.append(data)
        web.find_element_by_xpath('//*[@id="jump_page"]').clear()
        web.find_element_by_xpath('//*[@id="jump_page"]').send_keys(i)
        web.find_element_by_xpath('/html/body/div[2]/div[3]/div/div[2]/div[4]/div[2]/div/div/div/span[4]').click()
    return datalist

def savaDataExcel(list,savepath):
    book = xlwt.Workbook(encoding="utf-8")  # 创建wookbook对象
    sheet = book.add_sheet("合肥IT工作", cell_overwrite_ok=True)
    col = ("工作名", "工资", "工作地点", "工作经验", "要求学历", "招聘人数", "福利待遇", "公司名", "公司类别", "工作类别")
    for i in range(0, 10):
        sheet.write(0, i, col[i])
    for i in range(0, 10000):
        data = list[i]
        for j in range(0, 10):
            sheet.write(i + 1, j, data[j])

    book.save(savepath)  # 保存

def saveDataDB(datalist,dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            data[index] = '"'+data[index]+'"'
        sql = '''
            insert into jobinfo(
            job_name,job_price,job_address,job_age,job_education,job_num,job_welfare,job_company,job_catacom,job_classify)
            values(%s)''' % ",".join(data)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()

def init_db(dbpath):
    sql = '''
        create table jobinfo
        (
        id integer primary key autoincrement ,
        job_name varchar ,
        job_price varchar ,
        job_address varchar ,
        job_age varchar ,
        job_education numeric ,
        job_num numeric ,
        job_welfare varchar,
        job_company varchar,
        job_catacom varchar,
        job_classify varchar
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
    # 拿9950条数据，跑
    # savePath = "合肥IT工作—51job.xls"
    # savaDataExcel(datalist, savePath)
    dbpath = "job.db"
    saveDataDB(datalist, dbpath)




