from fastapi import APIRouter,Request
from pydantic import BaseModel
from db.database import execute_query,get_mssql_connection,get_mssql_connection_cp936,get_connection
from db.sql.menzhen.menzhenyizhuSQL import *
import xml.etree.ElementTree as ET
import pymssql
import logging
from typing import List
import traceback


logger = logging.getLogger(__name__)

menzhenYiZhuAPI = APIRouter(prefix="/menzhenyizhu",tags=["门诊医嘱"])


class SearchContent(BaseModel):
    content:str = ''
    keshiId:str = ''

@menzhenYiZhuAPI.post("/getICD10Code")
async def getICD10Code(request:Request,searchContent:SearchContent):
    '''
    获取ICD10编码
    '''
    responJson = {}
    if searchContent.content == '':
        responJson = {'code':1,'result':'请输入搜索内容'}
        return  responJson
    content = '%' + searchContent.content + '%'
    rows, columns = execute_query(getICD10CodeSQL,(content,content,content))
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }

    return responJson



@menzhenYiZhuAPI.post("/getYiZhuContent")
async def getYiZhuContent(request:Request,searchContent:SearchContent):
    '''
    获取医嘱内容
    '''
    if not hasattr(request.app.state,'fryid'):
        return {'code':2,'result':'无登录信息'}
    fryid = request.app.state.fryid

    responJson = {}
    
    if searchContent.keshiId == '':
        return {'code':1,'result':'请选择科室'}
    keshiId = searchContent.keshiId
    if searchContent.content == '':
        responJson = {'code':1,'result':'请输入搜索内容'}
        return  responJson
    content = '%' + searchContent.content + '%'
    rows, columns = execute_query(getYiZhuContentSQL,(content,keshiId,fryid))
    if len(rows) == 0:
        responJson = {'code':1,'result':'未查询到相关信息'}
        return  responJson
    else:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }

    return responJson



@menzhenYiZhuAPI.get("/getGeiYaoTuJing")
async def getGeiYaoTuJing(request:Request):
    '''
    获取给药途径
    '''
    if not hasattr(request.app.state,'fryid'):
        return {'code':2,'result':'无登录信息'}
    fryid = request.app.state.fryid
    rows, columns = execute_query(getGeiYaoTuJingSQL,(fryid,))
    if len(rows) == 0:
        return {'code':1,'result':'未查询到相关信息'}
    else:
        data = [dict(zip(columns, row)) for row in rows]
        return { 'code':0,'result':data }
    
@menzhenYiZhuAPI.get("/getPinci")
async def getPinci(request:Request):
    '''
    获取频次
    '''
    rows, columns = execute_query(getPinciSQL,())
    if len(rows) == 0:
        return {'code':1,'result':'未查询到相关信息'}
    else:
        data = [dict(zip(columns, row)) for row in rows]
        return { 'code':0,'result':data }
    

@menzhenYiZhuAPI.get('/getYongYaoMuDi')
async def getYongYaoMuDi(request:Request):
    '''
    获取用药目的
    '''
    rows, columns = execute_query(getYongYaoMuDiSQL,())
    if len(rows) == 0:
        return {'code':1,'result':'未查询到相关信息'}
    else:
        data = [dict(zip(columns, row)) for row in rows]
        return { 'code':0,'result':data }
    

@menzhenYiZhuAPI.get('/getYiZhuBeiZhu')
async def getYiZhuBeiZhu(request:Request):
    '''
    获取医嘱备注
    '''
    rows, columns = execute_query(getYiZhuBeiZhuSQL,())
    if len(rows) == 0:
        return {'code':1,'result':'未查询到相关信息'}
    else:
        data = [dict(zip(columns, row)) for row in rows]
        return { 'code':0,'result':data }
    

@menzhenYiZhuAPI.get('/getZhiXingKeShi')
async def getZhiXingKeShi(request:Request):
    '''
    获取执行科室
    '''
    rows, columns = execute_query(getZhiXingKeShiSQL,())
    if len(rows) == 0:
        return {'code':1,'result':'未查询到相关信息'}
    else:
        data = [dict(zip(columns, row)) for row in rows]
        return { 'code':0,'result':data }
    


