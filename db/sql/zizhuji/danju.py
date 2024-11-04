

danjuSQL = '''
select  
'111' fjzid
,'测试歌' fname
,'20岁' fage
,'123456' fno
,'男' fgender
,'感冒' fzyzd
,'陈医生' fkdr
,'2024-10-10 12:12:12' fkdsj
,'123456' fdjh
where '1'<>?
and '1'<> ?
'''


danjumingxiSQL = '''
select 
'DR' fitem
,40.0 fprice
,'次' funit
,1 fcount
,40 famount
union all 
select 
'党参' fitem
,2 fprice
,'g' funit
,10 fcount
,20 famount
where '1'<> ?
and '1' not in  
'''



danjuZongJiaSQL = '''
select 1
'''


printInfoHeaderSQL = '''
select 1
'''