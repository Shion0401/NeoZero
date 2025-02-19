from fastapi import APIRouter, FastAPI, Depends, Path, HTTPException
import models.models as models
from fastapi.middleware.cors import CORSMiddleware
import cruds.corp_info as handle_db
import cruds.images as image_db
import datetime

app = FastAPI()
router = APIRouter()


## RegisterCorpInfo
@router.post(path="/corpinfo/register")
async def RegisterCorpInfo(corpname: str, email: str, manager: str):
    result = await handle_db.RegisterCorpInfo(corpname, email, manager)
    if result == -1:
        return result
    return result
    # InserAdImageを呼び出す
    # result = await image_db.InserAdImage(result)
    # return result

## GetCorpName
# @router.get(path="/corp_info/corpname")
# async def GetCorpName(user_email: str, user_password: str):
#     result = handle_db.GetConfirmConbination(user_email, user_password)
#     if result == 1:
#         raise HTTPException(status_code=404, detail="Query Error!!")
#     return {
#         "status": "OK",
#         "data": result
#     }
    
    
## GetCorpInfo
@router.get(path="/corpinfo/{corp_id}")
async def GetCorpInfo(corp_id: str):
    result = await handle_db.GetCorpInfo(corp_id)
    return result
    # GetAdImageを呼び出す
    # result = await image_db.GetAdImage(result)
    # return result

## DeleteCorpInfo
@router.delete(path="/corpinfo/delete/{corp_id}")
async def DeleteCorpInfo(corp_id: str):
    result = await handle_db.DeleteCorpInfo(corp_id)
    if result == -1:
        return result
    return result
    # DeleteAdImageを呼び出す
    # result = await image_db.DeleteAdImage(corp_id)
    # return result