@menzhenYiZhuAPI.get('/getGeiYaoZhiXingKeShi')
async def getGeiYaoZhiXingKeShi(request:Request):
    '''
    获取给药执行科室
    '''
    rows, columns = execute_query(getGeiYaoZhiXingKeShiSQL,())
    if len(rows) == 0:
        return {'code':1,'result':'未查询到相关信息'}
    else:
        data = [dict(zip(columns, row)) for row in rows]
        return { 'code':0,'result':data }
    
class XiangMuID(BaseModel):
    id:str = ''

@menzhenYiZhuAPI.post('/getYiBaoXianZhi')
async def getYiBaoXianZhi(request:Request,xiangmuID:XiangMuID):
    '''
    获取医保限制
    '''
    if xiangmuID.id == '':
        return {'code':1,'result':'请选择项目'}
    rows, columns = execute_query(getYiBaoXianZhiSQL,(xiangmuID.id,))
    if len(rows) == 0:
        return {'code':1,'result':'未查询到相关信息'}
    else:
        data = [dict(zip(columns, row)) for row in rows]
        return { 'code':0,'result':data }
    

@menzhenYiZhuAPI.post('/getYaoPinGuiGe')
async def getYaoPinGuiGe(request:Request,xiangmuID:XiangMuID):
    '''
    获取药品规格
    '''
    if xiangmuID.id == '':
        return {'code':1,'result':'请选择项目'}
    rows, columns = execute_query(getYaoPinGuiGeSQL,(xiangmuID.id,))
    if len(rows) == 0:
        return {'code':1,'result':'未查询到相关信息'}
    else:
        data = [dict(zip(columns, row)) for row in rows]
        return { 'code':0,'result':data }
    

@menzhenYiZhuAPI.get('/getYiZhuDanID')
async def getYiZhuDanID(request:Request):
    '''
    获取医嘱ID
    '''
    if not hasattr(request.app.state,'fryid'):
        return {'code':2,'result':'无登录信息'}
    
    successFlag = False

    yizhudanID = ''
    conn = get_mssql_connection()
    cursor = conn.cursor()
    responJson = {'code':1,'result':'失败'}
    try:
        msg = cursor.callproc('CreateDanJuID',  (pymssql.output(int),7) )   
        logger.info( '医嘱单ID：'+str(msg[0]) )
        yizhudanID = msg[0]
        successFlag = True
    except(Exception) as e:
        error_code = e.args[0]
        error_message_bytes = e.args[1]
        error_message = error_message_bytes.decode('utf-8')
        logger.info(f"错误代码：{error_code}")
        logger.info(f"错误信息：{error_message}")
        responJson = {'code':2,'result':'校验失败'}
    finally:
        cursor.close()
        conn.close()

    if not successFlag:
        return responJson
    
    return {'code':0,'result':{'yzdid':yizhudanID}}




class YiZhuDan(BaseModel):
    id:str = ''
    ryid :str = '' # 人员ID
    jzid:str = ''  #就诊ID
    xingzhi:str = '' #性质
    leixing:str = '' #类型
    brksid:str = ''   #病人科室
    kdks:str = ''   #开单科室

class ZhenDuan(BaseModel):
    yzdid:str = '' #医嘱单ID
    ryid:str = ''  #人员ID
    jzid:str = ''  #就诊ID
    zdcx:str = '' #诊断次序
    cbzc:str = '1' #初步或正常
    xyzy:str = '0' #西医或中医
    zdlx:str = '1' #诊断类型
    jbid:str = '' #疾病ID
    jKESHIid:str = '0' #疾病参考id
    jbname:str = '' #疾病名称
    yizhen:str = '' #疑诊
    zyzh:str = '' #中医证候
    icdbm:str = '' #ICD编码
    zcbz:str = '' #主次标志

