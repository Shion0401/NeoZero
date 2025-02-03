import sys
import models.models as models
import db as databases

import datetime

# aws s3
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# boto3�̕ϐ���`�@����O���[�o���ϐ��ɂ�����
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
        post.image = file_url # �t�@�C��URL�̐ݒ�
    post.create_date_time = datetime.datetime.now()
    post.user_id = user_id  # user_id�̐ݒ�
    post.goodcount = 0  # �����l�̐ݒ�i�I�v�V���i���j

    session.add(post)
    session.commit()
    return 0

## GetOnesPost ����̃��[�U�[�̓��e���擾
async def GetOnesPost(user_id):
    session = databases.create_new_session()
    posts = session.query(models.Post).\
                filter(models.Post.user_id == user_id).\
                order_by(models.Post.create_date_time.desc()).\
                limit(10).\
                all()         
    if posts == None:
        posts = -1
##���Ƃŕ�����K�v����C���[�U�[�������Ƃ��Ɠ��e�����擾���鎞�ɌĂяo�����̂�
    # �e���e�ɂ��ĉ摜URL���擾���AS3����摜���擾
    for post in posts:
        image_url = post.image  # ���e�Ɋ֘A����摜URL
        if image_url == None:
         continue
        # �摜URL��S3��URL�`���ł���ꍇ
        elif image_url.startswith('https://s3.amazonaws.com/'):
            # S3����摜���擾
            bucket_name = BUCKET_NAME  # ���ۂ̃o�P�b�g��
            file_key = image_url.split('/')[-1]  # URL����t�@�C�������擾
            # # S3�I�u�W�F�N�g�̎擾
            # try:
            #     s3_response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
            #     image_data = s3_response['Body'].read()
            #     # �o�C�i������ϊ�����@�摜�̃f�[�^�����̂܂܃t�����g�ɕԂ�
            #     base64_image_data = base64.b64encode(image_data).decode('utf-8')
            # except ClientError as e:
            #     s3_response = -1
    
    return posts

## GetNewPost�@�V�����őS�̂̓��e���擾
async def GetNewPost():
    session = databases.create_new_session()
    posts = session.query(models.Post).\
                order_by(models.Post.create_date_time.desc()).\
                limit(10).\
                all()  
    if posts == None:
        posts = -1
    # �e���e�ɂ��ĉ摜URL���擾���AS3����摜���擾
    results = []
    for post in posts:
        image_url = post.image  # ���e�Ɋ֘A����摜URL
        if image_url == None:
         continue
        # �摜URL��S3��URL�`���ł���ꍇ
        elif image_url.startswith('https://s3.amazonaws.com/'):
            # S3����摜���擾
            bucket_name = BUCKET_NAME  # ���ۂ̃o�P�b�g��
            file_key = image_url.split('/')[-1]  # URL����t�@�C�������擾
            # # S3�I�u�W�F�N�g�̎擾
            # try:
            #     s3_response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
            #     image_data = s3_response['Body'].read()
            #     # �o�C�i������ϊ�����@�摜�̃f�[�^�����̂܂܃t�����g�ɕԂ�
            #     base64_image_data = base64.b64encode(image_data).decode('utf-8')
            # except ClientError as e:
            #     s3_response = -1
        
        # username���擾���A�K�v�ȏ�񂾂���z��ŕԂ� 
        user = session.query(models.User).\
                filter(models.User.id == post.user_id).\
                first()  
        post_data = {
                "id": post.id,
                "comment": post.caption,
                "userid": post.user_id,
                "image": base64_image_data,  # �킩��񂯂Ǒ��������H
                "name": user.name  # ���[�U�[��
        }
        results.append(post_data)
    return results # base64_image_data

## DeletePost �P�̓��e���폜
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

## DeletePostAll�@���ׂĂ̓��e���폜
async def DeletePostAll(user_id):
    session = databases.create_new_session()
    try:
        # ���[�U�[ID�ɕR�Â����e�����ׂĎ擾
        posts = session.query(models.Post).filter(models.Post.user_id == user_id).all()
        # ���e�����݂��Ȃ��ꍇ�̏���
        if not posts:
            return -1  # �܂��́A�K�؂ȃG���[���b�Z�[�W���O���X���[����
        # �摜��S3����폜

        # �e���e���폜
        for post in posts:
            session.delete(post)
        # �R�~�b�g
        session.commit()
        return 0  # ��������
    finally:
        # �Z�b�V���������
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