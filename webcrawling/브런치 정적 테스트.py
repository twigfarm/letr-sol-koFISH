import requests
from bs4 import BeautifulSoup as bs

url = 'https://brunch.co.kr/@inb4032/4'
res = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})

#test = requests.get(url)
#print(test)
#print(res.raise_for_status())

soup = bs(res.text, "html.parser")
print(soup.text)

dlist = soup.findAll('p', attrs={"class":"wrap_item"})
#print(dlist    ist)


'''
firstidx = dlist.find('>')  #다음'>'까지의 위치 찾기
text=dlist[lfirstidx+1:]    #해당 위치까지 자르기 (태그 부분이 잘린다)
lastidx=text.find('<')      #다음 '<'의 위치 찾기
list.append(text[:lastidx]) #알맹이를 뽑아서 리스트에 추가
'''

'''
while len(dlist)>0 :
    firstidx=dlist.find('>')
    text=dlist[firstidx+1:]
    lastidx=dlist.find('<')
    list.append(dlist[:lastidx])
    
print(list)
'''

'''
.service_contents > 

from urllib.request import Request, urlopen
html = urlopen("https://brunch.co.kr/@inb4032/4")
bsObject = bs(html, "html.parser")

#for meta in bsObject.head.find_all('meta'):
    #print(meta.get('content'))
#print(bsObject.head.find("meta", {"name":"description"}))
print(bsObject.head.find("meta", {"name":"description"}).get('content'))

'''
