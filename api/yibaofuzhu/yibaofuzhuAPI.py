from fastapi import APIRouter,Request
from yibao.info import * 
from pydantic import BaseModel
import requests
from settings import mdtrtarea_admvs
from time import time
import logging

logger = logging.getLogger(__name__)

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


class RenYuanBianHao(BaseModel):
    psn_no:str = ""
    insuplc_admdvs :str = mdtrtarea_admvs

@yibaofuzhuAPI.post("/personInfo")
async def get_yibao_info(request: Request,personInfoData:PersonInfoData):
    """
    获取参保人信息
    """
    logger.info('get_yibao_info')
    logger.info(personInfoData)
    last_time = 0
    if hasattr(request.app.state,'request_time'):
        last_time = request.app.state.request_time

    current_time = time()
    if (current_time - last_time < 28):
        remaining_time = 28 - (current_time - last_time)
        remaining_time = round(remaining_time, 2)
        return {'code':120,'result':f'请求频率过高，请{remaining_time}秒后再试'}

    request.app.state.request_time = current_time

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
    logger.info('1101入参')
    logger.info(postdata)
    response = requests.post(requestURL,data=postdata,headers=posthead)
    outputdata = json.loads(response.text)
    logger.info('1101出参')
    logger.info(outputdata)
    responJson = {'code':1,'result':'失败'}

    if outputdata :
        if outputdata['infcode'] == 0:
            output = outputdata['output']
            responJson = {'code':0,'result':output}
        else :
            responJson = {'code':outputdata['infcode'],'result':outputdata['err_msg']}

    return  responJson



@yibaofuzhuAPI.post("/jiaofeiInfo")
async def getJiaoFeiInfo(request: Request,renYuanBianHao:RenYuanBianHao):
    """
    获取缴费信息
    """
    
    requestjson = {
        "data": {
            "psn_no": renYuanBianHao.psn_no,
        }
    }
    
    requestURL,postdata,posthead = create_request_Data('90100',requestjson,renYuanBianHao.insuplc_admdvs)
    response = requests.post(requestURL,data=postdata,headers=posthead)
    outputdata = json.loads(response.text)

    responJson = {'code':1,'result':'失败'}

    if outputdata :
        if outputdata['infcode'] == 0:
            output = outputdata['output']
            logger.info(output)
            responJson = {'code':0,'result':output}
        else :
            logger.info(outputdata['err_msg'])
            responJson = {'code':outputdata['infcode'],'result':outputdata['err_msg']}

    return  responJson




@yibaofuzhuAPI.post("/manbingInfo")
async def getManBingInfo(request: Request,renYuanBianHao:RenYuanBianHao):
    """
    获取慢特病信息
    """
    requestjson = {
        "data": {
            "psn_no": renYuanBianHao.psn_no,
        }
    }
    
    requestURL,postdata,posthead = create_request_Data('5301',requestjson,renYuanBianHao.insuplc_admdvs)
    response = requests.post(requestURL,data=postdata,headers=posthead)
    outputdata = json.loads(response.text)

    responJson = {'code':1,'result':'失败'}

    if outputdata :
        if outputdata['infcode'] == 0:
            output = outputdata['output']
            logger.info(output)
            responJson = {'code':0,'result':output}
        else :
            logger.info(outputdata['err_msg'])
            responJson = {'code':outputdata['infcode'],'result':outputdata['err_msg']}

    return  responJson




@yibaofuzhuAPI.post("/dingdianInfo")
async def getDingDianInfo(request: Request,renYuanBianHao:RenYuanBianHao):
    """
    获取定点信息
    """
    requestjson = {
        "data": {
            "psn_no": renYuanBianHao.psn_no,
            'biz_appy_type':'03'
        }
    }
    
    requestURL,postdata,posthead = create_request_Data('5302',requestjson,renYuanBianHao.insuplc_admdvs)
    response = requests.post(requestURL,data=postdata,headers=posthead)
    outputdata = json.loads(response.text)

    responJson = {'code':1,'result':'失败'}

    if outputdata :
        if outputdata['infcode'] == 0:
            output = outputdata['output']
            responJson = {'code':0,'result':output}
        else :
            responJson = {'code':outputdata['infcode'],'result':outputdata['err_msg']}

    return  responJson