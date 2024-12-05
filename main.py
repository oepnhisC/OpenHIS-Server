from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from api.guahao.urls import guahaoAPI
from api.menzhen.urls import menzhenAPI
from api.shoufei.urls import shoufeiAPI
from api.zizhuji.urls import zizhujiAPI
from api.zizhuji.jiezhangurl import zizhuji_jiezhangAPI
from api.zizhuji.danjuAPI import danjuAPI
from api.yibaofuzhu.yibaofuzhuAPI import yibaofuzhuAPI
from api.shoufei.gaolingbuzhuAPI import gaolingbuzhuAPI
from api.yibaofuzhu.zifeibingrenshangchuangAPI import menzhenZiFeiBingRenAPI


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 开发环境
    # allow_origins=["http://127.0.0.1:16888", "http://localhost:16888"],  # 生产环境
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(guahaoAPI,tags=["挂号"])
app.include_router(menzhenAPI,tags=["门诊"])
app.include_router(shoufeiAPI,tags=["收费"])
app.include_router(zizhujiAPI,tags=["自助机"])
app.include_router(zizhuji_jiezhangAPI,tags=["自助机"])
app.include_router(danjuAPI,tags=["自助机单据"])

app.include_router(yibaofuzhuAPI,tags=["医保辅助"])
app.include_router(gaolingbuzhuAPI,tags=["高龄补助"])
app.include_router(menzhenZiFeiBingRenAPI,tags=["自费病人信息上传"])


@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=10888, reload=False) # 生产环境
    uvicorn.run('main:app', host="0.0.0.0", port=10888, reload=True)  # 开发环境