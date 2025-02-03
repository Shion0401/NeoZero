from fastapi import APIRouter, FastAPI, Depends, Path, HTTPException, Query, Response, UploadFile,File, Form
import models.models as models
from fastapi.middleware.cors import CORSMiddleware
import cruds.user_info as handle_db
import cruds.images as image_db
import cruds.user_post as userpost_db
import schemas.user_info as schema
import datetime
import uuid

app = FastAPI()
router = APIRouter()
app.include_router(router)

## UserRegister
@router.post(path="/userinfo/account/register")
async def UserRegister(data: schema.UserRegisterRequest):
    ## GetCheckEmailDuplication
    result = await handle_db.GetCheckEmailDuplication(data.email)
    if result == 0:
        result = await handle_db.UserRegister(data.name, data.email, data.password, data.comment)
        if result == 0:
            return 0
    return -1

## UserLogin
@router.post(path="/userinfo/account/login")
async def UserLogin(data: schema.UserLoginRequest):
    result = await handle_db.GetConfirmConbination(data.email, data.password)
    return result

## GetPetInfo
@router.get(path="/userinfo/info/pet")
async def GetPetInfo(user_id: str):
    result = handle_db.GetPetInfo(user_id)
    ###########
    if result == -1:
        return -1
    else:
        return {
            "name": result[0],
            "comment": result[1],
    }
    ###########
    # 成功していればGetIconを呼び出す
    # if result == -1:
    #     return -1
    # else:
    #     data = result
    #     icon = image_db.GetIcon(user_id)
    #     if icon == -1:
    #         return -1
    #     else:
    #         return {
    #             "name": data[0],
    #             "comment": data[1],
    #             "icon": icon
    #         }
    
## ChangeUserEmail
@router.put(path="/userinfo/email/change")
async def ChangeUserEmail(request: schema.EmailChangeRequest):
    result = await handle_db.GetConfirmConbination(request.email, request.password) 
    if result == -1:
        return result
    result = await handle_db.GetCheckEmailDuplication(request.new_email)
    if result == -1:
        return result
    # メールアドレス更新
    result = await handle_db.ChangeUserEmail(request.userid, request.new_email)
    return result
    
## ChangeUserPass
@router.put(path="/userinfo/pass/change")
async def ChangeUserPass(request: schema.PassChangeRequest):
    ## GetConfirmConbination
    result = await handle_db.GetConfirmConbination(request.email, request.password)
    if result == -1:
        return result
    # パスワード更新
    result = await handle_db.ChangeUserPass(request.userid, request.new_pass)
    return result
            
## ChangePetInfo 受け取るデータの型をフォームに変更
@router.put(path="/userinfo/info/change")
async def ChangePetInfo(
    user_id: str = Form(None), 
    user_name: str = Form(None), #Query(None), 
    user_comment: str = Form(None), 
    file: UploadFile = File(None)
    ):# user_icon: str = Query(None)変更
    # return "test"
    try:
        # そもそもユーザーがいるか判定
        user_exists = handle_db.CheckUser(user_id)
        if user_exists == None:
            return {"error": f"ユーザーがいません"}
        else:
            # ファイルがあるか
            #if file:
            #    file_content = await file.read()
            #    # ファイルがアップロードされている時
            #    if not file_content is None:
            #    # iconのURLを取得
            #        icon_url = await image_db.GetIcon(user_id)
            #    # ユーザーアイコンがある時，削除　 # 投稿削除のやつで代用
            #        if not icon_url is None:
            #            image_db.DeletePostImageas3(icon_url)
            #    # アイコンを変更する
            #        file_url = await image_db.ChangeIcon(file_content,file.content_type,file.filename)
            #        result = await handle_db.ChangePetInfo(user_id, user_name, user_comment, file_url)
            #else:
            result = await handle_db.ChangePetInfo(user_id, user_name, user_comment)  # アイコンは変更しない
            return  result
    except Exception as e:
        return {"error": str(e)}
    # return result
    #####
    # 成功したらChangeIconも
    # if result == -1:
    #     return result
    # icon = image_db.ChangeIcon(user_id, user_icon)
    # return result  

## DeleteUserAccount
@router.delete(path="/userinfo/account/delete/{user_id}")
async def DeleteUserAccount(user_id: str, user_email: str, user_password: str):
    ## GetConfirmConbination
    result = await handle_db.GetConfirmConbination(user_email, user_password)
    if result == -1:
        return result
    # 最初にs3から画像を削除する
    # GetOnesPostをよぶ 投稿がない場合，処理されない
    result = await userpost_db.GetOnesPost(user_id)
    if not result is None:
        posts = [
            {
                "title": post.title,
                "caption": post.caption,
                "goodcount": post.goodcount,
                "postid": post.image
            }
            for post in result
        ]
        images = [post["image"] for post in posts if "image" in post]
        # s3からすべての投稿画像を削除
        await image_db.DeletePostImageAlls3(images)
        # テーブルから投稿を削除
        await userpost_db.DeletePostAll(user_id)
    # DeletIconを呼び出す 
    icon_exitst =  handle_db.GetPetInfo(user_id)
    # iconが存在しない場合，削除処理をスキップ
    if not icon_exitst["image"] is None:
       result = await image_db.DeletePostImageas3(images)
       if result == -1:
           return "hoge"    
    if result == -1:
        return result
    result = await handle_db.DeleteUserAccount(user_id)
    return  result

