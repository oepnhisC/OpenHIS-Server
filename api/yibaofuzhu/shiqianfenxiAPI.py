from fastapi import APIRouter,Request
from yibao.info import * 
from pydantic import BaseModel
import requests
from settings import mdtrtarea_admvs,hospitalName,hospitalID
from time import time
import logging
from typing import List
from db.sql.yibaofuzhu.shiQianFenXiSQL import *
from db.database import execute_query
import json

logger = logging.getLogger(__name__)


shiqianfenxiAPI = APIRouter(prefix="/shiqianfenxi", tags=["事前分析"])

class FsiOrderDtos(BaseModel):
    rx_id:str #处方ID  
    rxno:str #处方号  
    grpno:str #组号
    long_drord_flag:str #长期医嘱标识 0否 1是
    hilist_type:str #目录类别 101西药中成药  102中药饮片  201医疗服务项目 301医用耗材   105其他   106中药颗粒  501长期服务项目
    chrg_type:str #收费类型 01床位费  02诊察费  03检查费  04化验费  05治疗费 06手术 07护理 08卫材 09西药 10中药饮片 11中成药  12一般诊疗  13挂号  14其他
    drord_bhvr:str #医嘱行为 0其他  1出院带药
    hilist_code:str #医保目录代码
    hilist_name:str #医保目录名称
    hilist_lv:str #医保目录等级  01甲类  02乙类 03丙
    hilist_pric:str #医保目录价格
    hosplist_code:str #医院目录代码
    hosplist_name:str #医院目录名称
    cnt:str #数量
    pric:str #单价
    sumamt:str #总金额
    ownpay_amt:str #自费金额
    selfpay_amt:str #自付金额
    spec:str #规格
    spec_unt:str #单位
    drord_begn_date :str #医嘱开始日期
    drord_dept_codg :str #医嘱科室编码
    drord_dept_name :str #医嘱科室名称
    drord_dr_codg :str #医嘱医生编码
    drord_dr_name :str #医嘱医生名称
    drord_dr_profttl:str='2' #医嘱职称 1医士 2医师 3主治医师 4副主任医师 5主任医师 6无 9其他
    curr_drord_flag : str='1' #是否当前处方(医嘱) 0否 1是

class FsiDiagnoseDtos(BaseModel):
    dise_id:str #诊断ID   
    inout_dise_type:str  #出入诊断类别 1入院诊断 2出院诊断   
    maindise_flag:str  #主诊断标识 0否  1是  
    dias_srt_no:str  #诊断序号
    dise_codg:str  #诊断编码
    dise_name:str  #诊断名称
    dise_date:str  #诊断日期

class FsiEncounterDtos(BaseModel):
    fsi_diagnose_dtos:List[FsiDiagnoseDtos] #诊断信息集合
    fsi_order_dtos:List[FsiOrderDtos] #处方信息集合
    fsi_operation_dtos:list = []#手术信息集合
    mdtrt_id:str #就诊ID
    medins_id:str #医疗机构ID
    medins_name:str #医疗机构名称
    medins_admdvs:str #医疗机构管理区划代码
    medins_type:str = 'A1' #医疗机构类型
    medins_lv:str = '05' #医疗机构等级
    wardarea_codg:str = '' #病区标识
    wardno:str='' #病房号
    bedno:str='' #床号
    adm_date:str #入院时间
    dscg_date:str #出院日期
    dscg_main_dise_codg:str #主诊断编码
    dscg_main_dise_name:str #主诊断名称
    dr_codg:str #医生编码
    adm_dept_codg:str #入院科室编码
    adm_dept_name:str #入院科室名称
    dscg_dept_codg:str #出诊科室编码
    dscg_dept_name:str #出诊科室名称
    med_mdtrt_type:str #就诊类型  1门诊 2住院 3购药 4其他
    med_type:str #医疗类别  11普通门诊  14门诊慢特病  21普通住院
    matn_stas:str #生育状态   0其他 1妊娠期 2哺乳期
    medfee_sumamt:str = '-' #总费用
    ownpay_amt:str= '-' #自费金额 
    selfpay_amt :str= '-' #自付金额 
    setl_totlnum :str= '-' #结算总数 
    insutype:str='' #险种 310 390    
    reim_flag:str='1'   
    out_setl_flag:str='2' #2医疗机构 3省内异地 4跨省异地

class PatientDtos(BaseModel):
    fsi_encounter_dtos:List[FsiEncounterDtos] #就诊信息集合
    fsi_his_data_dto:str = '' #医院信息集合
    patn_id:str #参保人ID
    patn_name:str #姓名
    gend:str #性别
    brdy:str #出生日期
    poolarea:str #统筹区编码
    curr_mdtrt_id:str #当前就诊ID
    

