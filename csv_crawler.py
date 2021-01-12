import csv
import pymysql

file = open('police.csv','r',encoding='utf8')
reader = csv.reader(file)

con = pymysql.connect(host='localhost',user='root', password='password',db='crawl_data',charset='utf8')
cursor = con.cursor()
sql = 'insert into police(entid,title,tel,homepage,roadaddress,sigungu) values(%s,%s,%s,%s,%s,%s)'

for line in reader:
    title = line[0]
    tel = line[1]
    homepage= line[2]
    roadaddress= line[3]
    sigungu= line[4]
    entid= line[5]
    cursor.execute(sql,(entid,title,tel,homepage,roadaddress,sigungu))

    print(title,tel)

con.commit()
con.close()

