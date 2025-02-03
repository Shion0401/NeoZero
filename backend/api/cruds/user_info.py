# あらゆる操作
# routersのみで呼び出される

import sys
import models.models as models
import db as databases
import hashlib

sys.dont_write_bytecode = True


## UserRegister
async def UserRegister(user_name, user_email, user_password, user_comment):
    session = databases.create_new_session()
    user = models.User()
    user.name = user_name
    user.email = user_email
    # hash_sha256 = hashlib.sha256(user_password.encode())
    user.password = user_password
    if user_comment is not None:
        user.comment = user_comment
    session.add(user)
    session.commit()
    return 0

## GetCheckEmailDuplication
async def GetCheckEmailDuplication(user_email):
    session = databases.create_new_session()
    user = session.query(models.User).\
                filter(models.User.email == user_email).\
                first()           
    if user == None:
        return 0
    else:
        return -1

## GetConfirmConbination
async def GetConfirmConbination(user_email, user_password):
    # hash_sha256 = hashlib.sha256(user_password.encode())
    session = databases.create_new_session()
    user = session.query(models.User).\
                filter(models.User.email == user_email, 
                       models.User.password == user_password).\
                first()           
    if user == None:
        return -1
    else:
        return user.id
## GetcheckUser
async def CheckUser(user_id):
    session = databases.create_new_session()
    user = session.query(models.User).\
                filter(models.User.id == user_id).\
                first()           
    if user == None:
        return -1
    else:
        return 0
## GetPetInfo
def GetPetInfo(user_id):
    session = databases.create_new_session()
    user = session.query(models.User).\
                filter(models.User.id == user_id).\
                first()           
    if user == None:
        return -1
    return user.name, user.comment, user.image


## ChangeUserEmail
async def ChangeUserEmail(user_id, new_user_email):
    session = databases.create_new_session()
    user = session.query(models.User).\
                filter(models.User.id == user_id).\
                first()
    if user == None:
        return -1
    user.email = new_user_email
    session.commit()
    return 0


## ChangeUserPass
async def ChangeUserPass(user_id, new_user_password):
    session = databases.create_new_session()
    user = session.query(models.User).\
                filter(models.User.id == user_id).\
                first()
    if user == None:
        return -1
    user.password = new_user_password
    session.commit()
    return 0


## ChangePetInfo
async def ChangePetInfo(user_id, user_name, user_comment):
    session = databases.create_new_session()
    user = session.query(models.User).\
                filter(models.User.id == user_id).\
                first()
    if user == None:
        return -1
    if user_name is not None:
        user.name = user_name
    if user_comment is not None:
        user.comment = user_comment
    # if user_comment is not None:
    session.commit()
    return 0

## DeleteUserAccount
async def DeleteUserAccount(user_id):
    session = databases.create_new_session()
    user = session.query(models.User).\
                filter(models.User.id == user_id).\
                first()
    if user == None:
        return -1
    session.delete(user)
    session.commit()
    return 0


## 確認用
# def select_all_user():
#     session = databases.create_new_session()
#     user_list = session.query(models.User).\
#             all()
#     if user_list == None:
#         user_list = []
#     return user_list

