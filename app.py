from flask import Flask, request, jsonify, render_template, url_for, redirect
import config
import pymongo
from tools import popMongoID

client = pymongo.MongoClient("127.0.0.1", 27017)
dbMat = client["mat"]
userSet = dbMat["user"]
baseInfo = dbMat["baseInfo"]

app = Flask(__name__)
app.config.from_object("config")


@app.route('/')
def hello_world():
    return redirect(url_for("signUp"))

# 注册界面
@app.route('/sign', methods = ["GET", "POST"])
def signUp():
    if request.method == "POST":
        # 获取前端表单数据
        userid = request.form.get("userid")
        # 判断是否是19级学生
        base = baseInfo.find_one({"userid" : userid})
        if base == None:
            msg = {
                "message" : "学号无效，请重新输入嗷~",
                "code" : "-1"
            }
            return jsonify(msg)

        # 判断是否已报名
        exist = userSet.find_one({"userid" : userid})
        if exist:
            msg = {
                "message" : "该同学已经报名了嗷~",
                "code" : "0"
            }
            return jsonify(msg)

        subject = request.form.get("subject")      

        infor = {
            "userid" : userid,
            "subject" : subject,
            "name" : base["name"],
            "userClass" : base["userClass"]
        }
        # 获取表中所有数据数量
        preDocment = userSet.count_documents({})
        # 插入数据
        userSet.insert_one(infor)
        # 获取当前数据量
        curDocument = userSet.count_documents({})
        # 插入成功
        if curDocument > preDocment :
            msg = {
                "message" : "注册成功！",
                "name" : base["name"],
                "userClass" : base["userClass"],
                "code" : "1"
            }
            return jsonify(msg)
        # 插入失败
        else :
            msg = {
                "message" : "注册失败！",
                "code" : "-2"
            }
            return jsonify(msg)
    elif(request.method == "GET"): 
        return render_template("index.html")


# 获取数据库中所有用户
@app.route("/student", methods = ["GET", "POST"])
def studentInfor():
    if request.method == "GET":
        return render_template("succss.html")
    elif request.method == "POST":
        # 获取数据库所有内容
        mongoJSON = userSet.find({})
        # 剔除mongodb中的自带`_id`
        result = popMongoID(mongoJSON)
        if len(result) != 0:
            msg = {
                "message" : "获取数据成功！",
                "code" : "1",
                "data" : result
            }
            return jsonify(msg)
        else:
            msg = {
                "message" : "获取数据失败！",
                "code" : "0"
            }
            return jsonify(msg)


if __name__ == '__main__':
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run(host = "127.0.0.1",
            port = 8000)
