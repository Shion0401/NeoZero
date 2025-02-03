import sys
import models.models as models
import db as databases

import datetime

sys.dont_write_bytecode = True


## GetReport
async def GetReport():#user_id
#     #�@���������C���J���m�F����D
#     # session = databases.create_new_session()
#     # user_exists = session.query(models.User).\
#     #                 filter(models.User.id == user_id).\
#     #                 first()
#     # if user_exists == None:

#     #####�������炵�������񏑂����Ƃ���######
    session = databases.create_new_session()

    # Report��User���������āAUser.name��Report.user_id�Ɋ�Â��Ď擾
    reports = session.query(models.Report).\
        options(joinedload(models.Report.user)).\
        order_by(models.Report.times.desc()).\
        limit(5).\
        all()

    results = []  # �ԋp�p���X�g

    # ���|�[�g�������X�g�ɒǉ�
    for report in reports:
        email = report.user.email
        user_id = report.user.id
        user_name = report.user.name  # User�e�[�u����name���擾
        report_count = report.times   # Report�e�[�u����times���擾
        update_date_time = report.update_date_time.isoformat()  # Report�̍X�V����
        
        report_data = {
            "email": email,
            "user_id" : user_id,
            "user_name": user_name,
            "report_count": report_count,
            "update_date_time": update_date_time,
        }

        results.append(report_data)

    return results  # ���ʂ����X�g�`���ŕԋp

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
