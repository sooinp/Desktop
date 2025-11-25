# 네이버 검색 API 예제 - 블로그 검색
import os
import sys
import urllib.request
import datetime
import time
import json

client_id = 'JkDKuSrYnw3mhB2nuJWK'
client_secret = 'c7rVAkosfB'

# [CODE 1] : 실제 검색기(CODE 2 -> CODE 1으로 링크 전달되면 실제 내용 검색)
def getRequestUrl(url):
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print ("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

# [CODE 2] : 검색 링크 생성기
def getNaverSearch(node, srcTextStr, start, display):
    base = "https://openapi.naver.com/v1/search"
    node = "/%s.json" % node
    parameters = "?query=%s&start=%s&display=%s" % (urllib.parse.quote(srcTextStr), start, display)

    url = base + node + parameters
    responseDecode = getRequestUrl(url)   # [CODE 1]

    if (responseDecode == None):
        return None
    else:
        return json.loads(responseDecode)

# [CODE 3] : Get 데이터 -> 딕셔너리로 묶음
def getPostData(post, jsonResult, cnt):
    title = post['title']
    description = post['description']
    #org_link = post['originallink']
    link = post['link']
    bloggername = post['bloggername']
    bloggerlink = post['bloggerlink']
    postdate = post['postdate']

    # pDate = datetime.datetime.strptime(post['pubDate'],  '%a, %d %b %Y %H:%M:%S +0900')
    # pDate = pDate.strftime('%Y-%m-%d %H:%M:%S')

    jsonResult.append({'cnt':cnt, 'title':title, 'description': description,
'bloggername':bloggername,  'bloggerlink':bloggerlink,  'postdate':postdate,   'link': link})

# [CODE 0]
def main():
    node = 'blog'   # 크롤링 대상 노드
    srcText = input('검색어를 입력하세요: ').split(" ")
    srcTextStr = ' '.join(srcText)
    cnt = 0
    jsonResult = []

    jsonResponse = getNaverSearch(node, srcTextStr, 1, 100)  # [CODE 2] ## 1: 첫 번째 페이지, 100: 100개(한 번에 가져오는 개수)

    total = jsonResponse['total']

    while ((jsonResponse != None) and (jsonResponse['display'] != 0)): #응답이 한 개 이상 존재하면 while, 응답 없거나 결과 0개면 멈춤
        for post in jsonResponse['items']:
            cnt += 1
            # print(post.keys())
            getPostData(post, jsonResult, cnt)  # [CODE 3]

        start = jsonResponse['start'] + jsonResponse['display'] # start 위치를 페이지마다 변경해서 search나 get 해올 수 있게 함
        if start == 3001: break    # 네이버 blog는 3000개까지만 무료 제공됨
        jsonResponse = getNaverSearch(node, srcTextStr, start, 100)  #[CODE 2]

    print('전체 검색 : %d 건' %total)

    with open('%s_naver_%s.json' % (srcTextStr, node), 'w', encoding='utf8') as outfile:
        jsonFile = json.dumps(jsonResult,  indent = 4, sort_keys = True,  ensure_ascii = False)

        outfile.write(jsonFile)

    print("가져온 데이터 : %d 건" %(cnt))
    print ('%s_naver_%s.json SAVED' % (srcTextStr, node))

if __name__ == '__main__':
    main()