import requests
import xmltodict
import json
import pymysql
import googlemaps
import mysql.connector
from mysql.connector import errorcode

url = """http://175.125.91.94/oasis/service/rest/convergence2019/getConver03"""

API_KEY='your key'
gmaps = googlemaps.Client(key=API_KEY)

def geoCoding(addr):
    geocode_result = gmaps.geocode(addr)
    components = geocode_result[0]
    geometry = components['geometry']
    location = geometry['location']
    return location

# con = pymysql.connect(host='localhost', user='root',
#                     password='password', db='petplace', charset='utf8')
# Obtain connection string information from the portal
config = {
  'host':'yourhost',
  'user':'youruser',
  'password':'yourpassword',
  'database':'petplace'
}

# Construct connection string
try:
   con = mysql.connector.connect(**config)
   print("Connection established")
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with the user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
    cursor = con.cursor()
    sql = 'insert into facility values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'

    count = 1
    for page in range(1,412):
    #for page in range(100,101):
        print(page)
        content = requests.get(url+'?pageNo='+str(page)).content

        dic = xmltodict.parse(content)
        jsonString = json.dumps(dic['response']['body'], ensure_ascii=False)
        jsonObj = json.loads(jsonString)
        items = jsonObj['items']
        if page<411:
            item = items['item']
        else:
            item = [items['item']]

        for i in item:
            if 'state' in i:
                state = i['state']
                if state == '폐업':
                    continue
            else:
                continue
            address = i['venue']
            if address is None:
                continue
            if i['subjectCategory']=='동물병원':
                f_id = 'h'+str(count).zfill(4)
                #geocoding
                location = geoCoding(address)
                latitude = location['lat']
                longitude = location['lng']
                description = None
            elif i['subjectCategory']=='동물약국':
                f_id = 'p'+str(count).zfill(4)
                #geocoding
                location = geoCoding(address)
                latitude = location['lat']
                longitude = location['lng']
                description = None
            else:
                f_id = 'a'+str(count).zfill(4)
                if 'spatial' in i:
                    temp = str(i['spatial']).split()
                    if len(temp) == 4:
                        latitude = float(temp[3])
                        longitude = float(temp[2][:-1])
                    else:
                        #geocoding
                        location = geoCoding(address)
                        latitude = location['lat']
                        longitude = location['lng']
                else:
                    continue
                description = i['description']
                description += ', ' + i['subDescription']
            if 'title' in i:
                title = i['title']
            else:
                title = i['venue']+' '+i['subjectCategory']
            gu = i['affiliation']
            if 'reference' in i:
                tel = i['reference']
            else:
                tel = '-'

            cursor.execute(sql, (f_id, title, gu, address, tel, latitude, longitude, state, description))
            count += 1

    con.commit()
    con.close()