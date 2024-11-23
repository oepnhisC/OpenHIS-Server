from fastapi import APIRouter,Request
from yibao.info import * 
from db.database import get_connection
from pydantic import BaseModel
import requests
from settings import mdtrtarea_admvs


yibaofuzhuAPI = APIRouter(prefix="/yibaofuzhu", tags=["医保辅助功能"])


class PersonInfoData(BaseModel):
    mdtrt_cert_type:str = "02"
    mdtrt_cert_no:str = ''
    card_sn:str = ""
    begntime:str = ""
    psn_cert_type:str = ''  
    certno:str =''
    psn_name:str =''
    insuplc_admdvs :str = mdtrtarea_admvs


@yibaofuzhuAPI.post("/personInfo")
async def get_yibao_info(request: Request,personInfoData:PersonInfoData):
    """
    获取参保人信息
    """
    requestjson = {
        "data": {
            "mdtrt_cert_type": personInfoData.mdtrt_cert_type,
            "mdtrt_cert_no": personInfoData.mdtrt_cert_no,
            "card_sn": personInfoData.card_sn,
            "begntime": personInfoData.begntime,
            "psn_cert_type": personInfoData.psn_cert_type,
            "certno": personInfoData.certno,
            "psn_name": personInfoData.psn_name
        }
    }
    
    requestURL,postdata,posthead = create_request_Data('1101',requestjson,personInfoData.insuplc_admdvs)
    response = requests.post(requestURL,data=postdata,headers=posthead)
    outputdata = json.loads(response.text)

    responJson = {'code':1,'result':'失败'}

    if outputdata :
        if outputdata['infcode'] == 0:
            output = outputdata['output']
            print(output)
            responJson = {'code':0,'result':output}
        else :
            print(outputdata['err_msg'])
            responJson = {'code':outputdata['infcode'],'result':outputdata['err_msg']}

    return  responJson