class YiZhuContent(BaseModel):
    yzdid:str = '' #医嘱单ID
    brid:str = ''  #病人ID
    jzid:str = ''  #就诊ID
    kzksid:str = '' #开嘱科室
    dsdw:str = '' #滴速单位
    sbbs:str = '' #伤病标识
    brksid:str = '' #病人科室
    cixu:str = '' #次序
    state:str = '' #医嘱状态
    zllx:str = '' #诊疗类型
    ylxmid:str = '' #医疗项目ID
    bbbw:str = '' #标本部位
    jcbw:str = '' #检查部位
    sfxmid:str = '0' #收费项目ID
    tianshu:str = '' #天数
    jiliang:str = '' #剂量
    yongliang:str = '' #用量
    danliang :str = '' #单量
    dldw:str = '' #单量单位
    shuliang:str = '' #数量
    yizhu:str = '' #医嘱内容
    yszt:str = '' #医嘱嘱托
    zxksid:str = '' #执行科室ID
    zxks:str = '' #执行科室
    zxpc:str = '' #执行频次
    plcs:str = '' #频率次数
    pljg:str = '' #频率间隔
    jgdw:str = '' #间隔单位
    gytjbz:str = '' #给药途径标志
    jjbz:str = '' #紧急标志
    kszxsj:str = '' #开始执行时间
    zxzzsj:str = '9999-12-30 00:00:00' #执行终止时间
    ysbm:str = '' #医生编码
    ysname:str = '' #医生姓名
    yzbz:str = '' #医嘱备注
    gyksid:str = '' #给药科室
    gyxz:str = '' #给药性质
    zuhao:str = '' #组号
    disu:str = '' #滴速
    tczllx:str = '' #套餐诊疗类型
    ysid:str = '' #医生ID
    zlfaid:str = '0' #治疗方案ID
    ypyf:str = '' #药品用法
    fhybxz:str = '' #符合医保限制
    yppcid:str = '0' #药品批次ID
    fubiaoid:str = '' #附表ID
    bfzbz:str = '' #并发症标志
    pishi:str = '' #皮试
    jcbwbm:str = '' #检查部位编码
    lsid:str = '' #临时ID
    lsxgid:str = '' #临时相关ID

class ShouFeiXiangMu(BaseModel):
    yzsl :str = '' #医嘱数量
    danjia:str = '' #单价
    xmid:str = '' #项目ID
    jbdwdj:str = '' #基本单位单价
    zongliang:str = '' #总量,基本单位数量
    zxksid:str = '' #执行科室ID
    zxks:str = '' #执行科室
    fyjlid:str = '' #费用记录ID
    fubiaoid:str = '' #附表ID
    yzdid:str = '' #医嘱单ID
    djid:str = '' #单据ID
    yppcid:str = '0' #药品批次ID
    cbj:str = '' #成本价
    tcid:str = '0' #套餐ID
    sfdzsl:str = '' #收费对照数量
    csbz:str = '' #从属标志
    fyxz:str = '1' #费用性质
    sffs:str = '' #收费方式
    fhybxz:str = '' #符合医保限制
    ybxmbm:str = '' #医保项目编码
    ybxmmc:str = '' #医保项目名称

class ShenQingDan(BaseModel):
    yzdid:str = '' #医嘱单ID
    brid:str = ''  #病人ID
    jzid:str = ''  #就诊ID
    jjbz:str = '' #紧急标志
    brksid:str = '' #病人科室
    sqks:str = '' #申请科室
    sqr:str = '' #申请人
    sqrid:str = '' #申请人ID
    zhaiyao:str='' #摘要
    fzjc:str = '' #辅助检查
    zllx:str = '' #诊疗类型
    sltz:str = '' #生理体征
    jcmd:str = '' #检查目的
    lczd:str = '' #临床诊断

