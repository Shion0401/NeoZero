# しおんちゃんここかいて〜
import sys
import models.models as models
import db as databases

import datetime
import time
import uuid

from fastapi import APIRouter, FastAPI, Depends, Path, HTTPException, Query, UploadFile,File
import models.models as models
from fastapi.middleware.cors import CORSMiddleware
#import api.cruds.images as image_db
import cruds.user_post as handle_db
import datetime
# aws s3 
import boto3
from botocore.exceptions import BotoCoreError, ClientError

sys.dont_write_bytecode = True


# boto3の変数定義
BUCKET_NAME = "neozero"
REGION_NAME = "us-east-1"
s3_client = boto3.client(
    "s3", 
    region_name=REGION_NAME)


app = FastAPI()
router = APIRouter()


## user_info
# InsertIcon バケット分ける？ 
# GetIcon ユーザーアイコンのURLを取得，返す
async def GetIcon(user_id):
    session = databases.create_new_session()
    user = session.query(models.User).\
                filter(models.User.id == user_id).\
                first()
    if user == None:
        return None
    # return user.image
    # # データベースとのセッション確立
    session = databases.create_new_session()
    # 投稿IDをテーブルから取得
    #　各投稿についてURLを取得，
    # 各投稿について画像URLを取得し、S3から画像を取得
    for post in posts:
        image_url = post.postid  # 投稿に関連する画像URL

        # 画像URLがS3のURL形式である場合
        if image_url.startswith('https://s3.amazonaws.com/'):
            # S3から画像を取得
            bucket_name = BUCKET_NAME  # 実際のバケット名
            file_key = image_url.split('/')[-1]  # URLからファイル名を取得

            # # S3オブジェクトの取得
            try:
                s3_response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
                image_data = s3_response['Body'].read()
                return image_data

            except Exception as e:
                print(f"Error fetching image from S3: {e}")

# ChangeIcon
async def ChangeIcon(file_content,contenttype,filename,s3_key):
    try:
        # S3にアップロード        
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=file_content,
            ContentType=contenttype
        )
        return {
            #"result" : result,
            # "message": "アップロード成功",
            file_url
        }
    except (BotoCoreError, ClientError) as e:
        return {
            "error": f"changepetInfo:アップロード失敗: {str(e)}",
            }

# DeleteIcon(useridからimageをとってくる必要がある) 

## user_post
# DeleteOnePostImg ある投稿の画像を削除する関数 今はアイコンを消すときもこれを呼び出している
async def DeletePostImageas3(image):
    session = databases.create_new_session()
    # return {"images": images}

    # # 以下，オブジェクトを削除
    # posts = image
    # return {
    #     "images": image, 
    #     "posts": posts
    #     }

    response = s3_client.delete_object(Bucket=BUCKET_NAME, Delete={'Objects': objects_to_delete})

    # 削除成功時のレスポンス
    if response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 204:
        print(f"Object deleted successfully.")
    else:
        print(f"Failed to delete object.")
        posts = session.query(models.Post).\
                filter(models.Post.user_id == user_id).\
                order_by(models.Post.create_date_time.desc()).\
                all()   
    return posts

# DeletePostImageAll　ユーザーが退会した際に，すべての投稿の画像を消す関数
async def DeletePostImageAlls3(images: list):
    session = databases.create_new_session()
    # return {"images": images}

# オブジェクトを削除　今はurlを表示しているだけ．
    objects_to_delete = [images]
    # posts = [
    #     {
    #       "image_url": objects_to_delete
    #     }
    # ]
    response = s3_client.delete_object(Bucket=BUCKET_NAME, Delete={'Objects': objects_to_delete})
# 削除成功時のレスポンス
    if response.get('ResponseMetadata', {}).get('HTTPStatusCode') == 204:
        print(f"Object deleted successfully.")
    else:
        print(f"Failed to delete object.")
        posts = session.query(models.Post).\
                filter(models.Post.user_id == user_id).\
                order_by(models.Post.create_date_time.desc()).\
                all()
    
    return posts
    # return {
    #     "images": objects_to_delete, 
    #     "posts": posts
    #     }



# InsertPostImage　投稿した画像をs3にアップロードする関数
async def InsertPostImage(file_content,contenttype,s3_key):
    try:
        # S3にアップロード        
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=file_content,
            ContentType=contenttype
        )
        return {
            # "file_url":file_url
        }
    except (BotoCoreError, ClientError) as e:
        return {
            "error": f"changepetInfo:アップロード失敗: {str(e)}",
            }

async def GetPostImg(post_id):
    # データベースとのセッション確立
    session = databases.create_new_session()
    
    # 投稿IDに関連する投稿情報を取得（例：DBからpostを取得）
    # 例：posts = session.query(Post).filter_by(post_id=post_id).all() など
    posts = get_posts_from_db(post_id)  # 実際の投稿取得処理を実装
    
    # 投稿の各画像URLを取得
    for post in posts:
        image_url = post.postid  # 投稿に関連する画像URL
        
        # 画像URLがS3のURL形式である場合
        if image_url.startswith('https://s3.amazonaws.com/'):
            # S3から画像を取得
            bucket_name = BUCKET_NAME  # 実際のバケット名
            file_key = image_url.split('/')[-1]  # URLからファイル名を取得

            # # S3オブジェクトの取得
            try:
                s3_response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
                image_data = s3_response['Body'].read()

                # 画像データをBase64エンコード
                base64_image = base64.b64encode(image_data).decode('utf-8')

                # Base64エンコードされた画像データを返す
                return {"image_base64": base64_image}

            except ClientError as e:
                print(f"Error fetching image from S3: {e}")
                return {"error": "Failed to fetch image from S3."}

    
# GetPostImage　画像のURLを取得
async def GetPostImgURL(post_id):
    # データベースとのセッション確立
    session = databases.create_new_session()
    image = session.query(models.Post).\
                filter(models.Post.id == post_id).\
                first()
    if image == None:
        return -1
    return image
# ChangeAdImage
# DeleteAdImage
# InsertAdImage
# GetAdImage
