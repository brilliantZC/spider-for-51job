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

@app.route('/score')
def showscore():
    score = [] # 评分
    num = []   # 评分的电影数
    conn = sqlite3.connect("movie.db")
    cur = conn.cursor()
    sql = "select score,count(score) from movie250 group by score"
    data = cur.execute(sql)
    for item in data:
        score.append(item[0])
        num.append(item[1])
    cur.close()
    conn.close()
    return render_template("score.html", score=score, num=num)

@app.route('/word')
def showword():
    return render_template("word.html")

@app.route('/team')
def showteam():
    return render_template("team.html")

if __name__ == '__main__':
    app.run()
