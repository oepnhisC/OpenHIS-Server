from fastapi import APIRouter,Request
from yibao.info import * 
from db.database import get_connection
from pydantic import BaseModel
from time import time
from db.sql.yibaofuzhu.zifeibingrenshangchuangSQL import *
from settings import hospitalID,hospitalName
import requests

menzhenZiFeiBingRenAPI = APIRouter(prefix="/yibaofuzhu", tags=["自费病人信息上传"])


class ShiJian(BaseModel):
    begin_time: str
    end_time: str


class JieZhangID(BaseModel):
    id: str

@menzhenZiFeiBingRenAPI.post("/getMenZhenZiFeiList")
def getMenZhenList(request: Request, shijian: ShiJian):
    """
    获取门诊自费病人列表
    """
    print(shijian)
    if not shijian.begin_time or not shijian.end_time:
        responJson = {'code':2,'result':'时间不能为空'}
        return  responJson
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(menZhenZiFeiListSQL,(shijian.begin_time,shijian.end_time))
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()
    conn.close()
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }
    
    return  responJson


@menzhenZiFeiBingRenAPI.post("/getzhenduan")
def getzhenduan(request: Request, jiezhangid: JieZhangID):
    """
    获取门诊自费诊断
    """
    print(jiezhangid)
    if not jiezhangid.id:
        responJson = {'code':2,'result':'结账ID不能为空'}
        return  responJson
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(menZhenZhenDuanSQL,(jiezhangid.id))
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()
    conn.close()
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }
    
    return  responJson


@menzhenZiFeiBingRenAPI.post("/getMingXi")
def getMingXi(request: Request, jiezhangid: JieZhangID):
    """
    获取门诊自费明细
    """
    print(jiezhangid)
    if not jiezhangid.id:
        responJson = {'code':2,'result':'结账ID不能为空'}
        return  responJson
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(menZhenMingXiSQL,(jiezhangid.id))
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()
    conn.close()
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }
    
    return  responJson


@menzhenZiFeiBingRenAPI.post("/uploadOne")
def uploadOne(request: Request, jiezhangid: JieZhangID):
    """
    上传门诊自费病人信息
    """
    print(jiezhangid)
    if not jiezhangid.id:
        responJson = {'code':2,'result':'结账ID不能为空'}
        return  responJson
    

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(checkIsUploadSQL,(jiezhangid.id))
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()
    conn.close()
    if len(rows) > 0:
        responJson = {'code':2,'result':'单据已上传'}
        return  responJson


    mdtrtinfo = {}
    diseinfo = []
    feedetail =[]
    invoice_no = ''

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(oneMenZhenZiFeiSQL,(jiezhangid.id))
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()
    conn.close()
    if len(rows) == 0:
        responJson = {'code':2,'result':'结账单据信息不存在'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]

        mdtrtinfoData = data[0]
        mdtrtinfo = {
            'fixmedins_mdtrt_id': mdtrtinfoData['fixmedins_mdtrt_id'],
            'fixmedins_code':hospitalID,
            'fixmedins_name':hospitalName,
            'psn_cert_type':mdtrtinfoData['psn_cert_type'],
            'certno':mdtrtinfoData['certno'],
            'psn_name':mdtrtinfoData['psn_name'],
            'begntime':mdtrtinfoData['begntime'],
            'med_type':mdtrtinfoData['med_type']
        }
        invoice_no = mdtrtinfoData['invoice_no']


    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(menZhenZhenDuanSQL,(jiezhangid.id))
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()
    conn.close()
    if len(rows) == 0:
        responJson = {'code':2,'result':'诊断信息不存在'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        for item in data:
            diseinfo.append({
                'diag_type':item['diag_type'],
                'diag_srt_no':item['diag_srt_no'],
                'diag_code':item['diag_code'],
                'diag_name':item['diag_name'],
                'diag_dept':item['diag_dept'],
                'diag_dr_code':item['diag_dr_code'],
                'diag_dr_name':item['diag_dr_name'],
                'diag_time':item['diag_time'],
                'vali_flag':item['vali_flag']
            })

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(menZhenMingXiSQL,(jiezhangid.id))
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.close()
    conn.close()
    if len(rows) == 0:
        responJson = {'code':2,'result':'明细信息不存在'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        for item in data:
            memo = {
                'hosp_appr_flag':item['hosp_appr_flag'],
                'invoice_no':invoice_no,
                'memo':''
            }
            if item['hosp_appr_flag'] == '1':
                memo['memo'] = '审批通过'
            elif item['hosp_appr_flag'] == '0':
                memo['memo'] = '无须审批'
            else:
                memo['memo'] = '自费'

            feedetail.append({
                'fixmedins_mdtrt_id':item['fixmedins_mdtrt_id'],
                'med_type':item['med_type'],
                'bkkp_sn':item['bkkp_sn'],
                'fee_ocur_time':item['fee_ocur_time'],
                'fixmedins_code':hospitalID,
                'fixmedins_name':hospitalName,
                'cnt':float(item['cnt']),
                'pric':float(item['pric']),
                'det_item_fee_sumamt':float(item['det_item_fee_sumamt']),
                'med_list_codg':item['med_list_codg'],
                'medins_list_codg':item['medins_list_codg'],
                'medins_list_name':item['medins_list_name'],
                'med_chrgitm_type':item['med_chrgitm_type'],
                'prodname':item['prodname'],
                'bilg_dept_codg':item['bilg_dept_codg'],
                'bilg_dept_name':item['bilg_dept_name'],
                'bilg_dr_code':item['bilg_dr_code'],
                'bilg_dr_name':item['bilg_dr_name'],
                'memo':memo
            })

        
    requestjson = {
        'mdtrtinfo':mdtrtinfo,
        'diseinfo':diseinfo,
        'feedetail':feedetail
    }

    requestURL,postdata,posthead = create_request_Data('4205',requestjson)
    response = requests.post(requestURL,data=postdata,headers=posthead)
    outputdata = json.loads(response.text)
    print(outputdata)
    if outputdata :
        if outputdata['infcode'] == 0:
            output = outputdata['output']
            responJson = {'code':0,'result':output}

            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(addUploadSQL,(jiezhangid.id,1))
            conn.commit()
            cursor.close()
            conn.close()

        else :
            responJson = {'code':outputdata['infcode'],'result':outputdata['err_msg']}
    return  responJson



@menzhenZiFeiBingRenAPI.post("/uploadOneFinish")
def uploadOneFinish(request: Request, jiezhangid: JieZhangID):
    """
    上传门诊自费病人信息完成
    """
    print(jiezhangid)
    if not jiezhangid.id:
        responJson = {'code':2,'result':'结账ID不能为空'}
        return  responJson
    
    requestjson = {
        'fixmedins_mdtrt_id':jiezhangid.id,
        'fixmedins_code':hospitalID,
        'cplt_flag':'1'
    }
    requestURL,postdata,posthead = create_request_Data('4203',requestjson)
    response = requests.post(requestURL,data=postdata,headers=posthead)
    outputdata = json.loads(response.text)
    print(outputdata)
    if outputdata :
        if outputdata['infcode'] == 0:
            output = outputdata['output']
            responJson = {'code':0,'result':output}
        else :
            responJson = {'code':outputdata['infcode'],'result':outputdata['err_msg']}
    return  responJson