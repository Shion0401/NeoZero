from fastapi import APIRouter, FastAPI, Depends, Path, HTTPException
import models.models as models
from fastapi.middleware.cors import CORSMiddleware
import cruds.follow as handle_db
import cruds.images as image_db
import schemas.follow as schema
import datetime

app = FastAPI()
router = APIRouter()


## Follow & UnFollow
@router.post(path="/follow")
async def Follow(data: schema.FollowStatusRequest):
    check = await handle_db.GetConfirmConbination(data.userid, data.followedid)
    print(f"GetConfirmConbination result: {check}")  # デバッグ用ログ
    if check == "None":
        result = await handle_db.Follow(data.userid, data.followedid)
    elif check == -1:
        return -1
    else:
        result = await handle_db.ChangeFlag(data.userid, data.followedid)
    print(f"ChangeFlag result: {result}")  # デバッグ用ログ
    return result

## GetFollow フォローリストをとってくる
@router.get(path="/followlist/{user_id}")
async def GetFollow(user_id: str):
    result = await handle_db.GetFollow(user_id)
    if result == -1:
        return -1
    # GetIconを呼び出す
    # result = await handle_db.GetIcon(user_id)
    print(result)
    return result
    
## FollowStatus
@router.get(path="/post/followstatus/{userid}/{postId}")
async def FollowStatus(userid: str, postId: str):
    followed = await handle_db.Followed(postId)
    result = await handle_db.FollowStatus(userid, followed)
    return result
