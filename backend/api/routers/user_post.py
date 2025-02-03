from fastapi import APIRouter, FastAPI, Depends, Path, HTTPException, Query,UploadFile,File,Form
import models.models as models
from fastapi.middleware.cors import CORSMiddleware
import cruds.images as image_db
import cruds.user_post as handle_db
import datetime
import time
import uuid


# aws s3
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# boto3の変数定義
BUCKET_NAME = "neozero"
REGION_NAME = "us-east-1"
s3_client = boto3.client(
    "s3", 
    region_name=REGION_NAME)


app = FastAPI()
router = APIRouter()


## Post  切り取ったやつ　image: str, 
@router.post(path="/post")
async def Post(user_id: str = Form(None), title: str = Form(None), caption: str = Form(None),file:UploadFile = File(...)):
    print(f"Received user_id: {user_id}")  # ここでuser_idの値を確認
    print(f"Received titile: {title}")  # ここでuser_idの値を確認
    print(f"Received caption: {caption}")  # ここでuser_idの値を確認

    try:
        # # ファイル読み取り
        file_content = await file.read()
        # UUIDを作成する．
        timestanp = int(time.time())
        unique_id = uuid.uuid4()
        # S3のファイル識別子
        s3_key = f"{timestanp}_{unique_id}/{file.filename}",

        # S3のファイルURLをつくる
        file_url = f"https://{BUCKET_NAME}.s3.{REGION_NAME}.amazonaws.com/{s3_key}",

        # 以下の2行はデバック用　returnで内容確認
        title = title,
        caption = caption,

        # 関数呼び出し
        # image_db.InsertPostImage(file_content,file.filename,file.content_type,s3_key)
        file_url = await image_db.InsertPostImage(file_content,file.content_type,file.filename)
        postid = handle_db.Post(user_id, title, caption, file_url)
        return {
            #"result" : result,
            "message": "アップロード成功",
            "file_url": s3_key,
            "title": title,
            "caption": caption,
        }
    except (BotoCoreError, ClientError) as e:
        return {
            "error": f"アップロード失敗: {str(e)}",
           # "result": result,
            "postid": postid
            }
    
    # if postid == -1:
    #     return -1
    # InsertPostImageを呼び出す
    # result = image_db.InsertPostImage(postid, image)
    # return result

## GetOnesPost
@router.get(path="/post/get/{user_id}")
async def GetOnesPost(user_id: str):
    print("routers GetO",user_id)
    result = await handle_db.GetOnesPost(user_id)
    return result
    # posts = [
    #     {
    #         "postId":post.id,
    #         "title": post.title,
    #         "caption": post.caption,
    #         "goodcount": post.goodcount,
    #         "postimage": post.image
    #     }
    #     for post in result
    # ]
    # return {"posts": posts}
    # GetPostImageを呼び出す
    # if result == -1:
    #     return -1
    # posts = [
    #     {
    #         "title": post.title,
    #         "caption": post.caption,
    #         "goodcount": post.goodcount,
    #         "image": image_db.GetPostImage(post.image)
    #     }
    #     for post in result
    # ]
    # return {"posts": posts}
 
## GetNewPost
@router.get(path="/post/new")
async def GetNewPost():
    result = await handle_db.GetNewPost()
    if result == -1:
        return -1
    posts = [
        {
            "id":post.id,
            "userid": post.user_id,
            "caption": post.caption,
            "goodcount": post.goodcount,
            "postid": post.image
        }
        for post in result
    ]
    return {"posts": posts}
    # GetPostImageを呼び出す
    # if result == -1:
    #     return -1
    # posts = [
    #     {
    #         "title": post.title,
    #         "caption": post.caption,
    #         "goodcount": post.goodcount,
    #         "image": image_db.GetPostImage(post.image)
    #     }
    #     for post in result
    # ]

 

## DeletePost 
@router.delete(path="/post/delete")
async def DeletePost(post_id: str = Query(...)):#user_id: str, 
    print(post_id)
    # DeletePostImageを呼び出す
    # result = await image_db.DeletePostImage(user_id, post_id)
    # if result == -1:
    #     return -1
    result = await handle_db.DeletePost(post_id)#user_id, 
    return result

# GoodCount
# @router.get(path="/post/goodcount/{post_id}")
# async def GoodCount(post_id: str):
#     result = await handle_db.GoodCount(post_id)
#     return result

## Good
# @router.put(path="/post/good/{post_id}")
# async def Good(post_id: str):
#     result = await handle_db.Good(post_id)
#     return result
