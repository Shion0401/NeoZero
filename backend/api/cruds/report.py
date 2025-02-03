import sys
import models.models as models
import db as databases

import datetime

sys.dont_write_bytecode = True


## GetReport
async def GetReport():#user_id
#     #　そもそもイルカを確認する．
#     # session = databases.create_new_session()
#     # user_exists = session.query(models.User).\
#     #                 filter(models.User.id == user_id).\
#     #                 first()
#     # if user_exists == None:

#     #####ここからしおおおん書いたところ######
    session = databases.create_new_session()

    # ReportとUserを結合して、User.nameをReport.user_idに基づいて取得
    reports = session.query(models.Report).\
        options(joinedload(models.Report.user)).\
        order_by(models.Report.times.desc()).\
        limit(5).\
        all()

    results = []  # 返却用リスト

    # レポート情報をリストに追加
    for report in reports:
        email = report.user.email
        user_id = report.user.id
        user_name = report.user.name  # Userテーブルのnameを取得
        report_count = report.times   # Reportテーブルのtimesを取得
        update_date_time = report.update_date_time.isoformat()  # Reportの更新日時
        
        report_data = {
            "email": email,
            "user_id" : user_id,
            "user_name": user_name,
            "report_count": report_count,
            "update_date_time": update_date_time,
        }

        results.append(report_data)

    return results  # 結果をリスト形式で返却

## InsertReport
async def InsertReport(user_id):
    session = databases.create_new_session()
    report = models.Report()
    report.times = 1
    report.update_date_time = datetime.datetime.now()
    report.user_id = user_id
    session.add(report)
    session.commit()
    return 0
    
    
## UpdateReport
async def UpdateReport(user_id):
    session = databases.create_new_session()
    report = session.query(models.Report).\
                filter(models.Report.user_id == user_id).\
                first()
    if report == None:
        return -1
    report.times += 1
    report.update_date_time = datetime.datetime.now()
    session.commit()
    return 0

    
## DeleteReport
def DeleteReport(user_id):
    session = databases.create_new_session()
    report = session.query(models.Report).\
                filter(models.Report.user_id == user_id).\
                first()
    if report == None:
        return -1
    session.delete(report)
    session.commit()
    return 0
    
async def ReportPost(postid):
    session = databases.create_new_session()
    post = session.query(models.Post).\
                    filter(models.Post.id == postid).\
                    first()   
    user = session.query(models.User).\
                    filter(models.User.id == post.user_id).\
                    first()               
    if post == None:
        return -1
    else:
        return {
           "posts":[
            {
            "name": user.name,
            "comment": post.caption,
            "image": post.image,
            "reportuserid":user.id
            }
            ]
    }
