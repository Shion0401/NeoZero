from fastapi import APIRouter, FastAPI, Depends, Path, HTTPException
import models.models as models
from fastapi.middleware.cors import CORSMiddleware
import api.cruds.good as handle_db
import api.schemas.good as schema

app = FastAPI()
router = APIRouter()

## Good
@router.post(path="/post/good")
async def Good(data: schema.GoodRequest):
    check = await handle_db.GetConfirmConbination(data.userid, data.postid)
    if check == "None":
        result = await handle_db.Good(data.userid, data.postid)
    elif check == -1:
        return -1
    else:
        result = await handle_db.ChangeFlag(data.userid, data.postid)
    return result

## GoodStatus
@router.get(path="/post/goodstatus/{userid}/{postId}")
async def GoodStatus(userid: str, postId: str):
    result = await handle_db.GoodStatus(userid, postId)
    return result
