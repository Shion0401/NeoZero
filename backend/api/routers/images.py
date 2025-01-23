from fastapi import APIRouter, FastAPI, Depends, Path, HTTPException, Query, UploadFile,File
import models.models as models
from fastapi.middleware.cors import CORSMiddleware
import cruds.images as image_db
import cruds.user_post as handle_db
import datetime

# aws s3�@������O���[�o���ɂ�����
import boto3
from botocore.exceptions import BotoCoreError, ClientError

# boto3�̕ϐ���`�@����O���[�o���ϐ��ɂ�����
BUCKET_NAME = "neozero"
REGION_NAME = "us-east-1"
s3_client = boto3.client(
    "s3", 
    region_name=REGION_NAME)


app = FastAPI()
router = APIRouter()

## ���[�U�[�A�C�R����Ԃ�
@router.get(path="/geticonimg/{user_id}")
async def GetUserIcon(user_id: str):
    user_icon = await image_db.GetIcon(user_id)
    # ���[�U�[�A�C�R�������݂��Ȃ��ꍇ�͏������s���Ȃ�
    if not user_icon is None:
        if user_icon.startswith('https://s3.amazonaws.com/'):
            # S3����摜���擾
            bucket_name = BUCKET_NAME  # ���ۂ̃o�P�b�g��
            file_key = user_icon.split('/')[-1]  # URL����t�@�C�������擾
            # # S3�I�u�W�F�N�g�̎擾
            try:
                s3_response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
                image_data = s3_response['Body'].read()
                # �o�C�i������ϊ�����@�摜�̃f�[�^�����̂܂܃t�����g�ɕԂ�
                base64_image_data = base64.b64encode(image_data).decode('utf-8')
            except ClientError as e:
                s3_response = -1
    # ���[�U�[�A�C�R�������݂��Ȃ��ꍇ��NULL��Ԃ�
    return user_icon
