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
    # ロギングを有効化
    print(user_id)  # デバッグ用: リクエストデータを確認
    # logging.basicConfig()
    # logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    # engine = create_engine("mysql+pymysql://user:password@host/dbname")
    # logging.debug(f"user_id={user_id}, title={title}, caption={caption}, file_url={file_url}")
    # セッションの作成
    session = databases.create_new_session()

    # Post オブジェクトの作成
    post = models.Post()

    # 各フィールドを設定
    post.title = title
    post.caption = caption
    post.image = file_url  # ファイルURLを設定
    post.create_date_time = datetime.datetime.now()  # 作成日時
    post.user_id = user_id  # user_id の設定
    post.goodcount = 0  # 初期値の設定

    # セッションに追加
    session.add(post)

    # コミットしてデータベースに保存
    try:
        session.commit()
    except Exception as e:
        session.rollback()  # エラー発生時はロールバック
        raise e
    finally:
        session.close()  # セッションを閉じる


## GetOnesPost 特定のユーザーの投稿を取得
async def GetOnesPost(user_id):
    print("GetOnesPost user_id",user_id)
    session = databases.create_new_session()
    posts = session.query(models.Post).\
                filter(models.Post.user_id == user_id).\
                order_by(models.Post.create_date_time.desc()).\
                limit(4).\
                all()         
    if posts == None:
        posts = -1
    
    results = []  # 返却用リスト

    # 各投稿について画像URLを取得し、S3から画像を取得
    for post in posts:
        print(type(post))  # 各要素の型を確認
        
        user = session.query(models.User).\
                filter(models.User.id == post.user_id).\
                first() 

        if isinstance(post, models.Post):
            print(post.image)  # 正常なら image 属性にアクセスできるはず
        else:
            print("Unexpected type:", type(post))
        # print("hogehoge",post.image)

        file_key = post.image   # 投稿に関連する画像URL

        print(f"File Key: {file_key}")


        # S3オブジェクトの取得
        try:
            s3_response = s3_client.get_object(Bucket=BUCKET_NAME, Key=file_key)
            image_data = s3_response['Body'].read()
            # mada
            # with open('downloaded_image.png', 'wb') as f:
            #     f.write(image_data)
            # バイナリから変換する：画像のデータをそのままフロントに返す
            base64_data = base64.b64encode(image_data)
            base64_string = base64_data.decode('utf-8')
            #print("Base64 Image Data", base64_image_data)
            data_url = f"data:image/png;base64,{base64_string}"

            post_data = {
                "post_id": post.id,
                "title": post.title,
                "comment": post.caption,  # 投稿の内容
                "image": data_url,  # Base64エンコードされた画像データ
            }
            results.append(post_data)


        except ClientError as e:
            # エラー処理
            error_message = e.response["Error"]["Message"]
            # raise HTTPException(status_code=404, detail=f"Failed to fetch the image: {error_message}")

    return results

## GetNewPost　新着順で全体の投稿を取得
async def GetNewPost():
    session = databases.create_new_session()
    posts = session.query(models.Post).\
                order_by(models.Post.create_date_time.desc()).\
                limit(4).\
                all()
    if posts == None:
        posts = -1
    results = []  # 返却用リスト
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