class ShouShuRenYuan(BaseModel):
    yzdid:str = '' #医嘱单ID
    brid:str = ''  #病人ID
    jzid:str = ''  #就诊ID
    zuhao:str = '' #组号
    cixu:str = '' #次序
    gangwei:str = '' #岗位
    ryid:str = '' #人员ID
    rybm:str = '' #人员编码
    ryname:str = '' #人员姓名
    sch:str = '' #顺序号
    ysid:str = '' #要素id

class GuaHaoBingLi(BaseModel):
    jzid:str = '' #就诊ID
    jws:str='' #既往史

class YiZhu(BaseModel):
    yizhudan:List[YiZhuDan] = []
    zhenduan:List[ZhenDuan] = []
    yizhucontent:List[YiZhuContent] = []
    shoufeixiangmu:List[ShouFeiXiangMu] = []
    shenqingdan:List[ShenQingDan] = []
    shoushurenyuan:List[ShouShuRenYuan] = []
    guahaobingli:List[GuaHaoBingLi] = []
    brid:str = '' #病人ID
    jzid:str = '' #就诊ID
    kzksid:str = '' #开嘱科室
    flag:str = '' #标志


@menzhenYiZhuAPI.post('/yiZhuJianCha')
async def yiZhuJianCha(request:Request,yizhu:YiZhu):
    '''
    药品医嘱检查
    '''
    if not hasattr(request.app.state,'fryid'):
        return {'code':2,'result':'无登录信息'}
    fryid = request.app.state.fryid

    responJson = {}


    root = ET.Element("Root")
    YZD1 = ET.SubElement(root, "YZD1")
    for yzd in yizhu.yizhudan:
        YZD1_ie = ET.SubElement(YZD1, "Ie", {
            "YZDID": yzd.id,
            "YZD06": yzd.xingzhi,
            "YZD07": yzd.leixing,

        })

    ZDD1 = ET.SubElement(root, "ZDD1")
    for zhenduan in yizhu.zhenduan:
        ZDD1_ie = ET.SubElement(ZDD1, "Ie", {
            "YZDID": zhenduan.yzdid, 
            "JBB11": zhenduan.jbid, 
            "ZDD15": zhenduan.jbname, 
        
        })

    YZNR1 = ET.SubElement(root, "YZNR1")
    for content in yizhu.yizhucontent:
        YZNR1_ie = ET.SubElement(YZNR1, "Ie", {
            "YZDID": content.yzdid, 
            "YZFB28": content.dsdw,
            "KESHI11":content.brksid, "ROWNR":content.cixu, 
            "XMLX01": content.zllx, "ZZXM01": content.ylxmid, "YZNR14": content.bbbw, 
            "YZNR15": content.jcbw, "SFXM01": content.sfxmid, "YZNR17": content.tianshu,
            "YZNR18": content.jiliang, "YZNR19": content.yongliang,
              "YZNR20": content.danliang,
            "KESHI14": content.gyksid, "YZNR58": content.gyxz, "YZNR59": content.zuhao, 
            "YZNR60": content.disu,  "XMLX11": content.tczllx, "YGB11": fryid, 
            "YZNR12": content.zlfaid, "YZFB02": content.fhybxz, "YPPC01": content.yppcid, 
            "YZFB08": content.fubiaoid,
        })

    SQD1 = ET.SubElement(root, "SQD1")
    for shenqing in yizhu.shenqingdan:
        SQD1_ie = ET.SubElement(SQD1, "Ie", {
            "SQD01": shenqing.yzdid, 
            "RYXX07": yizhu.jzid, 
            "KESHI11": shenqing.brksid,
            "KESHI12": shenqing.sqks, 
            "YGB11":shenqing.sqrid,  
            "SQD29": shenqing.zhaiyao,
            "XMLX01": shenqing.zllx, 
        })

  

    xml_string = ET.tostring(root, encoding='utf-8').decode('utf-8')

    print(xml_string)

    conn = get_mssql_connection()
    cursor = conn.cursor()
    responJson = {'code':1,'result':'失败'}
    try:
        
        msg = cursor.callproc('JianChaYiZhu',  ( xml_string,1,yizhu.jzid,0,fryid,0,0,pymssql.output(str) ) )   
        logger.info( '检查医嘱结果：'+str(msg[7]) )
        responJson = {'code':0,'result':msg[7]}
    except(Exception) as e:
        error_code = e.args[0]
        error_message_bytes = e.args[1]
        error_message = error_message_bytes.decode('utf-8')
        logger.info(f"错误代码：{error_code}")
        logger.info(f"错误信息：{error_message}")
        responJson = {'code':2,'result':'系统错误'}
    finally:
        cursor.close()
        conn.close()

    return responJson