class ShiQianFenXiXinXi(BaseModel):
    patient_dtos:List[PatientDtos] = [] #参保人信息
    trig_scen:str #触发场景   1门诊挂号;2门诊收费登记;3住院登记;4住院收费登记;5住院执行医嘱；6门诊结算;7门诊预结算;8住院结算;9住院预结算;
    rule_ids:list = [] #规则ID集合


class YiZhuXinXi(BaseModel):
    brname:str #病人姓名
    brid:str #病人ID
    jzid:str #就诊ID
    yzdidList:List[str] #医嘱单ID
    fsi_diagnose_dtos:List[FsiDiagnoseDtos] #诊断信息集合
    adm_date : str #入院日期
    dscg_main_dise_codg:str #主诊断编码
    dscg_main_dise_name:str #主诊断名称
    dr_codg :str #医生编码
    adm_dept_codg:str #入院科室编码
    adm_dept_name:str #入院科室名称
    med_type:str #医疗类别  11普通门诊  14门诊慢特病  21普通住院
    insutype : str #险种 310 390    
    gend:str #性别 0未知 1男 2女 9未说明
    brdy:str #出生日期
    

@shiqianfenxiAPI.post("/shiQianFenXi")
async def shiQianFenXi(request: Request,yzxx:YiZhuXinXi):
    '''
    3101 明细审核事前分析服务
    '''
    if not hasattr(request.app.state,'fryid'):
        return {'code':2,'result':'无登录信息'}
    fryid = request.app.state.fryid
    fryno = request.app.state.username
    fname = request.app.state.fname

    responJson = {}

    if len(yzxx.yzdidList)<= 0:
        responJson = {'code':2,'result':'医嘱单ID不能为空'}
        return responJson

    placeholders = ','.join('?' for _ in yzxx.yzdidList)  
    newsql = chuFangXinXiSQL + f'({placeholders})'
    rows,columns = execute_query(newsql,(yzxx.brid,yzxx.jzid,)+tuple(yzxx.yzdidList) )  
    if len(rows) <= 0:
        responJson = {'code':2,'result':'未查询到相关数据'}
        return responJson

    chuFangXinXi = [dict(zip(columns, row)) for row in rows]


    medfee_sumamt = round(sum(float(i['sumamt']) for i in chuFangXinXi)  ,2) 

    requestjson ={
    "data": {
        "patient_dtos": [
            {
            "fsi_encounter_dtos": [
                {
                "fsi_diagnose_dtos":[instance.__dict__  for instance in yzxx.fsi_diagnose_dtos] ,
                "fsi_order_dtos": chuFangXinXi,
                "fsi_operation_dtos": [],
                "mdtrt_id": yzxx.jzid,
                "medins_id": hospitalID,
                "medins_name": hospitalName,
                "medins_admdvs": mdtrtarea_admvs,
                "medins_type": "A1",
                "medins_lv": "05",
                "wardarea_codg": "",
                "wardno": "",
                "bedno": "",
                "adm_date": yzxx.adm_date,
                "dscg_date": yzxx.adm_date,
                "dscg_main_dise_codg": yzxx.dscg_main_dise_codg,
                "dscg_main_dise_name":yzxx.dscg_main_dise_name,
                "dr_codg": yzxx.dr_codg,
                "adm_dept_codg": yzxx.adm_dept_codg,
                "adm_dept_name": yzxx.adm_dept_name,
                "dscg_dept_codg": yzxx.adm_dept_codg,
                "dscg_dept_name": yzxx.adm_dept_name,
                "med_mdtrt_type": "1",
                "med_type": yzxx.med_type,
                "matn_stas": "0",
                "medfee_sumamt": medfee_sumamt,
                "ownpay_amt": "0",
                "selfpay_amt": "0",
                "acct_payamt": "",
                "ma_amt": "",
                "hifp_payamt": "",
                "setl_totlnum": "1",
                "insutype": yzxx.insutype,
                "reim_flag": "1",
                "out_setl_flag": "2"
                }
            ],
            "fsi_his_data_dto": "",
            "patn_id": yzxx.brid,
            "patn_name": yzxx.brname,
            "gend": yzxx.gend,
            "brdy": yzxx.brdy,
            "poolarea": mdtrtarea_admvs,
            "curr_mdtrt_id": yzxx.jzid
            }
        ],
        "trig_scen": "2"
        }
    }
    requestURL,postdata,posthead = create_request_Data('3101',requestjson,opter=fryno,opter_name=fname)
    logger.info(f'用户:{fname}，3101入参:{postdata}')
    response = requests.post(requestURL,data=postdata.encode('utf-8'),headers=posthead)
    outputdata = json.loads(response.text)
    logger.info(f'用户:{fname}，3101出参:{outputdata}')

    responJson = {'code':1,'result':'失败'}
    if outputdata :
        if outputdata['infcode'] == 0:
            output = outputdata['output']
            responJson = {'code':0,'result':output,'uploadData':json.loads(postdata)}
        else :
            responJson = {'code':outputdata['infcode'],'result':outputdata['err_msg'],'uploadData':json.loads(postdata)}
    return responJson





