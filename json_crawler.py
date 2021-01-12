import requests
import pymysql

url ='https://dapi.kakao.com/v3/search/book'
header = {
    'Authorization': 'KakaoAK yourkey'
}
params={
    'query':'사람',
    'size':10,
    'page':1
}

data = requests.get(url,headers=header,params=params).json() #응답을 Json으로 받아달라.
#print(data)
books = data['documents']

con = pymysql.connect(host='localhost',user='root', password='password',db='crawl_data',charset='utf8')
cursor = con.cursor()
sql = """insert into books(title,authors,publisher,price)
        values(%s,%s,%s,%s)""" 
        #db로 넘어갈 때 sql문 자체가 string이기 때문에 전부string 포맷으로 해야함

for item in books :
    authors = ', '.join(item['authors'])
    title = item['title']
    price = item['price']
    publisher = item['publisher']
    print('{}:{}:{}:{}'.format(title,authors,publisher,price))
    cursor.execute(sql,(title,authors,publisher,price))#데이터는 튜플로 넣기

con.commit()
con.close()