@menzhenYiZhuAPI.post('/shengChengFeiYong')
async def shengChengFeiYong(request:Request,yizhu:YiZhu):
    '''
    生成医嘱或费用
    '''
    if not hasattr(request.app.state,'fryid'):
        return {'code':2,'result':'无登录信息'}
    fryid = request.app.state.fryid

    root = ET.Element("Root")

    YZNR1 = ET.SubElement(root, "YZNR1")

    for content in yizhu.yizhucontent:
        ie = ET.SubElement(YZNR1, "Ie", {
            "YZNR01": content.lsid,"YZNR11":content.lsxgid,
            "KESHI11": content.brksid,"ROWNR": content.cixu,"XMLX01": content.zllx,
            "ZZXM01": content.ylxmid,"YZNR14": content.bbbw,
            "YZNR15": content.jcbw,"SFXM01": content.sfxmid,
            "YZNR18": content.jiliang, "YZNR20": content.danliang,
        })

    xml_string = ET.tostring(root, encoding='utf-8').decode('utf-8')
    logger.info('生成医嘱或费用')
    logger.info(xml_string)

    conn = get_mssql_connection_cp936()
    cursor = conn.cursor()
    responJson = {'code':1,'result':'失败'}
    rows = []
    columns = []
    success = False
    try:
        cursor.callproc('ShengChengYiZhuFeiYong',  ( xml_string,1,yizhu.jzid,0,'普通',yizhu.flag,0 ) )   
        rows = cursor.fetchall() 
        columns = [column[0] for column in cursor.description]
        success = True
    except(Exception) as e:
        error_code = e.args[0]
        error_message_bytes = e.args[1]
        error_message = error_message_bytes.decode('utf-8')
        logger.info(f"错误代码：{error_code}")
        logger.info(f"错误信息：{error_message}")
        responJson = {'code':2,'result':'系统错误'}
        success = False
    finally:
        cursor.close()
        conn.close()

    if success:
        data = [dict(zip(columns, row)) for row in rows]
        responJson = { 'code':0,'result':data }

    
    return responJson




