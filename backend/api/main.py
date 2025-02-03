from fastapi import FastAPI, APIRouter
from routers import user_info, user_post, report, admin, corp_info, follow, good, images
from fastapi.middleware.cors import CORSMiddleware
from logging import getLogger, StreamHandler


logger = getLogger(__name__)
logger.addHandler(StreamHandler())
logger.setLevel("INFO")



app = FastAPI()
router = APIRouter()
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
<<<<<<< HEAD
    allow_origins=["http://localhost:3000","https://neozeroinc.vercel.app/","https://neozero.metifie.com"],  # フロントエンドのオリジン
=======
    allow_origins=["http://localhost:3000"],  # フロントエンドのオリジン ,"https://neozeroinc.vercel.app","https://neozero.metifie.com"
>>>>>>> 35c19948 (AWSのバックエンドをadd)
    allow_credentials=True,                    # credentialsを許可
    allow_methods=["*"],                       # 全HTTPメソッドを許可
    allow_headers=["*"],                       # 全ヘッダーを許可
)

app.include_router(user_info.router)
app.include_router(user_post.router)
app.include_router(report.router)
app.include_router(admin.router)
app.include_router(corp_info.router)
app.include_router(follow.router)
app.include_router(good.router)
app.include_router(images.router)
