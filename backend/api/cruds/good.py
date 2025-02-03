import sys
import models.models as models
import db as databases

sys.dont_write_bytecode = True

## GetConfirmConbination
async def GetConfirmConbination(userid, postid):
    session = databases.create_new_session()
    user_exists = session.query(models.User).\
                    filter(models.User.id == userid).\
                    first()
    post_exists = session.query(models.Post).\
                    filter(models.Post.id == postid).\
                    first()
    if not user_exists or not post_exists:
        return -1
    good = session.query(models.Good).\
                filter(models.Good.user_id == userid, 
                       models.Good.post_id == postid).\
                first()           
    if good == None:
        return "None"
    else:
        return good.flag
    
## Good
async def Good(userid, postid):
    session = databases.create_new_session()
    good = models.Good()
    good.user_id = userid
    good.post_id = postid
    good.flag = 1
    session.add(good)
    #session.commit()
    return 0

## ChangeFlag（0:いいね解除中, 1:いいね中）
async def ChangeFlag(userid, postid):
    session = databases.create_new_session()
    good = session.query(models.Good).\
                filter(models.Good.user_id == userid, 
                       models.Good.post_id == postid).\
                first()
    if good == None:
        return -1 
    else:
        good.flag = not good.flag
    session.commit()
    return good.flag

# ## Gooddelete
# async def Gooddelete(userid, postid):
#     session = databases.create_new_session()
#     good = session.query(models.Good).\
#                 filter(models.Good.user_id == userid, 
#                        models.Good.post_id == postid).\
#                 first()
#     if good == None:
#         return 0
#     session.delete(good)
#     session.commit()
#     return good.flag

async def GoodStatus(userid, postid):
    session = databases.create_new_session()
    good = session.query(models.Good).\
                filter(models.Good.user_id == userid, 
                       models.Good.post_id == postid).\
                first()
    if good == None:
        return 0
    return good.flag
