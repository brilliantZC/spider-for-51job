from flask import Flask,render_template,request
import sqlite3
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/index')
def home():
    return render_template("index.html")


@app.route('/job_detail_first')
def showjob_detail_first():
    datalist = []
    conn = sqlite3.connect("job.db")
    cur = conn.cursor()
    sql = "select * from jobinfo where id BETWEEN 1 and 50"
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    cur.close()
    conn.close()
    return render_template("job_detail.html", datalist=datalist)

@app.route('/showjob_detail_then',methods=['POST','GET'])
def showjob_detail_then():
    if request.method == 'POST':
        result = request.form
        apage = int(result.get('page'))
        i = apage*50+1
        j = apage*50+50
        print(i,j)
    datalist = []
    conn = sqlite3.connect("job.db")
    cur = conn.cursor()
    sql = "select * from jobinfo where id BETWEEN '{}' and '{}'".format(i,j)
    data = cur.execute(sql)
    for item in data:
        datalist.append(item)
    cur.close()
    conn.close()
    return render_template("job_detail.html",datalist=datalist)

@app.route('/job_pic')
def showjob_pic():
    job_classify = []
    num = []
    education_dic = {}
    campany = []
    cnum = []
    conn = sqlite3.connect("job.db")
    cur = conn.cursor()
    sql1 = "select count(job_name) from jobinfo where job_name like '%Java%'"
    sql2 = "select count(job_name) from jobinfo where job_name like '%Python%'"
    sql3 = "select count(job_name) from jobinfo where job_name like '%NET%' "
    sql4 = "select count(job_name) from jobinfo where job_name like '%Android%' "
    sql5 = "select count(job_name) from jobinfo where job_name like '%C++%' "
    sql6 = "select count(job_name) from jobinfo where job_name like '%C语言%' "
    sql7 = "select count(job_name) from jobinfo where job_name like '%C#%' "
    sql8 = "select count(job_name) from jobinfo where job_name like '%PHP%' "
    sql9 = "select count(job_education) from jobinfo where job_education like '%硕士%'"
    sql10 = "select count(job_education) from jobinfo where job_education like '%本科%'"
    sql11 = "select count(job_education) from jobinfo where job_education like '%大专%'"
    sql12 = "select count(job_education) from jobinfo where job_education like '%中专%'"
    sql13 = "select count(job_education) from jobinfo where job_education like '%高中%'"
    sql14 = "select count(job_education) from jobinfo where job_education like '%初中%'"
    sql15 = "select count(job_catacom) from jobinfo where job_catacom like '%上市公司%'"
    sql16 = "select count(job_catacom) from jobinfo where job_catacom like '%民营公司%'"
    sql17 = "select count(job_catacom) from jobinfo where job_catacom like '%合资%'"
    sql18 = "select count(job_catacom) from jobinfo where job_catacom like '%国企%'"
    sql19 = "select count(job_catacom) from jobinfo where job_catacom like '%外资%'"
    sql20 = "select count(job_catacom) from jobinfo where job_catacom like '%创业公司%'"
    data = cur.execute(sql1)
    for item in data:
        job_classify.append('Java')
        num.append(item[0])
    data = cur.execute(sql2)
    for item in data:
        job_classify.append('Python')
        num.append(item[0])
    data = cur.execute(sql3)
    for item in data:
        job_classify.append('.NET')
        num.append(item[0])
    data = cur.execute(sql4)
    for item in data:
        job_classify.append('Android')
        num.append(item[0])
    data = cur.execute(sql5)
    for item in data:
        job_classify.append('C++')
        num.append(item[0])
    data = cur.execute(sql6)
    for item in data:
        job_classify.append('C')
        num.append(item[0])
    data = cur.execute(sql7)
    for item in data:
        job_classify.append('C#')
        num.append(item[0])
    data = cur.execute(sql8)
    for item in data:
        job_classify.append('PHP')
        num.append(item[0])
    data = cur.execute(sql9)
    for item in data:
        education_dic['硕士'] = item[0]
    data = cur.execute(sql10)
    for item in data:
        education_dic['本科'] = item[0]
    data = cur.execute(sql11)
    for item in data:
        education_dic['大专'] = item[0]
    data = cur.execute(sql12)
    for item in data:
        education_dic['中专'] = item[0]
    data = cur.execute(sql13)
    for item in data:
        education_dic['高中'] = item[0]
    data = cur.execute(sql14)
    for item in data:
        education_dic['初中'] = item[0]
    data = cur.execute(sql15)
    for item in data:
        campany.append('上市公司')
        cnum.append(item[0])
    data = cur.execute(sql16)
    for item in data:
        campany.append('民营公司')
        cnum.append(item[0])
    data = cur.execute(sql17)
    for item in data:
        campany.append('合资')
        cnum.append(item[0])
    data = cur.execute(sql18)
    for item in data:
        campany.append('国企')
        cnum.append(item[0])
    data = cur.execute(sql19)
    for item in data:
        campany.append('外资')
        cnum.append(item[0])
    data = cur.execute(sql20)
    for item in data:
        campany.append('创业公司')
        cnum.append(item[0])
    cur.close()
    conn.close()
    return render_template("job_pic.html", job_classify=job_classify, num=num,education_dic=education_dic,campany=campany,cnum=cnum)

@app.route('/word')
def showword():
    return render_template("word.html")

@app.route('/team')
def showteam():
    return render_template("team.html")

if __name__ == '__main__':
    app.run()
