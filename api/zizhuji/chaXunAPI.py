from fastapi import APIRouter,Request
from yibao.info import create_request_Data
from pydantic import BaseModel
import requests
import json
import logging
from db.database import execute_query
from db.sql.zizhuji.chaXunSQL import *

logger = logging.getLogger(__name__)

chaXunAPI = APIRouter(prefix="/ziZhuJiChaXun",tags=["自助机查询"])

class PingZhengXinXi(BaseModel):
    ecToken:str=''
    idNo:str=''
    insuOrg:str=''
    userName:str=''

@chaXunAPI.post("/yiBaoPingZhengChaXun")
def yiBaoPingZhengChaXun(request: Request,pzxx:PingZhengXinXi):
    '''
    电子医保凭证查询
    '''
    logger.info(f'电子医保凭证查询:{pzxx}' )
    if pzxx.ecToken == '' or pzxx.idNo == '' or pzxx.insuOrg == '' or pzxx.userName == '':
        return {'code':1,'result':'医保凭证信息不能为空'}

    requestjson = {
        "data": {
            "mdtrt_cert_type": "01",
            "mdtrt_cert_no": pzxx.ecToken,
            "card_sn": "",
            "begntime": "",
            "psn_cert_type": "01",
            "certno": pzxx.idNo,
            "psn_name": pzxx.userName
        }
    }

    requestURL,postdata,posthead = create_request_Data('1101',requestjson,pzxx.insuOrg)
    logger.info(f'自助机1101入参:{postdata}')
    response = requests.post(requestURL,data=postdata.encode('utf-8'),headers=posthead)
    outputdata = json.loads(response.text)
    logger.info(f'自助机1101出参:{outputdata}')

    responJson = {'code':1,'result':'失败'}

    if outputdata :
        if outputdata['infcode'] == 0:
            certno =outputdata['output']['baseinfo']['certno']
            logger.info('查询成功,证件号:'+certno)
            responJson = {'code':0,'result':certno}
            rows,columns = execute_query(getRenYuanXinXiByShenFenZhengSQL, (certno,))
            if len(rows) == 0:
                responJson = {'code':2,'result':'没有查询到相关人员信息，请核实信息是否正确'}
            else:
                ryidList = []
                for ryid in rows:
                    ryidList.append(ryid[0]) 
                # 记录人员ID
                logger.info(f'人员ID：{ryidList}')
                request.app.state.ryidList = ryidList
                responJson = {'code':0,'result':ryidList}
                return  responJson    

        else :
            logger.info('查询失败,错误信息:'+outputdata['err_msg'])
            responJson = {'code':outputdata['infcode'],'result':outputdata['err_msg']}

    return  responJson



class SearchContent(BaseModel):
    text:str=''
    type:str='' # 0电子医保凭证，1公众号就诊二维码，2小票二维码

# 获取人员信息
@chaXunAPI.post("/getRenYuanXinXi")
def getRenYuanXinXi(request: Request,st:SearchContent):
    shuru = st.text
    searchType = st.type
    if shuru == '' or searchType == '':
        responJson = {'code':2,'result':'输入有误，请重新输入'}
        return  responJson
    logger.info(f'查询人员信息:{shuru},{searchType}')
    shuru = shuru.replace('\r',  '').replace('\n', '')
    #门诊号
    if(searchType == '1'):
        if( len(shuru) == 10):
            
            rows,columns = execute_query(getRenYuanXinXiByMenZhenHaoSQL, (shuru,))
            if len(rows) == 0:
                responJson = {'code':2,'result':'没有查询到相关人员信息，请核实信息是否正确'}
            else:
                ryidList = []
                for ryid in rows:
                    ryidList.append(ryid[0]) 
                # 记录人员ID
                logger.info(f'人员ID：{ryidList}')
                request.app.state.ryidList = ryidList
                responJson = {'code':0,'result':ryidList}
                return  responJson
        else:
            responJson = {'code':1,'result':'门诊号有误，请重试'}
            return  responJson

    # 小票二维码
    if(searchType == '2'):
        if 'xhcj' in shuru:
            rows,columns = execute_query(getRenYuanXinXiByXiaoPiaoSQL, (shuru,))
            if len(rows) == 0:
                responJson = {'code':2,'result':'没有查询到相关人员信息，请核实信息是否正确'}
                return  responJson
            else:
                ryidList = []
                for ryid in rows:
                    ryidList.append(ryid[0]) 
                # 记录人员ID
                logger.info(f'人员ID：{ryidList}')
                request.app.state.ryidList = ryidList
                responJson = {'code':0,'result':ryidList}
                return  responJson

    return  responJson