# 去除mongoDB返回的id
def popMongoID(mongoJSON):
    resultJSON = [s.copy() for s in mongoJSON]
    for r in resultJSON:
        r.pop("_id")
    return resultJSON