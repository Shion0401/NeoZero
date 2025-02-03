from fastapi import APIRouter, FastAPI, Depends, Path, HTTPException
import models.models as models
from fastapi.middleware.cors import CORSMiddleware
import cruds.report as handle_db
import cruds.images as image_db
import schemas.report as schema
import datetime

app = FastAPI()
router = APIRouter()
#origins = ["*"]


## GetReport
@router.get(path="/report/count")
async def GetReport(user_id: str):
    result = await handle_db.GetReport(user_id)
    return result
    

## Insert&UpdateReport
@router.put(path="/report/countup")
async def InsertUpdateReport(user_id: str):
    result = await GetReport(user_id)
    if result == -1:
        return -1
    elif result == 0:
        result = await handle_db.InsertReport(data.userid)
    else:
        result = await handle_db.UpdateReport(data.userid)
    return result

## ExclusionViolationUser
@router.delete(path="/report/exclusive")
async def ExclusionViolationUser(user_id: str):
    result = handle_db.DeleteReport(user_id)
    return result

##Å@ReportPost
@router.get(path="/report/post")
async def ReportPost(postid: str):
    result = await handle_db.ReportPost(postid)
    return result

