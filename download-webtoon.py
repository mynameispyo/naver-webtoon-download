from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
###User Setting###
start = 1
end = 200
titleId = 568986
path = "D:\"
##################
for i in range(start,end+1):
    with urlopen(f'https://comic.naver.com/webtoon/detail.nhn?titleId={titleId}&no={i}') as response:
        soup = BeautifulSoup(response, 'html.parser')
        for anchor in soup.find_all('img'):
            if anchor.get('src', '/')[:31] == "https://image-comic.pstatic.net":
                url = anchor.get('src', '/')

                img_data = requests.get(url, headers=headers).content
                with open(f'{path}{i}-{url[-7:]}', 'wb') as handler:
                    handler.write(img_data)
