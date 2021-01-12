import requests
import xmltodict
import json
import pymysql

url = """http://open.gyeongnam.go.kr/rest/gyeongnampoliceoffice/getGyeongnampoliceofficeList?serviceKey=yourkey&pageNo=1&numOfRows=30"""

content= requests.get(url).content
#print(content)

dic = xmltodict.parse(content) #xml을 받아서 딕셔너리로 바꿔줌
#print(dic) #딕셔너리.items() 했을 때처럼 튜플에 key,value로 보임
#ensure_ascii=False 한글 보이게 처리 dumps: 제이슨 스트링으로 바꿔줌
jsonString= json.dumps(dic['rfcOpenApi']['body'], ensure_ascii=False)
#print(jsonString)
jsonObj= json.loads(jsonString) #loads:jsonobject으로 바꿔줌
data = jsonObj['data']
stations = data['list']

con = pymysql.connect(host='localhost',user='root', password='pass',
                    db='crawl_data',charset='utf8')
cursor = con.cursor()
sql = 'insert into police values(%s,%s,%s,%s,%s,%s)'
    #혹은 insert into police(entid,title,tel,homepage,roadaddress,sigungu) values(%s,%s,%s,%s,%s,%s)
for item in stations:
    title= item['title']
    tel = item['tel']
    homepage= item['homepage']
    roadaddress= item['roadaddress']
    sigungu = item['sigungu']
    entid = item['entid']
    
    #print("{}:{}:{}:{}:{}:{}".format(title,tel,homepage,roadaddress,sigungu,entid))
    cursor.execute(sql,(entid,title,tel,homepage,roadaddress,sigungu))

con.commit()
con.close()