@menzhenYiZhuAPI.post('/queRenYiZhu')
async def queRenYiZhu(request:Request,yizhu:YiZhu):
    '''
    确认医嘱
    '''
    if not hasattr(request.app.state,'fryid'):
        return {'code':2,'result':'无登录信息'}
    
    fryid = request.app.state.fryid
    fryno = request.app.state.username
    fname = request.app.state.fname

    responJson = {}
    root = ET.Element("Root")
    YZD1 = ET.SubElement(root, "YZD1")
    for yzd in yizhu.yizhudan:
        YZD1_ie = ET.SubElement(YZD1, "Ie", {
            "YZDID": yzd.id, "RYXX01": yizhu.brid, "RYXX07": yizhu.jzid,
            "YZD06": yzd.xingzhi, "YZD07": yzd.leixing,
        })

    ZDD1 = ET.SubElement(root, "ZDD1")
    for zhenduan in yizhu.zhenduan:
        ZDD1_ie = ET.SubElement(ZDD1, "Ie", {
            "YZDID": zhenduan.yzdid, "RYXX01": yizhu.brid, "RYXX07": yizhu.jzid, 
            "ZDD06": zhenduan.zdcx, "ZDD07": zhenduan.cbzc, "ZDD10": zhenduan.xyzy,
             "JBB11": zhenduan.jbid,
        })

    # YZNR1 节点
    YZNR1 = ET.SubElement(root, "YZNR1")
    for content in yizhu.yizhucontent:
        YZNR1_ie = ET.SubElement(YZNR1, "Ie", {
            "YZDID": content.yzdid,  "RYXX01": yizhu.brid,"YZNR06": yizhu.jzid,
            "YZFB28": content.dsdw, "YZFB41": content.sbbs,  
            "KESHI11":yizhu.kzksid, "ROWNR":content.cixu, "YZNR10": content.state, 
            "XMLX01": content.zllx, "ZZXM01": content.ylxmid, "YZNR14": content.bbbw, 
            "YZNR15": content.jcbw, "SFXM01": content.sfxmid, "YZNR17": content.tianshu,
            "YZNR18": content.jiliang, "YZNR19": content.yongliang, "YZNR20": content.danliang,
        })

    # SFJL1 节点
    SFJL1 = ET.SubElement(root, "SFJL1")
    for xiangmu in yizhu.shoufeixiangmu:
        SFJL1_ie = ET.SubElement(SFJL1, "Ie", {
            "YZNR21": xiangmu.yzsl,     "SFXM25": xiangmu.danjia, "SFXM01": xiangmu.xmid,
              "SFJL33": xiangmu.jbdwdj, 
            "SFJL25": xiangmu.zongliang, "KESHI14": xiangmu.zxksid, "VEG08": xiangmu.fyjlid, 
             "YZFB08":xiangmu.fubiaoid, "YZD31": xiangmu.yzdid, 
            "YPPC01": xiangmu.yppcid, "YPB23": xiangmu.cbj, "SFXM11": xiangmu.tcid, 
        })

    SQD1 = ET.SubElement(root, "SQD1")
    for shenqing in yizhu.shenqingdan:
        SQD1_ie = ET.SubElement(SQD1, "Ie", {
            "SQD01": shenqing.yzdid, "RYXX01": yizhu.brid ,"RYXX07": yizhu.jzid, 
              "SQD07": shenqing.jjbz, "KESHI11": shenqing.brksid,
          
        })

   
 
    xml_string = ET.tostring(root, encoding='utf-8').decode('utf-8')

    responJson = {'code':1,'result':'失败'}
    success = False
    sql = """
    DECLARE @out1 int,@out2 varchar(500);
    EXEC YiZhuQueRenQianJianCha ?,?, ?, ?, ?, ?, ?, ?, ?, ?, @out1 OUTPUT,@out2 OUTPUT;
    SELECT @out1,@out2;
    """
    conn = get_connection()
    cursor = conn.cursor() 
    try:
        cursor.execute(sql,  '123456',xml_string,0,0,0,1,yizhu.kzksid,fryid,fryno,fname)
        result = cursor.fetchone()
        logger.info( '确认医嘱前ID：'+str(result[0]) )
        logger.info( '确认医嘱前MSG：'+str(result[1]) )
        if result[0] == 0:
            success = True
        else:
            responJson = {'code':2,'result':result[1]}
        conn.commit() 
    except(Exception) as e:
        logger.error(traceback.format_exc())
        responJson = {'code':2,'result':'系统错误'}
    finally:
        cursor.close() 
        conn.close() 

    if not success:
        return responJson
    

    sql = """
    DECLARE @out1 varchar(500);
    EXEC QueRenYiZhu ?,?, ?, ?, ?, ?, ?, ?, ?, ?, @out1 OUTPUT;
    SELECT @out1;
    """
    conn = get_connection()
    cursor = conn.cursor() 
    try:
        cursor.execute(sql,  '123456',xml_string,0,0,0,1,yizhu.kzksid,fryid,fryno,fname)
        result = cursor.fetchone()
        logger.info( '确认医嘱结果：'+str(result[0]) )
        success = True
        conn.commit() 
        responJson = {'code':0,'result':'成功'}
    except(Exception) as e:
        logger.error(traceback.format_exc())
        responJson = {'code':2,'result':'系统错误'}
    finally:
        cursor.close() 
        conn.close() 

    return responJson

