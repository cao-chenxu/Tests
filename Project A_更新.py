import requests
from bs4 import BeautifulSoup
import pandas as pd

# �õ�ҳ�������
request_url = 'http://car.bitauto.com/xuanchegongju/?l=8&mid=8'
headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
html=requests.get(request_url,headers=headers,timeout=10)
content = html.text

# ͨ��content����BeautifulSoup����
soup = BeautifulSoup(content, 'html.parser', from_encoding='gbk')

#��ȡ�����ĳ�����Ϣ��
temp = soup.find('div',class_="search-result-list")
print(temp)
df = pd.DataFrame(columns = ['car_name', 'car_price', 'imgsource'])
a_list = temp.find_all('a')
print(a_list)

for a in a_list:
    temp = {}
    p_list = a.find_all('p')
    imgsource = a.find_all('img')
    print(imgsource)
    if len(p_list) > 0:
        car_name, car_price, imgsource = p_list[0].text, p_list[1].text, imgsource
        temp['car_name'], temp['car_price'], temp['imgsource'] = car_name, car_price, imgsource
        df = df.append(temp, ignore_index=True)
print(df)

#��������
df['car_price'] = df['car_price'].str.replace('��','')
df['car_price'] = df['car_price'].str.replace('����','')
print(df['car_price'])
df[['min_price','max_price']] = df['car_price'].str.split('-',expand=True)
df.drop('car_price', axis=1, inplace=True)


#�����ݱ��浽csv�ļ���
data = pd.DataFrame(columns = ['car_name', 'min_price', 'max_price', 'imgsource'])
data['car_name'], data['min_price'], data['max_price'], data['imgsource'] = df['car_name'], df['min_price'], df['max_price'], df['imgsource']
data.to_csv('�׳���.csv', encoding='gbk', index=False)

