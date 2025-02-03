import sys
import models.models as models
import db as databases

import datetime

# aws s3
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# boto3の変数定義　これグローバル変数にしたい
BUCKET_NAME = "neozero"
REGION_NAME = "us-east-1"
s3_client = boto3.client(
    "s3", 
    region_name=REGION_NAME)

sys.dont_write_bytecode = True


## Post
def Post(user_id, title, caption, file_url):
    session = databases.create_new_session()
    post = models.Post()
    if title is not None:
        post.title = title
    if caption is not None:
        post.caption = caption
    if caption is not None:
        post.image = file_url # ファイルURLの設定
    post.create_date_time = datetime.datetime.now()
    post.user_id = user_id  # user_idの設定
    post.goodcount = 0  # 初期値の設定（オプショナル）

    session.add(post)
    session.commit()
    return 0

## GetOnesPost 特定のユーザーの投稿を取得
async def GetOnesPost(user_id):
    session = databases.create_new_session()
    posts = session.query(models.Post).\
                filter(models.Post.user_id == user_id).\
                order_by(models.Post.create_date_time.desc()).\
                limit(10).\
                all()         
    if posts == None:
        posts = -1
##あとで分ける必要あり，ユーザーを消すときと投稿情報を取得する時に呼び出されるので
    # 各投稿について画像URLを取得し、S3から画像を取得
    for post in posts:
        image_url = post.image  # 投稿に関連する画像URL
        if image_url == None:
         continue
        # 画像URLがS3のURL形式である場合
        elif image_url.startswith('https://s3.amazonaws.com/'):
            # S3から画像を取得
            bucket_name = BUCKET_NAME  # 実際のバケット名
            file_key = image_url.split('/')[-1]  # URLからファイル名を取得
            # # S3オブジェクトの取得
            # try:
            #     s3_response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
            #     image_data = s3_response['Body'].read()
            #     # バイナリから変換する　画像のデータをそのままフロントに返す
            #     base64_image_data = base64.b64encode(image_data).decode('utf-8')
            # except ClientError as e:
            #     s3_response = -1
    
    return posts

## GetNewPost　新着順で全体の投稿を取得
async def GetNewPost():
    session = databases.create_new_session()
    posts = session.query(models.Post).\
                order_by(models.Post.create_date_time.desc()).\
                limit(10).\
                all()  
    if posts == None:
        posts = -1
    # 各投稿について画像URLを取得し、S3から画像を取得
    results = []
    for post in posts:
        image_url = post.image  # 投稿に関連する画像URL
        if image_url == None:
         continue
        # 画像URLがS3のURL形式である場合
        elif image_url.startswith('https://s3.amazonaws.com/'):
            # S3から画像を取得
            bucket_name = BUCKET_NAME  # 実際のバケット名
            file_key = image_url.split('/')[-1]  # URLからファイル名を取得
            # # S3オブジェクトの取得
            # try:
            #     s3_response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
            #     image_data = s3_response['Body'].read()
            #     # バイナリから変換する　画像のデータをそのままフロントに返す
            #     base64_image_data = base64.b64encode(image_data).decode('utf-8')
            # except ClientError as e:
            #     s3_response = -1
        
        # usernameも取得し、必要な情報だけを配列で返す 
        user = session.query(models.User).\
                filter(models.User.id == post.user_id).\
                first()  
        post_data = {
                "id": post.id,
                "comment": post.caption,
                "userid": post.user_id,
                "image": base64_image_data,  # わからんけど多分こう？
                "name": user.name  # ユーザー名
        }
        results.append(post_data)
    return results # base64_image_data

## DeletePost １つの投稿を削除
async def DeletePost(post_id):#user_id, #models.Post.user_id == user_id, 
    session = databases.create_new_session()
    post = session.query(models.Post).\
                filter(models.Post.id == post_id).\
                first()
    if post == None:
        return -1
    #DeletePostimg

    session.delete(post)
    session.commit()
    return 0

## DeletePostAll　すべての投稿を削除
async def DeletePostAll(user_id):
    session = databases.create_new_session()
    try:
        # ユーザーIDに紐づく投稿をすべて取得
        posts = session.query(models.Post).filter(models.Post.user_id == user_id).all()
        # 投稿が存在しない場合の処理
        if not posts:
            return -1  # または、適切なエラーメッセージや例外をスローする
        # 画像をS3から削除

        # 各投稿を削除
        for post in posts:
            session.delete(post)
        # コミット
        session.commit()
        return 0  # 処理成功
    finally:
        # セッションを閉じる
        session.close()

## GoodCount
async def GoodCount(post_id):
    session = databases.create_new_session()
    post = session.query(models.Post).\
                filter(models.Post.id == post_id).\
                first()         
    if post == None:
        post = -1
    return post.goodcount
    
    
## Good
async def Good(post_id):
    session = databases.create_new_session()
    post = session.query(models.Post).\
                filter(models.Post.id == post_id).\
                first()
    if post == None:
        return -1
    post.goodcount += 1
    session.commit()
    return 0

## DeletePost
async def DeletePost(post_id):#user_id,
    session = databases.create_new_session()
    post = session.query(models.Post).\
                filter(models.Post.id == post_id).\
                first()#models.Post.user_id == user_id,
    if post == None:
        return -1
    session.delete(post)
    session.commit()
    return 0