class WarnDtos(BaseModel):
    warn_rslt_id:str #违规标识 取自jr_id
    dspo_way:str  #处理方式 1.继续执行医嘱  2.返回修改医嘱
    dspo_way_rea :str=''  #处理原因  如果为dspoWay 为1必填

class FanKuiXinXi(BaseModel):
    warn_type:str = '1' #反馈类型 1事前  2事中
    warns:List[WarnDtos] #处理数据集合

@shiqianfenxiAPI.post("/shiQianFenXiFanKui")
async def shiQianFenXiFanKui(request: Request,fkxx:FanKuiXinXi):
    '''
    事前分析反馈
    '''
    if not hasattr(request.app.state,'fryid'):
        return {'code':2,'result':'无登录信息'}
    fryid = request.app.state.fryid
    fryno = request.app.state.username
    fname = request.app.state.fname

    for warn in fkxx.warns:
        if warn.dspo_way == '1':
           if warn.dspo_way_rea == '':
               return {'code':2,'result':'选择继续继续执行医嘱时，处理原因不能为空'}

    requestjson = {
        'data':{
            'warn_type':fkxx.warn_type,
            'warns':[instance.__dict__ for instance in fkxx.warns]
        }
    }

    requestURL,postdata,posthead = create_request_Data('3103',requestjson,opter=fryno,opter_name=fname)
    logger.info(f'用户:{fname}，3103入参:{postdata}')
    response = requests.post(requestURL,data=postdata.encode('utf-8'),headers=posthead)
    outputdata = json.loads(response.text)
    logger.info(f'用户:{fname}，3103出参:{outputdata}')

    if outputdata :
        if outputdata['infcode'] == 0:
            output = outputdata['output']
            responJson = {'code':0,'result':output}
        else :
            responJson = {'code':outputdata['infcode'],'result':outputdata['err_msg']}
    return responJson


@shiqianfenxiAPI.post('/getZhuYuanList')
async def getZhuYuanList(request: Request):
    '''
    获取住院病人列表
    '''
    responJson = {}
    rows, columns = execute_query(getZhuYuanListSQL,())
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }

    return responJson

class ZhuYuanChaXun(BaseModel):
    beginTime:str #开始时间
    endTime:str #结束时间
    content:str #病人ID

@shiqianfenxiAPI.post('/chaXunZhuYuanBingRen')
async def chaXunZhuYuanBingRen(request: Request,zycx:ZhuYuanChaXun):
    '''
    查询住院病人
    '''
    responJson = {}
    if zycx.content == '':
        return {'code':2,'result':'查询内容不能为空'}
    
    rows, columns = execute_query(chaXunZhuYuanBingRenSQL,( zycx.beginTime, zycx.endTime, zycx.content , zycx.content, zycx.content, zycx.content ))
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }
    
    return responJson

class ZhuYuanXinXi(BaseModel):
    brid:str #病人ID
    jzid:str #就诊ID

@shiqianfenxiAPI.post('/getZhuYuanZhenDuan')
async def getZhuYuanZhenDuan(request: Request,zyxx:ZhuYuanXinXi):
    '''
    获取住院诊断信息
    '''
    responJson = {}
    if zyxx.brid == '' or zyxx.jzid == '':
        return {'code':2,'result':'病人ID或就诊ID不能为空'}
    
    rows, columns = execute_query( getZhuYuanZhenDuanSQL,( zyxx.jzid,zyxx.brid ) )
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }
    
    return responJson


@shiqianfenxiAPI.post('/getZhuYuanBingRenXinXi')
async def getZhuYuanBingRenXinXi(request: Request,zyxx:ZhuYuanXinXi):
    '''
    获取住院病人信息
    '''
    responJson = {}
    if zyxx.brid == '' or zyxx.jzid == '':
        return {'code':2,'result':'病人ID或就诊ID不能为空'}
    
    rows, columns = execute_query( getZhuYuanBingRenXinXiSQL,( zyxx.jzid ,zyxx.brid ) )
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }
    
    return responJson



@shiqianfenxiAPI.post('/getZhuYuanChuFangXinXi')
async def getZhuYuanChuFangXinXi(request: Request,zyxx:ZhuYuanXinXi):
    '''
    获取住院处方信息
    '''
    responJson = {}
    if zyxx.brid == '' or zyxx.jzid == '':
        return {'code':2,'result':'病人ID或就诊ID不能为空'}
    
    rows, columns = execute_query( getZhuYuanChuFangXinXiSQL,( zyxx.jzid ,zyxx.brid ) )
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }
    
    return responJson