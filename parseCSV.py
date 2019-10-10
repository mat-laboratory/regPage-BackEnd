import pymongo
import csv

# 连接数据库
client = pymongo.MongoClient("127.0.0.1", 27017)
db = client["mat"]
baseInfo = db["baseInfo"]


if __name__ == "__main__":
    with open("static/shell.csv", encoding="utf-8") as fp:
        # 读取csv文件
        csvReader = csv.reader(fp)
        infor = {}
        for line in csvReader:
            # 处理数据，构建json
            userid = line[0][:-1]
            name = line[1]
            userClass = line[2]
            infor = {
                "userid" : userid,
                "name" : name,
                "userClass" : userClass
            }
            print(userid, len(userid))
            # 插入数据
            baseInfo.insert_one(infor)