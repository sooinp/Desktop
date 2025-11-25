import urllib.request
import datetime
import time
import json
import pandas as pd

ServiceKey = '843107c0957f6bcc968e6f505aeb6d6f41e5116cb8d1b80ec28d954f3a4d6728'


#[CODE 1]
def getRequestUrl(url):
    req = urllib.request.Request(url)
    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for Url: %s" % (datetime.datetime.now(), url))
        return None
    
#[CODE 2]
def getTourismStatsItem(yyyymm, nat_cd, ed_cd):
    service_url = "http://openapi.tour.go.kr/openapi/service/EdrcntTourismStatsService/getEdrcntTourismStatsList"
    parameters = "?_type=json&serviceKey=" + ServiceKey #인증키
    parameters += "&YM=" + yyyymm
    parameters += "&NAT_CD=" + nat_cd
    parameters += "&ED_CD=" + ed_cd

    url = service_url + parameters
    print(url)  #액세스 거부 여부 확인용 출력기
    responseDecode = getRequestUrl(url)  #[CODE 1]
    
    if (responseDecode == None):
        return None
    else:
        return json.loads(responseDecode)
    
#[CODE 3]
def getTourismStatsService(nat_cd, ed_cd, nStartYear, nEndYear):
    jsonResult = []
    result = []
    natName = ''
    ed = ''
    dataEND = "{0}{1:0>2}".format(str(nEndYear), str(12))
    isDataEnd = 0  #데이터 끝 확인용 flag 초기화
    
    for year in range(nStartYear, nEndYear+1):
        for month in range(1, 13):
            if (isDataEnd == 1): break  #수집기간 남아도 데이터 끝나면 중지
            
            yyyymm = "{0}{1:0>2}".format(str(year), str(month))
            jsonData = getTourismStatsItem(yyyymm, nat_cd, ed_cd) #[CODE 2]
            
            if (jsonData['response']['header']['resultMsg'] == 'OK'):
                if not jsonData['response']['body']['items']:  #데이터 없는 마지막 항목의 경우
                    isDataEnd = 1
                    if (month - 1) == 0:  #마지막 데이터가 12월인데, 현재 month가 다음 해 1월인 경우, year와 month 변수 조정
                        year = year - 1
                        month = 13
                    dataEND = "{0}{1:0>2}".format(str(year), str(month - 1))
                    print("데이터 없음.... \n제공되는 통계 데이터는 %s년 %s월까지입니다.\n" % (str(year), str(month-1)), '-'*70)
                    jsonData = getTourismStatsItem(dataEND, nat_cd, ed_cd)  #출력용, 마지막 데이터 재호출
                    break
                
                natName = jsonData['response']['body']['items']['item']['natKorNm']
                natName = natName.replace(' ', '')
                num = jsonData['response']['body']['items']['item']['num']
                ed = jsonData['response']['body']['items']['item']['ed']
                print('[%s_%s : %s]' % (natName, yyyymm, num))
                print('-'*70)
                jsonResult.append({'nat_name':natName, 'nat_cd':nat_cd, 'yyyymm':yyyymm, 'visit_cnt':num})
                result.append([natName, nat_cd, yyyymm, num])
                
    #마지막 jsonData 확인용 출력기
    print('<마지막 jsonData>\n',json.dumps(jsonData, indent=4, sort_keys=True, ensure_ascii=False))
    return (jsonResult, result, natName, ed, dataEND)

                
#[CODE 0]
def main():
    jsonResult = []
    result = []
    natName=''
    
    print("<< 국내 입국한 외국인의 통계 데이터를 수집합니다. >>")
    nat_cd = input("국가 코드를 입력하세요(예> 중국 112, 일본 130, 미국 275): ")
    nStartYear = int(input("데이터를 몇 년부터 수집할까요?: "))
    nEndYear = int(input("데이터를 몇 년까지 수집할까요?: "))
    ed_cd = "E"  #E: 방한외래관광객, D: 해외 출국
    
    jsonResult, result, natName, ed, dataEND = getTourismStatsService(nat_cd, ed_cd, nStartYear, nEndYear)  #[CODE 3]
    if (natName == ''):  #URL 요청은 성공했으나 데이터 제공X인 경우
        print("데이터가 전달되지 않았습니다. 공공데이터포털의 서비스 상태를 확인하시기 바랍니다.")
    else:
        #파일 저장1: json 파일
        with open('./%s_%s_%d_%s.json' % (natName, ed, nStartYear, dataEND), 'w', encoding='utf8') as outfile:
            jsonFile = json.dumps(jsonResult, indent = 4, sort_keys = True, ensure_ascii = False)
            outfile.write(jsonFile)
        #파일 저장2: csv 파일
        columns = ["입국자국가", "국가코드", "입국연월", "입국자 수"]
        result_df = pd.DataFrame(result, columns = columns)
        result_df.to_csv('./%s_%s_%d_%s.csv' % (natName, ed, nStartYear, dataEND), index = False, encoding = 'cp949')
        
if __name__=='__main__':
    main()